# Tutorial gem5: modo SE com API Python

## Introdução

O modo **System-call Emulation (SE)** executa um programa de usuário sem iniciar um sistema operacional completo. O gem5 cria o processo simulado e emula as chamadas de sistema necessárias, como abertura de arquivos, leitura, escrita e encerramento. Isso permite estudar CPU, caches e memória com uma configuração mais simples e mais rápida que o modo Full System.

Este tutorial ensina, passo a passo, a montar um arquivo Python usando a **API padrão (gem5 standard library)** para executar uma simulação em modo SE. O exemplo usa a ISA **X86** e um executável local chamado `contagem_ocorrencias`.

> O modo SE não é adequado para estudar boot, kernel, drivers, interrupções de dispositivos ou aplicações que dependem de serviços completos do sistema operacional. Para esses casos, use Full System.

## Objetivo

Ao final, você terá:

1. um programa de usuário compilado para X86;
2. um arquivo `se_contagem.py` que descreve a plataforma simulada;
3. uma execução SE iniciada pela API Python;
4. um diretório de saída com `stats.txt`, `config.ini` e `config.json`;
5. uma base para variar CPU, caches, memória e argumentos do programa.

---

# Parte prática

## Etapa 1 — Preparar o gem5

Os comandos abaixo consideram Linux, o repositório do gem5 em `~/gem5` e a ISA X86. Ajuste os caminhos se necessário.

```bash
cd ~/gem5
scons build/X86/gem5.opt -j"$(nproc)"
```

Confirme que o binário foi criado:

```bash
./build/X86/gem5.opt --version
```

O sufixo `.opt` é apropriado para experimentos: possui otimizações e mantém verificações úteis. Evite `gem5.fast` durante o desenvolvimento, pois erros de configuração podem ficar menos visíveis.

## Etapa 2 — Criar a área do experimento

Crie diretórios para código-fonte, binários, configurações e resultados.

```bash
mkdir -p ~/gem5-experimentos/se-python/{src,bin,configs,resultados}
cd ~/gem5-experimentos/se-python
```

A estrutura será:

```text
se-python/
├── bin/
│   └── contagem_ocorrencias
├── configs/
│   └── se_contagem.py
├── resultados/
└── src/
    └── contagem_ocorrencias.c
```

## Etapa 3 — Implementar o programa de exemplo

Crie `src/contagem_ocorrencias.c`:

```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    const unsigned long tamanho = (argc > 1) ? strtoul(argv[1], NULL, 10) : 1000000UL;
    const unsigned long intervalo = 1024UL;
    unsigned long *dados = malloc(tamanho * sizeof(unsigned long));

    if (dados == NULL) {
        fprintf(stderr, "Falha ao alocar memoria.\n");
        return 1;
    }

    for (unsigned long i = 0; i < tamanho; i++) {
        dados[i] = (i * 17UL + 13UL) % intervalo;
    }

    unsigned long alvo = 37UL;
    unsigned long ocorrencias = 0;

    for (unsigned long i = 0; i < tamanho; i++) {
        if (dados[i] == alvo) {
            ocorrencias++;
        }
    }

    printf("tamanho=%lu alvo=%lu ocorrencias=%lu\n", tamanho, alvo, ocorrencias);
    free(dados);
    return 0;
}
```

O programa inicializa um vetor e faz uma varredura sequencial para contar o número de ocorrências de um valor. O tamanho do vetor é recebido como primeiro argumento. Ele é útil para observar o impacto de caches porque realiza um volume controlável de acessos à memória.

## Etapa 4 — Compilar o executável

Compile-o para a mesma ISA do binário do gem5, neste caso X86.

```bash
cd ~/gem5-experimentos/se-python
gcc -O2 -Wall -Wextra src/contagem_ocorrencias.c -o bin/contagem_ocorrencias
```

Teste no computador hospedeiro antes da simulação:

```bash
./bin/contagem_ocorrencias 10000
```

Resultado esperado, com o valor exato de ocorrências determinado pelo padrão de inicialização:

```text
tamanho=10000 alvo=37 ocorrencias=10
```

Verifique a arquitetura do binário:

```bash
file bin/contagem_ocorrencias
```

Em uma máquina X86-64, a saída deve indicar um executável ELF `x86-64`. Para usar ARM, RISC-V ou outra ISA, é necessário compilar o programa com o compilador cruzado apropriado e gerar o binário correspondente à ISA selecionada no gem5.

## Etapa 5 — Entender o arquivo Python de configuração

O script Python cria os objetos que compõem a plataforma simulada e os conecta. A sequência essencial é:

1. importar as classes da API;
2. criar a hierarquia de cache;
3. criar o controlador de memória;
4. escolher CPU e ISA;
5. criar a placa (`board`) e definir clock;
6. associar o binário ao workload SE;
7. criar o simulador e chamar `run()`.

A API do gem5 substitui a montagem manual de muitos objetos internos. A `board` atua como o ponto central que reúne processador, cache, memória e workload.

## Etapa 6 — Criar o arquivo Python

Crie `configs/se_contagem.py` com o conteúdo completo abaixo.

```python
"""Simulação SE de contagem de ocorrências usando a API Python do gem5."""

import argparse
from pathlib import Path

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator


parser = argparse.ArgumentParser(
    description="Executa contagem_ocorrencias em modo SE no gem5."
)
parser.add_argument(
    "--binary",
    required=True,
    help="Caminho para o executável X86 a simular.",
)
parser.add_argument(
    "--tamanho",
    type=int,
    default=1_000_000,
    help="Número de elementos do vetor usado pelo programa.",
)
parser.add_argument(
    "--cpu",
    choices=["timing", "atomic"],
    default="timing",
    help="Modelo de CPU: timing (padrão) ou atomic.",
)
args = parser.parse_args()

binary_path = Path(args.binary).resolve()
if not binary_path.is_file():
    raise FileNotFoundError(f"Executável não encontrado: {binary_path}")

# (1) Hierarquia clássica privada: L1 de instruções, L1 de dados e L2 por núcleo.
cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1i_size="32KiB",
    l1d_size="32KiB",
    l2_size="256KiB",
)

# (2) Memória principal: um canal DDR3-1600 com 512 MiB de capacidade.
memory = SingleChannelDDR3_1600(size="512MiB")

# (3) Processador simples de um núcleo para ISA X86.
# TimingSimpleCPU modela atrasos de acesso à memória; AtomicSimpleCPU é mais rápido,
# mas não é indicado para medir desempenho detalhado de cache.
cpu_type = CPUTypes.TIMING if args.cpu == "timing" else CPUTypes.ATOMIC
processor = SimpleProcessor(
    cpu_type=cpu_type,
    isa=ISA.X86,
    num_cores=1,
)

# (4) A placa conecta CPU, caches e memória. O clock é de 3 GHz.
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# (5) Workload SE: binário local e argumento enviado ao main().
board.set_se_binary_workload(
    binary=BinaryResource(local_path=str(binary_path)),
    arguments=[str(args.tamanho)],
)

# (6) Constrói a simulação e executa até o programa finalizar.
simulator = Simulator(board=board)
simulator.run()

print("Simulação encerrada.")
print(f"Causa de saída: {simulator.get_last_exit_event_cause()}")
print(f"Tick final: {simulator.get_current_tick()}")
```

## Etapa 7 — Examinar cada bloco do script

### 7.1 Argumentos externos

`argparse` permite variar o executável, o tamanho do problema e o tipo de CPU sem editar o arquivo. Por exemplo, `--tamanho 4000000` se transforma no argumento recebido por `main(int argc, char *argv[])`.

O uso de `Path(...).resolve()` transforma o caminho em absoluto. Isso evita que o gem5 deixe de localizar o binário quando o script é executado a partir de outro diretório.

### 7.2 Hierarquia de cache

`PrivateL1PrivateL2CacheHierarchy` cria, para cada núcleo:

- uma L1 de instruções (`l1i_size`);
- uma L1 de dados (`l1d_size`);
- uma L2 privada (`l2_size`).

Como há um núcleo, o experimento terá uma L1I, uma L1D e uma L2. A escolha de `32KiB/32KiB/256KiB` é apenas um ponto de partida. Cada execução deve registrar esses parâmetros para que comparações sejam justas.

### 7.3 Memória

`SingleChannelDDR3_1600(size="512MiB")` fornece uma memória DDR3 com canal único. A capacidade deve acomodar o processo e seus dados. Para o vetor de 1.000.000 elementos, são aproximadamente 8 MiB quando `unsigned long` ocupa 8 bytes, portanto 512 MiB é suficiente.

### 7.4 CPU

`SimpleProcessor` cria CPUs simples. Neste tutorial:

| Valor de `--cpu` | Tipo usado | Uso recomendado |
|---|---|---|
| `timing` | `TimingSimpleCPU` | Experimentos que consideram latência e hierarquia de memória. |
| `atomic` | `AtomicSimpleCPU` | Testes funcionais e exploração rápida; não use para conclusões detalhadas de desempenho. |

O processador recebe `ISA.X86`, que precisa ser compatível com o binário do gem5 (`build/X86/gem5.opt`) e com o executável informado em `--binary`.

### 7.5 Workload SE

A chamada abaixo é a parte que define o modo SE:

```python
board.set_se_binary_workload(
    binary=BinaryResource(local_path=str(binary_path)),
    arguments=[str(args.tamanho)],
)
```

`BinaryResource` aponta para um arquivo executável local. O gem5 cria um processo simulado para esse binário e fornece os argumentos. Não há kernel nem imagem de disco nessa configuração.

## Etapa 8 — Executar a simulação

Execute a partir da raiz do repositório do gem5. O parâmetro `-d` define um diretório exclusivo para os arquivos de saída.

```bash
cd ~/gem5
./build/X86/gem5.opt \
  -d ~/gem5-experimentos/se-python/resultados/se-1m-timing \
  ~/gem5-experimentos/se-python/configs/se_contagem.py \
  --binary ~/gem5-experimentos/se-python/bin/contagem_ocorrencias \
  --tamanho 1000000 \
  --cpu timing
```

A saída textual do programa deverá incluir uma linha semelhante a:

```text
tamanho=1000000 alvo=37 ocorrencias=977
```

A simulação foi bem-sucedida quando a causa de saída informar que o processo terminou, geralmente com texto semelhante a `exiting with last active thread context`.

> A linha com `ocorrencias` depende da fórmula do programa e do tamanho. O principal é confirmar que o programa atingiu o fim e que o valor é consistente entre execuções com a mesma entrada.

## Etapa 9 — Localizar e validar os resultados

Liste os arquivos produzidos:

```bash
ls ~/gem5-experimentos/se-python/resultados/se-1m-timing
```

Os principais são:

| Arquivo | Finalidade |
|---|---|
| `stats.txt` | Estatísticas numéricas da simulação. |
| `config.ini` | Configuração efetiva, em formato legível. |
| `config.json` | Configuração efetiva, em JSON. |
| `simout` | Saída padrão do programa simulado. |
| `simerr` | Saída de erro do programa simulado. |

Verifique a causa final e alguns contadores:

```bash
grep -E "sim_exit|simTicks|simInsts|numCycles" \
  ~/gem5-experimentos/se-python/resultados/se-1m-timing/stats.txt
```

Os nomes podem variar entre versões e modelos de CPU. Para localizar estatísticas de cache, use:

```bash
grep -E "dcache.*(overallHits|overallMisses)|l2.*(overallHits|overallMisses)" \
  ~/gem5-experimentos/se-python/resultados/se-1m-timing/stats.txt
```

## Etapa 10 — Interpretar `stats.txt`

Comece confirmando o término normal e depois observe tempo, instruções e memória.

### Tempo simulado e instruções

Procure estatísticas como:

- `simTicks`: tempo simulado em ticks;
- `simInsts`: instruções executadas, quando disponível no modelo;
- `system.cpu.numCycles`: ciclos do processador;
- `system.cpu.committedInsts`: instruções comprometidas, comum em alguns modelos de CPU.

Não compare diretamente ticks de configurações que usam relógios diferentes. Para um único processador, quando estiverem disponíveis ciclos e instruções, o CPI pode ser calculado por:

\[
CPI = \frac{\text{numCycles}}{\text{instruções}}
\]

Sempre anote qual contador de instruções foi utilizado, pois os nomes e a disponibilidade variam por CPU.

### Taxa de faltas de cache

Para uma cache, a taxa de faltas é:

\[
\text{miss rate} = \frac{\text{misses}}{\text{hits} + \text{misses}}
\]

Se `stats.txt` trouxer `overallHits::total` e `overallMisses::total` para a L1D, use esses dois valores. O programa varre o vetor sequencialmente: uma L1D pequena tende a apresentar faltas compulsórias ao percorrer linhas de cache novas, enquanto uma L2 maior pode atender parte dessas faltas sem acesso à memória principal.

## Etapa 11 — Fazer um experimento controlado

O primeiro experimento pode comparar dois tamanhos de entrada, mantendo todo o restante idêntico.

```bash
cd ~/gem5

./build/X86/gem5.opt \
  -d ~/gem5-experimentos/se-python/resultados/se-1m \
  ~/gem5-experimentos/se-python/configs/se_contagem.py \
  --binary ~/gem5-experimentos/se-python/bin/contagem_ocorrencias \
  --tamanho 1000000 --cpu timing

./build/X86/gem5.opt \
  -d ~/gem5-experimentos/se-python/resultados/se-8m \
  ~/gem5-experimentos/se-python/configs/se_contagem.py \
  --binary ~/gem5-experimentos/se-python/bin/contagem_ocorrencias \
  --tamanho 8000000 --cpu timing
```

Para interpretar a comparação:

1. confirme que ambos os programas terminaram normalmente;
2. compare `simTicks` e ciclos, se disponíveis;
3. compare hits e misses da L1D e L2;
4. mantenha a mesma versão do gem5, clock, CPU, caches e flags de compilação;
5. não atribua uma diferença a um único fator sem verificar os contadores correspondentes.

## Etapa 12 — Variações úteis no script

### Alterar o clock

Edite apenas este valor:

```python
clk_freq="3GHz"
```

Ao variar frequência, o tempo em ticks pode mudar. Avalie ciclos e instruções para separar mudanças de microarquitetura de mudanças de clock.

### Alterar tamanhos de cache

Por exemplo, para L1D de 64 KiB e L2 de 1 MiB:

```python
cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1i_size="32KiB",
    l1d_size="64KiB",
    l2_size="1MiB",
)
```

Use diretórios de saída diferentes para cada configuração e registre os parâmetros no nome ou em uma planilha de experimentos.

### Trocar para execução funcional rápida

```bash
--cpu atomic
```

Use essa opção para confirmar que o programa e os argumentos funcionam. Retorne a `--cpu timing` antes de realizar análise de desempenho da memória.

## Etapa 13 — Problemas frequentes

### `ModuleNotFoundError: No module named 'gem5'`

Execute o script através do binário `gem5.opt`, não com `python3` diretamente:

```bash
./build/X86/gem5.opt caminho/para/se_contagem.py ...
```

O binário prepara o ambiente necessário para importar a API do gem5.

### Executável não encontrado

Confira o valor após `--binary`, as permissões e a existência do arquivo:

```bash
ls -l ~/gem5-experimentos/se-python/bin/contagem_ocorrencias
```

### Erro de ISA ou formato ELF

Use um executável X86 com `build/X86/gem5.opt`. Se o executável foi compilado para ARM ou RISC-V, construa o gem5 para a mesma ISA e ajuste `isa=ISA.X86` no script.

### Falta de memória simulada

Aumente a capacidade do objeto de memória, por exemplo:

```python
memory = SingleChannelDDR3_1600(size="1GiB")
```

### Diretório de saída já existe ou mistura resultados

Nunca reutilize um diretório para experimentos diferentes. Defina um novo caminho com `-d` em cada execução.

---

## Checklist final

- [ ] O gem5 foi compilado para X86.
- [ ] O programa foi compilado para X86 e executa fora do simulador.
- [ ] O arquivo Python importa os componentes da API do gem5.
- [ ] `SimpleBoard` recebeu processador, memória e hierarquia de cache.
- [ ] `set_se_binary_workload()` recebeu o binário e os argumentos.
- [ ] A execução foi iniciada com `build/X86/gem5.opt`.
- [ ] A causa de saída indica término normal.
- [ ] `stats.txt` foi analisado em um diretório exclusivo de resultados.

## Próximos passos

Como extensão, crie cópias do script para testar diferentes tamanhos de L1D e L2, ou substitua `SimpleProcessor` por um processador mais detalhado quando a versão do gem5 e o objetivo do estudo justificarem isso. Em todos os casos, altere uma variável por vez e registre a configuração efetiva junto dos resultados.