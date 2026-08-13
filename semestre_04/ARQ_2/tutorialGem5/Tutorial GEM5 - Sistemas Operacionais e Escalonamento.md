# Tutorial GEM5 — Sistemas Operacionais e Escalonamento de Processos

## Introdução

O escalonador do sistema operacional decide qual tarefa executa em cada CPU e por quanto tempo. Esse mecanismo é observado de modo mais fiel em **Full System (FS)**, pois há kernel, temporizadores, interrupções e processos reais. Em contraste, o modo SE emula chamadas de sistema para processos, mas não inicializa um SO completo.

## Objetivo

Preparar um experimento FS com Linux para observar concorrência entre cargas CPU-bound, registrar troca de contexto e comparar afinidade de CPU. O tutorial usa API Python para configurar a plataforma e comandos no terminal do sistema convidado para controlar as tarefas.

## Pré-requisitos

- gem5 compilado para ARM ou X86;
- kernel e imagem de disco Linux compatíveis com a ISA;
- recursos de FS disponíveis localmente;
- pelo menos 2 núcleos simulados para o experimento de afinidade.

Exemplo de build ARM:

```bash
cd ~/gem5
scons build/ARM/gem5.opt -j"$(nproc)"
```

## Etapa 1 — Entender as métricas do SO

| Conceito | Como observar no convidado |
|---|---|
| Troca de contexto | `/proc/<pid>/status`, `pidstat -w`, `perf stat` |
| Migração entre CPUs | `ps -o psr`, `perf stat` |
| Afinidade | `taskset -p` |
| Tempo de CPU | `time`, `/usr/bin/time`, `pidstat` |
| Carga do sistema | `uptime`, `/proc/loadavg` |

A disponibilidade de `perf`, `pidstat` e `taskset` depende da imagem Linux. Instale `procps`, `sysstat` e `util-linux` na imagem quando necessário.

## Etapa 2 — Criar uma carga de trabalho

No sistema convidado, salve `cpu_bound.c`:

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    uint64_t n = argc > 1 ? strtoull(argv[1], NULL, 10) : 800000000ULL;
    volatile uint64_t x = 1;
    for (uint64_t i = 0; i < n; i++) x = x * 2862933555777941757ULL + 3037000493ULL;
    printf("pid=%d resultado=%llu\n", getpid(), (unsigned long long)x);
    return 0;
}
```

Inclua `#include <unistd.h>` para `getpid()` e compile no convidado:

```bash
gcc -O2 -o cpu_bound cpu_bound.c
```

Alternativamente, compile no host com um compilador cruzado e copie o binário para a imagem.

## Etapa 3 — Criar a configuração FS em Python

As imagens e classes de placa variam de acordo com a distribuição e a versão do gem5. O padrão abaixo usa a biblioteca de componentes; adapte os caminhos de recursos ao seu ambiente.

```python
# scripts/fs_escalonamento.py
from gem5.components.boards.arm_board import ArmBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import PrivateL1PrivateL2CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

cache = PrivateL1PrivateL2CacheHierarchy(
    l1d_size="32KiB", l1i_size="32KiB", l2_size="1MiB"
)
processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, isa=ISA.ARM, num_cores=2)
board = ArmBoard(
    clk_freq="2GHz", processor=processor, memory=SingleChannelDDR3_1600("1GiB"),
    cache_hierarchy=cache,
    release=obtain_resource("arm64-linux-kernel-5.10.110"),
    platform=obtain_resource("VExpress_GEM5_V1"),
)
board.set_kernel_disk_workload(
    kernel=obtain_resource("arm64-linux-kernel-5.10.110"),
    disk_image=obtain_resource("arm64-ubuntu-20.04-img"),
    readfile_contents="echo 'Pronto para experimento de escalonamento'"
)
Simulator(board=board).run()
```

> Identificadores de recursos são exemplos. Liste os recursos disponíveis na instalação e use kernel, disco e placa compatíveis. Para X86, utilize uma placa e recursos X86 equivalentes.

## Etapa 4 — Inicializar a simulação

```bash
build/ARM/gem5.opt --outdir=resultados/fs_base scripts/fs_escalonamento.py
```

Conecte-se ao terminal serial indicado na saída. Após o boot, confirme a contagem de CPUs:

```bash
nproc
lscpu
```

## Etapa 5 — Executar sem afinidade

No convidado:

```bash
./cpu_bound 500000000 &
./cpu_bound 500000000 &
wait
```

Para observar trocas de contexto, execute durante a carga:

```bash
pidstat -w 1
```

Anote PIDs, CPU reportada por `ps -o pid,psr,comm -C cpu_bound` e tempos de conclusão.

## Etapa 6 — Executar com afinidade

Fixe as duas tarefas em CPUs diferentes:

```bash
taskset -c 0 ./cpu_bound 500000000 &
taskset -c 1 ./cpu_bound 500000000 &
wait
```

Depois, provoque competição no mesmo núcleo:

```bash
taskset -c 0 ./cpu_bound 500000000 &
taskset -c 0 ./cpu_bound 500000000 &
wait
```

## Etapa 7 — Coletar resultados

No host, examine `stats.txt` ao fim da simulação; no convidado, guarde saídas de `time`, `pidstat` e `/proc`. Compare sempre o mesmo intervalo de simulação e as mesmas entradas.

| Cenário | CPUs disponíveis | Afinidade | Tempo das tarefas | Trocas de contexto |
|---|---:|---|---:|---:|
| Base | 2 | livre | | |
| Separado | 2 | CPU 0 e 1 | | |
| Contenção | 2 | ambas CPU 0 | | |

## Interpretação

- Afinidade em CPUs distintas tende a reduzir competição por tempo de CPU, mas caches compartilhadas e memória ainda podem causar interferência.
- Duas tarefas em um mesmo núcleo devem dividir o processador e apresentar mais preempções.
- Não atribua toda diferença ao escalonador sem controlar frequência, cache, prioridade, entradas e atividade do sistema.

## Exercícios

1. Execute três tarefas em dois núcleos e observe o aumento de competição.
2. Compare `nice -n 10` com prioridade padrão em uma carga concorrente.
3. Use uma carga intensiva em memória e compare seu comportamento com `cpu_bound`.

## Conclusão

O modo FS permite estudar escalonamento como fenômeno de sistema. A combinação de controles no convidado e estatísticas do gem5 cria uma base para experimentos de afinidade, concorrência e interferência.