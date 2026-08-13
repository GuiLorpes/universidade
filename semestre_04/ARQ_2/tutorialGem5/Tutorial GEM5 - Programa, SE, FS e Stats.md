# Tutorial gem5 — execução de programa em SE e FS e análise de estatísticas

## Introdução

Este tutorial mostra como preparar e executar um programa C simples no **gem5**, tanto no modo **System-call Emulation (SE)** quanto no modo **Full System (FS)**. Também mostra duas formas de iniciar cada experimento: por meio dos scripts de configuração fornecidos pelo gem5, na linha de comando, e por scripts próprios escritos com a API Python moderna (`gem5.components` e `gem5.simulate`).

> **Versão e premissas:** os exemplos de API Python usam o gem5 contemporâneo e assumem que o repositório foi compilado em `build/X86/gem5.opt`. Os nomes e as opções dos scripts legados em `configs/example/` podem mudar entre versões; confirme-os com `--help` na sua cópia do gem5.

## Objetivo

Ao final, você deverá ser capaz de:

1. implementar um programa de carga controlada;
2. compilá-lo com GCC e Clang para uma ISA alvo do gem5;
3. executá-lo em SE por linha de comando e por API Python;
4. executá-lo em FS por linha de comando e por API Python;
5. localizar e interpretar métricas essenciais de `stats.txt`.

---

## 1. Conceitos: SE e FS

| Modo | O que o gem5 simula | Quando usar |
|---|---|---|
| **SE (System-call Emulation)** | Processo de usuário e as chamadas de sistema mais comuns. Não inicializa kernel nem sistema de arquivos convidados. | Microbenchmarks, estudos de CPU/cache e experimentos rápidos. |
| **FS (Full System)** | Máquina inteira: firmware, kernel Linux, dispositivos, disco e processos. | Estudos de sistema operacional, E/S, rede, boot, drivers e comportamento de múltiplos processos. |

No modo SE, o binário é informado diretamente ao gem5. No modo FS, o binário precisa estar acessível **dentro da imagem de disco do sistema convidado**, e a execução normalmente é solicitada por um script no boot ou pelo console do Linux convidado.

---

## 2. Pré-requisitos e organização

Parta de um checkout do gem5 já compilado para X86:

```bash
cd ~/gem5
scons build/X86/gem5.opt -j"$(nproc)"
```

Crie um diretório de trabalho separado:

```bash
mkdir -p ~/gem5-lab/{src,bin,configs,resources,results}
cd ~/gem5-lab
```

Nos comandos a seguir, ajuste estas variáveis conforme sua instalação:

```bash
export GEM5_HOME="$HOME/gem5"
export GEM5_BIN="$GEM5_HOME/build/X86/gem5.opt"
export LAB="$HOME/gem5-lab"
```

Verifique o executável:

```bash
"$GEM5_BIN" --version
```

---

# Prática

## Etapa 1 — Implementar o programa de experimento

Crie `src/vector_sum.c`. O programa soma dois vetores de inteiros e mede apenas uma região de interesse (ROI) com `m5_work_begin` e `m5_work_end`. Esses marcadores são úteis no modo FS para delimitar estatísticas, mas o programa continua funcionando em SE quando compilado sem eles.

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#ifdef GEM5_M5OPS
#include <gem5/m5ops.h>
#endif

#ifndef N
#define N (1 << 20)
#endif

int main(void)
{
    int32_t *a = malloc(N * sizeof(*a));
    int32_t *b = malloc(N * sizeof(*b));
    int32_t *c = malloc(N * sizeof(*c));

    if (a == NULL || b == NULL || c == NULL) {
        fprintf(stderr, "Falha ao alocar vetores\\n");
        free(a);
        free(b);
        free(c);
        return 1;
    }

    for (size_t i = 0; i < N; ++i) {
        a[i] = (int32_t)i;
        b[i] = (int32_t)(2 * i);
    }

#ifdef GEM5_M5OPS
    m5_work_begin(0, 0);
#endif

    int64_t checksum = 0;
    for (size_t i = 0; i < N; ++i) {
        c[i] = a[i] + b[i];
        checksum += c[i];
    }

#ifdef GEM5_M5OPS
    m5_work_end(0, 0);
#endif

    printf("N=%d checksum=%lld\\n", N, (long long)checksum);

    free(a);
    free(b);
    free(c);
    return 0;
}
```

O resultado esperado é:

```text
N=1048576 checksum=1649265868800
```

> Para estudos mais longos, aumente `N`, por exemplo com `-DN='(1<<24)'` na compilação. Registre esse valor junto com os resultados.

---

## Etapa 2 — Compilar para gem5 com GCC e Clang

### 2.1 Escolha da ISA e do compilador

O binário deve ser compatível com a ISA que foi compilada no gem5. Neste tutorial, `build/X86/gem5.opt` exige um binário **x86-64**. Em um host x86-64, GCC e Clang normalmente geram esse formato por padrão.

Para ARM, RISC-V ou outra ISA, use o respectivo *cross-compiler* e compile o gem5 para a mesma ISA, por exemplo `build/ARM/gem5.opt` ou `build/RISCV/gem5.opt`.

### 2.2 Binário para SE com GCC

Em SE, não use as m5ops neste exemplo. Gere um binário estático para reduzir dependências de bibliotecas dinâmicas:

```bash
gcc -O2 -std=c11 -Wall -Wextra -static \
  "$LAB/src/vector_sum.c" -o "$LAB/bin/vector_sum_gcc"
file "$LAB/bin/vector_sum_gcc"
```

### 2.3 Binário para SE com Clang

```bash
clang -O2 -std=c11 -Wall -Wextra -static \
  "$LAB/src/vector_sum.c" -o "$LAB/bin/vector_sum_clang"
file "$LAB/bin/vector_sum_clang"
```

Se o seu Clang não encontrar a biblioteca C estática, instale o pacote de desenvolvimento da libc da sua distribuição ou use GCC. Como alternativa, gere um binário dinâmico, mas então as bibliotecas necessárias precisarão existir no ambiente simulado.

### 2.4 Binário para FS com GCC e m5ops

Para usar os marcadores de ROI no Linux convidado, obtenha e compile a biblioteca de m5ops do próprio gem5:

```bash
cd "$GEM5_HOME/util/m5"
scons build/x86/out/m5
```

Compile o programa para o FS. O caminho de `m5ops.h` pode variar por versão; localize-o se necessário com `find "$GEM5_HOME" -name m5ops.h`.

```bash
gcc -O2 -std=c11 -Wall -Wextra -static -DGEM5_M5OPS \
  -I"$GEM5_HOME/include" \
  "$LAB/src/vector_sum.c" "$GEM5_HOME/util/m5/build/x86/out/m5op_x86.o" \
  -o "$LAB/bin/vector_sum_fs_gcc"
```

Com Clang, o equivalente é:

```bash
clang -O2 -std=c11 -Wall -Wextra -static -DGEM5_M5OPS \
  -I"$GEM5_HOME/include" \
  "$LAB/src/vector_sum.c" "$GEM5_HOME/util/m5/build/x86/out/m5op_x86.o" \
  -o "$LAB/bin/vector_sum_fs_clang"
```

Valide os binários no host antes de simular:

```bash
"$LAB/bin/vector_sum_gcc"
"$LAB/bin/vector_sum_clang"
```

---

## Etapa 3 — Executar em SE pela linha de comando

O script legado `configs/example/se.py` aceita um executável e monta uma configuração SE básica. Consulte as opções disponíveis na sua versão:

```bash
"$GEM5_BIN" "$GEM5_HOME/configs/example/se.py" --help
```

Execute o binário GCC com uma CPU simples temporizada, duas caches privadas L1 e memória DDR3:

```bash
cd "$LAB"
"$GEM5_BIN" -d "$LAB/results/se-cli-gcc" \
  "$GEM5_HOME/configs/example/se.py" \
  --cmd="$LAB/bin/vector_sum_gcc" \
  --cpu-type=TimingSimpleCPU \
  --caches --l1d_size=32kB --l1i_size=32kB \
  --mem-type=DDR3_1600_8x8 --mem-size=512MB
```

Para comparar compiladores, execute uma segunda vez, sempre em outro diretório de saída:

```bash
"$GEM5_BIN" -d "$LAB/results/se-cli-clang" \
  "$GEM5_HOME/configs/example/se.py" \
  --cmd="$LAB/bin/vector_sum_clang" \
  --cpu-type=TimingSimpleCPU \
  --caches --l1d_size=32kB --l1i_size=32kB \
  --mem-type=DDR3_1600_8x8 --mem-size=512MB
```

A opção `-d` é importante: cada execução deve possuir diretório próprio, evitando sobrescrever `stats.txt`, `config.ini` e `simout`.

Confira o término:

```bash
tail -n 15 "$LAB/results/se-cli-gcc/simout"
grep -E '^(simTicks|simInsts|hostSeconds)' "$LAB/results/se-cli-gcc/stats.txt"
```

---

## Etapa 4 — Executar em SE pela API Python

Crie `configs/run_se.py`. Este script cria explicitamente a placa, CPU, caches, memória e carga de trabalho com a API Python do gem5.

```python
import argparse

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator

parser = argparse.ArgumentParser()
parser.add_argument("--binary", required=True, help="Caminho absoluto do binário x86-64")
args = parser.parse_args()

cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1d_size="32KiB",
    l1i_size="32KiB",
    l2_size="256KiB",
)

memory = SingleChannelDDR3_1600(size="512MiB")
processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING,
    isa=ISA.X86,
    num_cores=1,
)

board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

board.set_se_binary_workload(BinaryResource(local_path=args.binary))
simulator = Simulator(board=board)
simulator.run()
print(simulator.get_last_exit_event_cause())
```

Execute-o com o mesmo binário usado no teste anterior:

```bash
"$GEM5_BIN" -d "$LAB/results/se-python-gcc" \
  "$LAB/configs/run_se.py" \
  --binary "$LAB/bin/vector_sum_gcc"
```

A principal diferença é de controle: na linha de comando foi usado um script pronto do gem5; aqui, o script Python é seu e define a topologia. O comando `gem5.opt script.py` continua sendo a forma de iniciar o simulador.

---

## Etapa 5 — Preparar recursos para Full System

FS requer, no mínimo, uma imagem de disco Linux compatível com X86 e um kernel. É recomendável usar recursos oficiais do gem5, pois kernel, imagem e configuração devem ser compatíveis entre si.

Você precisa obter e registrar localmente:

```text
$LAB/resources/vmlinux
$LAB/resources/x86-linux.img
```

O kernel deve ser um `vmlinux` apropriado para o guest x86 e a imagem deve conter um Linux inicializável. Não use URLs ou imagens aleatórias sem verificar a compatibilidade com a versão do gem5.

### 5.1 Colocar o programa na imagem

Copie o binário FS para a imagem usando uma máquina virtual, um *loop mount* ou uma ferramenta como `guestfish`. O exemplo abaixo usa `guestfish`; ele pode requerer privilégios administrativos conforme o sistema:

```bash
cp "$LAB/resources/x86-linux.img" "$LAB/resources/x86-linux-vector-sum.img"
guestfish --rw -a "$LAB/resources/x86-linux-vector-sum.img" -i \
  copy-in "$LAB/bin/vector_sum_fs_gcc" /root/
```

Opcionalmente, copie também o executável `m5`, caso sua imagem não o contenha:

```bash
guestfish --rw -a "$LAB/resources/x86-linux-vector-sum.img" -i \
  copy-in "$GEM5_HOME/util/m5/build/x86/out/m5" /root/
```

Dentro do guest, o programa estará em `/root/vector_sum_fs_gcc`. Execute-o pelo terminal serial após o boot:

```bash
chmod +x /root/vector_sum_fs_gcc
/root/vector_sum_fs_gcc
```

Para automatizar, adicione um script `/root/run-vector-sum.sh` à imagem que contenha:

```sh
#!/bin/sh
/root/vector_sum_fs_gcc
/sbin/m5 exit
```

O `m5 exit` faz a simulação terminar; sem ele, o guest continuará em execução até outro evento de saída.

---

## Etapa 6 — Executar em FS pela linha de comando

O script legado `configs/example/fs.py` é uma forma direta de iniciar uma configuração FS. Primeiro, verifique a interface presente em sua versão:

```bash
"$GEM5_BIN" "$GEM5_HOME/configs/example/fs.py" --help
```

Inicie o guest com o kernel e a imagem preparados:

```bash
"$GEM5_BIN" -d "$LAB/results/fs-cli" \
  "$GEM5_HOME/configs/example/fs.py" \
  --kernel="$LAB/resources/vmlinux" \
  --disk-image="$LAB/resources/x86-linux-vector-sum.img" \
  --cpu-type=TimingSimpleCPU \
  --num-cpus=1 \
  --mem-size=2GB \
  --caches
```

Acompanhe o console em outro terminal:

```bash
tail -f "$LAB/results/fs-cli/system.pc.com_1.device"
```

Em algumas versões, o terminal serial aparece em arquivo com outro nome, como `system.terminal`. Liste o diretório de saída para encontrá-lo:

```bash
find "$LAB/results/fs-cli" -maxdepth 2 -type f | sort
```

Quando houver login no console, execute o programa manualmente ou deixe o script de boot executá-lo. O término esperado do gem5 é algo equivalente a `m5_exit instruction encountered`.

> **Tempo de simulação:** o boot de Linux em uma CPU detalhada pode ser muito lento. Para validar o fluxo, comece com `TimingSimpleCPU`; depois mantenha o mesmo kernel, imagem e workload e altere somente o modelo que está sendo estudado.

---

## Etapa 7 — Executar em FS pela API Python

Crie `configs/run_fs.py`. O script configura uma placa X86, associa recursos locais e inicia o sistema operacional convidado.

```python
import argparse

from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import DiskImageResource, KernelResource
from gem5.simulate.simulator import Simulator

parser = argparse.ArgumentParser()
parser.add_argument("--kernel", required=True, help="Caminho para vmlinux")
parser.add_argument("--disk-image", required=True, help="Caminho para a imagem de disco")
args = parser.parse_args()

cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1d_size="32KiB",
    l1i_size="32KiB",
    l2_size="256KiB",
)

memory = SingleChannelDDR3_1600(size="2GiB")
processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING,
    isa=ISA.X86,
    num_cores=1,
)

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

board.set_kernel_disk_workload(
    kernel=KernelResource(local_path=args.kernel),
    disk_image=DiskImageResource(local_path=args.disk_image),
)

simulator = Simulator(board=board)
simulator.run()
print(simulator.get_last_exit_event_cause())
```

Execute:

```bash
"$GEM5_BIN" -d "$LAB/results/fs-python" \
  "$LAB/configs/run_fs.py" \
  --kernel "$LAB/resources/vmlinux" \
  --disk-image "$LAB/resources/x86-linux-vector-sum.img"
```

A API moderna pode mudar nomes de componentes entre versões. Se um import falhar, consulte a documentação correspondente à versão instalada e substitua o componente pelo equivalente. A lógica não muda: criar processador, memória, hierarquia de cache e placa; associar kernel e disco; criar `Simulator`; chamar `run()`.

---

## Etapa 8 — Interpretar `stats.txt`

Ao terminar cada execução, o diretório indicado por `-d` contém principalmente:

| Arquivo | Uso |
|---|---|
| `stats.txt` | Contadores e métricas da simulação. |
| `config.ini` | Configuração efetivamente instanciada; essencial para reprodutibilidade. |
| `config.json` | Representação estruturada da configuração. |
| `simout` e `simerr` | Saída padrão e diagnósticos. |

Em FS, `stats.txt` pode conter **vários blocos** delimitados por `Begin Simulation Statistics` e `End Simulation Statistics`, especialmente se o guest executar `m5 resetstats`, `m5 dumpstats` ou se houver checkpoints. Não compare blocos diferentes por acidente.

### 8.1 Métricas básicas

Localize métricas globais:

```bash
grep -E '^(simTicks|simInsts|hostSeconds|finalTick)' \
  "$LAB/results/se-python-gcc/stats.txt"
```

Interpretação:

- `simTicks`: tempo simulado, em *ticks* do gem5. É uma medida de tempo do modelo, não tempo de relógio do computador hospedeiro.
- `simInsts`: quantidade de instruções simuladas; use-a para normalizar custos entre execuções comparáveis.
- `hostSeconds`: tempo real gasto pelo host para executar a simulação. Serve para avaliar custo experimental, não desempenho do programa simulado.
- `finalTick`: tick em que a simulação terminou.

### 8.2 CPI e IPC

Em estatísticas de uma CPU, procure campos de instruções e ciclos, por exemplo:

```bash
grep -E 'system\.cpu\.(numCycles|committedInsts|cpi|ipc)' \
  "$LAB/results/se-cli-gcc/stats.txt"
```

Quando `numCycles` e `committedInsts` estiverem disponíveis, calcule:

\[
\mathrm{CPI} = \frac{\mathrm{numCycles}}{\mathrm{committedInsts}}
\qquad\text{e}\qquad
\mathrm{IPC} = \frac{\mathrm{committedInsts}}{\mathrm{numCycles}}
\]

CPI menor ou IPC maior pode indicar melhor desempenho, mas só é uma comparação válida se ISA, binário, frequência, CPU, caches, memória e região medida forem iguais.

### 8.3 Miss rate de cache

Os nomes exatos dependem da hierarquia. Busque as estatísticas de cache:

```bash
grep -E 'system\.cache_hierarchy.*(overallHits|overallMisses|missRate)' \
  "$LAB/results/se-python-gcc/stats.txt"
```

Se só houver hits e misses, a taxa de faltas é:

\[
\mathrm{miss\ rate} = \frac{\mathrm{misses}}{\mathrm{hits} + \mathrm{misses}}
\]

Analise separadamente L1I, L1D e L2. Para este programa, o padrão de acesso sequencial tende a favorecer pré-busca e localidade espacial, mas vetores maiores que a cache ainda produzem faltas de capacidade.

### 8.4 Comparação responsável entre GCC e Clang

Para comparar compiladores, mantenha fixos o tamanho `N`, o modo (SE ou FS), a configuração de CPU/memória e a arquitetura. Compare pelo menos:

```bash
for d in se-cli-gcc se-cli-clang; do
  echo "===== $d ====="
  grep -E '^(simTicks|simInsts|hostSeconds)' "$LAB/results/$d/stats.txt"
done
```

Não conclua que um compilador é melhor apenas com `hostSeconds`: essa métrica mede a velocidade do host rodando o simulador. Priorize `simTicks`, ciclos, instruções comprometidas, CPI/IPC e métricas de cache. Confirme ainda que ambos os binários imprimiram o mesmo `checksum`.

---

## Checklist de reprodutibilidade

Antes de registrar ou publicar resultados, guarde:

- hash do commit e versão do gem5 (`git rev-parse HEAD`);
- comando completo ou script Python utilizado;
- compilador e flags (`gcc --version`, `clang --version`);
- hash dos binários, kernel e imagem de disco (`sha256sum`);
- `config.ini`, `config.json`, `stats.txt`, `simout` e `simerr`;
- tamanho de `N`, modo de execução e definição da ROI.

## Próximos experimentos

Repita primeiro o mesmo experimento alterando **uma variável por vez**: tamanho da L1, presença/tamanho da L2, tipo de CPU ou tamanho de `N`. Em FS, use `m5 resetstats` antes e `m5 dumpstats` após a região de interesse para separar o boot do Linux das estatísticas do programa.