# Tutorial gem5: modo System-call Emulation (SE)

## Introdução

O modo **System-call Emulation (SE)** do gem5 executa uma aplicação de usuário sem inicializar um kernel, uma imagem de disco ou o processo de boot de uma máquina completa. O simulador carrega o executável, modela a plataforma configurada — CPU, caches, interconexão e memória — e emula as chamadas de sistema necessárias.

Este tutorial usa como carga de trabalho a **multiplicação clássica de matrizes quadradas**. Ela foi escolhida no lugar de soma de vetores porque apresenta maior reutilização de dados e permite observar mais claramente o efeito da hierarquia de caches.

> SE é indicado para estudos controlados de arquitetura com programas de usuário. Para avaliar boot, kernel, drivers, rede ou um ambiente Linux completo, use o modo Full System (FS).

## Objetivos

Ao final, você deverá conseguir:

1. explicar o escopo e as limitações do modo SE;
2. implementar e compilar um programa para a ISA simulada;
3. executar a carga no modo SE pela linha de comando;
4. configurar uma execução equivalente usando a API Python do gem5;
5. interpretar `stats.txt` e comparar configurações de cache.

---

# 1. Fundamentos do modo SE

## 1.1 O que é modelado

Durante uma execução SE, o gem5 pode modelar:

- uma ou mais CPUs simuladas;
- caches L1, L2 e outros níveis da hierarquia;
- barramentos, controladores e memória DRAM;
- memória virtual e o processo simulado;
- instruções, ciclos, acessos e faltas de cache.

Quando a aplicação usa uma syscall suportada — por exemplo, escrita em `stdout`, alocação de memória ou encerramento — o gem5 trata essa operação por sua camada de emulação.

## 1.2 O que SE não inclui

SE não inicializa bootloader, kernel Linux convidado, shell, serviços, drivers nem dispositivos como subsistemas completos de um sistema operacional. Portanto, ele não é uma distribuição Linux simulada.

| Aspecto | SE | FS |
|---|---|---|
| Kernel convidado | Não | Sim |
| Imagem de disco | Normalmente não | Normalmente sim |
| Preparação | Menor | Maior |
| Custo de simulação | Geralmente menor | Geralmente maior |
| Estudo de aplicação, CPU e cache | Muito adequado | Possível |
| Estudo de SO e dispositivos | Inadequado | Adequado |

## 1.3 Quando usar SE

Use SE para comparar modelos de CPU, tamanhos de cache, associatividade, latência de memória e comportamento de microbenchmarks ou programas C/C++ autocontidos. Prefira FS quando o experimento depender de recursos reais do kernel ou de software que exige um ambiente Linux completo.

---

# 2. Pré-requisitos

Os comandos usam a ISA **RISC-V de 64 bits**. Troque `RISCV` e a ferramenta de compilação pela ISA escolhida.

```bash
cd ~/gem5
scons build/RISCV/gem5.opt -j"$(nproc)"
```

Em Ubuntu/Debian, instale uma toolchain cruzada para RISC-V:

```bash
sudo apt update
sudo apt install build-essential gcc-riscv64-linux-gnu
```

Crie o diretório do experimento:

```bash
mkdir -p ~/gem5-tutorial/se-matrizes
cd ~/gem5-tutorial/se-matrizes
```

> O executável deve ter a mesma ISA do binário do gem5. Um ELF x86 não pode ser carregado em uma simulação RISC-V.

---

# 3. Etapa 1 — Implementar o programa de multiplicação de matrizes

Crie `multiplica_matrizes.c`:

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#ifndef N_PADRAO
#define N_PADRAO 128
#endif

static uint64_t checksum(const int *m, size_t n)
{
    uint64_t soma = 0;
    for (size_t i = 0; i < n * n; ++i)
        soma += (uint32_t)m[i];
    return soma;
}

int main(int argc, char **argv)
{
    size_t n = N_PADRAO;
    if (argc == 2)
        n = strtoul(argv[1], NULL, 10);

    if (n == 0 || n > 1024) {
        fprintf(stderr, "Uso: %s [ordem entre 1 e 1024]\n", argv[0]);
        return 1;
    }

    size_t elementos = n * n;
    int *a = calloc(elementos, sizeof(*a));
    int *b = calloc(elementos, sizeof(*b));
    int *c = calloc(elementos, sizeof(*c));

    if (!a || !b || !c) {
        fprintf(stderr, "Erro: falha ao alocar matrizes.\n");
        free(a); free(b); free(c);
        return 1;
    }

    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n; ++j) {
            a[i * n + j] = (int)((i + j) % 17);
            b[i * n + j] = (int)((2 * i + j) % 13);
        }
    }

    /* C = A x B: ordem i-j-k, simples e adequada para o experimento. */
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n; ++j) {
            int acumulador = 0;
            for (size_t k = 0; k < n; ++k)
                acumulador += a[i * n + k] * b[k * n + j];
            c[i * n + j] = acumulador;
        }
    }

    printf("ordem=%zu checksum=%llu\n", n,
           (unsigned long long)checksum(c, n));
    free(a); free(b); free(c);
    return 0;
}
```

O programa aloca três matrizes `N × N`, inicializa `A` e `B`, calcula `C = A × B` e imprime um *checksum*. O checksum impede que o resultado seja irrelevante e também permite validar que diferentes execuções fizeram o mesmo trabalho.

A ordem dos três laços é `i-j-k`. Para cada elemento de `C`, o programa percorre uma linha de `A` e uma coluna de `B`. Como a linguagem C armazena matrizes por linhas, o acesso a `B` é menos local; isso torna o programa útil para estudos de cache. Não altere a ordem dos laços entre experimentos se quiser compará-los diretamente.

---

# 4. Etapa 2 — Compilar para a ISA simulada

## 4.1 RISC-V

A ligação estática diminui a dependência de bibliotecas compartilhadas durante a execução em SE:

```bash
riscv64-linux-gnu-gcc \
  -O2 -static -march=rv64gc -mabi=lp64d \
  -o multiplica_matrizes_riscv multiplica_matrizes.c
```

Verifique o ELF gerado:

```bash
file multiplica_matrizes_riscv
```

A saída deve indicar `ELF 64-bit`, `RISC-V` e, idealmente, `statically linked`.

## 4.2 Outras ISAs

| ISA simulada | Exemplo de compilação |
|---|---|
| x86 | `gcc -O2 -static -o multiplica_matrizes_x86 multiplica_matrizes.c` |
| ARM 64 bits | `aarch64-linux-gnu-gcc -O2 -static -o multiplica_matrizes_arm64 multiplica_matrizes.c` |
| RISC-V 64 bits | `riscv64-linux-gnu-gcc -O2 -static -o multiplica_matrizes_riscv multiplica_matrizes.c` |

Use `-O2` consistentemente. Flags de compilação alteram o fluxo de instruções e podem alterar de modo substancial as estatísticas; por isso, devem ser registradas e mantidas constantes durante uma comparação arquitetural.

---

# 5. Etapa 3 — Executar SE pela linha de comando

Defina caminhos:

```bash
export GEM5=~/gem5
export ISA=RISCV
export GEM5_BIN="$GEM5/build/$ISA/gem5.opt"
export PROG=~/gem5-tutorial/se-matrizes/multiplica_matrizes_riscv
```

Execute uma configuração inicial com `TimingSimpleCPU`, caches L1 e L2:

```bash
"$GEM5_BIN" \
  --outdir=out-se-cli \
  "$GEM5/configs/example/se.py" \
  --cmd="$PROG" \
  --options="128" \
  --cpu-type=TimingSimpleCPU \
  --num-cpus=1 \
  --caches \
  --l1i_size=32KiB \
  --l1d_size=32KiB \
  --l2cache \
  --l2_size=256KiB \
  --mem-size=512MiB
```

| Opção | Função |
|---|---|
| `--outdir` | Diretório exclusivo dos resultados. |
| `se.py` | Script de configuração para System-call Emulation. |
| `--cmd` | Executável a ser carregado. |
| `--options` | Argumentos entregues ao programa; aqui, a ordem da matriz. |
| `--cpu-type` | Modelo de CPU. |
| `--caches` | Habilita caches L1. |
| `--l2cache` | Habilita a L2. |
| `--mem-size` | Memória física simulada. |

## 5.1 Validar o resultado funcional

Ao terminar, confira a saída do programa e o motivo do encerramento:

```bash
cat out-se-cli/simout
grep -Ei "exit|exiting" out-se-cli/simout
```

A saída deve conter `ordem=128 checksum=...`. Em execuções com a mesma ISA, binário e argumento, o checksum deve permanecer igual. Antes de analisar desempenho, confirme também que o programa encerrou normalmente.

Arquivos relevantes:

- `stats.txt`: estatísticas coletadas;
- `config.ini`: objetos e parâmetros efetivamente instanciados;
- `config.json`: configuração em formato estruturado;
- `simout` e `simerr`: saída padrão e mensagens da simulação.

## 5.2 Limitar instruções para depuração

Para verificar rapidamente uma configuração:

```bash
"$GEM5_BIN" \
  --outdir=out-se-teste \
  "$GEM5/configs/example/se.py" \
  --cmd="$PROG" --options="128" \
  --cpu-type=TimingSimpleCPU --caches \
  --maxinsts=1000000
```

Se o limite for atingido, a simulação representa apenas uma execução parcial. Não compare desempenho final com esse limite ativo, a menos que todas as execuções sejam deliberadamente limitadas ao mesmo ponto.

---

# 6. Etapa 4 — Executar SE com a API Python

A API Python é recomendada para experimentos reproduzíveis, pois a plataforma é descrita explicitamente no script.

Crie `se_matrizes.py`:

```python
from pathlib import Path

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import CustomResource
from gem5.simulate.simulator import Simulator

isa = ISA.RISCV

cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1i_size="32KiB",
    l1d_size="32KiB",
    l2_size="256KiB",
)

memory = SingleChannelDDR3_1600(size="512MiB")

processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING,
    isa=isa,
    num_cores=1,
)

board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

programa = CustomResource(
    local_path=str(Path.home() / "gem5-tutorial/se-matrizes/multiplica_matrizes_riscv")
)

board.set_se_binary_workload(
    binary=programa,
    arguments=["128"],
)

Simulator(board=board).run()
```

Execute-o a partir do diretório do experimento:

```bash
cd ~/gem5-tutorial/se-matrizes
"$GEM5_BIN" --outdir=out-se-api se_matrizes.py
```

A configuração contém quatro partes: o `SimpleProcessor` define CPU e ISA; a hierarquia define L1 e L2; o modelo de memória define DRAM; `SimpleBoard` conecta os componentes e recebe o binário via `set_se_binary_workload()`.

> As classes e os caminhos de importação podem variar entre versões do gem5. Caso ocorra um erro de importação, use a documentação e os exemplos correspondentes à versão instalada.

---

# 7. Etapa 5 — Escolher o modelo de CPU

| Modelo | Uso apropriado |
|---|---|
| `AtomicSimpleCPU` | Testes funcionais rápidos; não serve para timing detalhado. |
| `TimingSimpleCPU` | Primeiro estudo de caches e latência. |
| `MinorCPU` | Pipeline in-order mais detalhado. |
| `O3CPU` | Estudos de execução fora de ordem; maior custo de simulação. |

Exemplo usando `O3CPU`:

```bash
"$GEM5_BIN" \
  --outdir=out-se-o3 \
  "$GEM5/configs/example/se.py" \
  --cmd="$PROG" --options="128" \
  --cpu-type=O3CPU \
  --caches --l2cache --mem-size=512MiB
```

Uma comparação válida deve manter constantes programa, argumento, ISA, flags de compilação, clock, memória e caches; altere somente a variável sob estudo.

---

# 8. Etapa 6 — Interpretar `stats.txt`

Abra o arquivo ao final da simulação:

```bash
less out-se-cli/stats.txt
```

Localize métricas importantes:

```bash
grep -E "simSeconds|simTicks|simInsts|numCycles|ipc|overallMissRate" out-se-cli/stats.txt
```

Os nomes completos dependem da configuração, mas as métricas representam:

| Métrica | Interpretação |
|---|---|
| `simSeconds` | Tempo na máquina simulada, não o tempo gasto pelo computador hospedeiro. |
| `simTicks` | Tempo interno simulado em *ticks*. |
| `simInsts` | Instruções simuladas, quando disponível. |
| `numCycles` | Ciclos do componente, geralmente da CPU. |
| `ipc` | Instruções por ciclo. |
| `overallMissRate` | Proporção de acessos que falharam na cache. |
| `overallMissLatency` | Latência média associada às faltas. |

O IPC é dado por:

\[
IPC = \frac{\text{instruções executadas}}{\text{ciclos}}.
\]

Uma taxa de faltas pode ser expressa como:

\[
\text{taxa de faltas} = \frac{\text{misses}}{\text{acessos}}.
\]

Para descobrir os nomes reais das estatísticas de cache na sua execução:

```bash
grep -i "cache" out-se-cli/stats.txt | head -n 60
grep -n -E "size=|assoc=|clk_domain" out-se-cli/config.ini | head -n 80
```

`config.ini` é essencial: ele registra a configuração efetivamente criada, e não apenas a configuração pretendida.

## 8.1 Experimento sugerido: L1D de 16 KiB versus 64 KiB

Execute duas vezes, variando apenas a L1 de dados:

```bash
# L1D de 16 KiB
"$GEM5_BIN" --outdir=out-l1d-16k \
  "$GEM5/configs/example/se.py" \
  --cmd="$PROG" --options="128" \
  --cpu-type=TimingSimpleCPU --caches \
  --l1i_size=32KiB --l1d_size=16KiB \
  --l2cache --l2_size=256KiB --mem-size=512MiB

# L1D de 64 KiB
"$GEM5_BIN" --outdir=out-l1d-64k \
  "$GEM5/configs/example/se.py" \
  --cmd="$PROG" --options="128" \
  --cpu-type=TimingSimpleCPU --caches \
  --l1i_size=32KiB --l1d_size=64KiB \
  --l2cache --l2_size=256KiB --mem-size=512MiB
```

Compare checksum, instruções, ciclos, `simSeconds`, IPC, acessos e faltas da L1D, além das faltas no nível seguinte. Os checksums precisam ser iguais; diferenças indicam que a carga de trabalho não foi equivalente.

Uma L1D maior pode reduzir faltas, mas não garante menor tempo simulado: a carga pode ser limitada por computação, a L2 pode absorver as faltas ou a latência da cache maior pode ser diferente no modelo. A conclusão deve considerar todas as métricas relevantes.

---

# 9. Boas práticas e solução de problemas

1. Use executáveis estáticos, especialmente na primeira validação.
2. Registre versão do gem5, ISA, compilador e flags de compilação.
3. Use um diretório `--outdir` diferente para cada experimento.
4. Valide o checksum e o encerramento normal antes de comparar desempenho.
5. Diferencie tempo simulado de tempo de parede no host.
6. Analise `stats.txt` junto com `config.ini`; não tire conclusões a partir de uma única métrica.

## Problemas comuns

**Executável incompatível:** confirme a ISA com `file multiplica_matrizes_riscv` e recompile para a arquitetura correta.

**Bibliotecas ausentes:** recompile com `-static`, caso a toolchain permita.

**Programa não terminou:** remova ou aumente `--maxinsts` e confira `simout` e `simerr`.

**Estatísticas de cache não aparecem:** confirme `--caches` e `--l2cache`, depois examine `config.ini` para identificar os objetos criados.

---

# Conclusão

O modo SE permite estudar uma aplicação de usuário no gem5 com menor complexidade que FS. Neste tutorial, a multiplicação de matrizes fornece uma carga de trabalho com comportamento de memória suficiente para comparar CPUs e hierarquias de cache. O fluxo recomendado é: compilar para a ISA correta, validar o checksum, executar configurações controladas e interpretar `stats.txt` em conjunto com `config.ini`.