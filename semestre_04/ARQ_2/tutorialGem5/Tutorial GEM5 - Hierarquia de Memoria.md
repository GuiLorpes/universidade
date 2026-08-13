# Tutorial GEM5 — Hierarquia de Memória

## Introdução e objetivo

A hierarquia de memória determina como o processador acessa instruções e dados: registradores, caches, memória principal e interconexões possuem custos e capacidades diferentes. Neste tutorial será montada, no modo **System Call Emulation (SE)** e pela **API Python do gem5**, uma plataforma com caches L1 e L2 para comparar configurações de capacidade, associatividade e latência.

Ao final, você será capaz de criar um script de simulação, executar um programa e interpretar estatísticas de cache em `stats.txt`.

## Pré-requisitos

- gem5 compilado para a ISA escolhida. Os exemplos usam x86: `build/X86/gem5.opt`;
- Python 3 e compilador C;
- diretório raiz do repositório do gem5 como diretório de trabalho.

> Para outra ISA, compile o programa e substitua o binário do gem5 de forma coerente, por exemplo `build/ARM/gem5.opt`.

## Etapa 1 — Criar a aplicação de teste

Crie `workloads/acesso_memoria.c`:

```c
#include <stdio.h>
#include <stdlib.h>

#ifndef N
#define N (1 << 20)
#endif

int main(void) {
    int *v = malloc(N * sizeof(int));
    if (!v) return 1;

    long long soma = 0;
    for (int r = 0; r < 20; r++) {
        for (int i = 0; i < N; i++) v[i] = i + r;
        for (int i = 0; i < N; i += 16) soma += v[i];
    }
    printf("soma=%lld\n", soma);
    free(v);
    return 0;
}
```

O segundo laço usa passo 16 e provoca acessos não totalmente sequenciais, úteis para observar faltas de cache.

Compile para x86:

```bash
mkdir -p workloads
 gcc -O2 -static workloads/acesso_memoria.c -o workloads/acesso_memoria
```

Se a distribuição não fornecer bibliotecas estáticas, remova `-static` e informe as bibliotecas necessárias ao processo SE quando aplicável.

## Etapa 2 — Entender a configuração

A configuração terá:

| Componente | Papel inicial |
|---|---|
| `TimingSimpleCPU` | CPU que considera atrasos de memória |
| L1I | Cache de instruções privada |
| L1D | Cache de dados privada |
| L2 | Cache unificada compartilhada pelo núcleo |
| `SystemXBar` | Interconexão entre CPU, caches e memória |
| `DDR3_1600_8x8` | Modelo de memória principal |

A relação de capacidade é desejavelmente crescente: L1 pequena e rápida; L2 maior e mais lenta; DRAM ainda maior e muito mais lenta.

## Etapa 3 — Montar o arquivo Python

Crie `configs/tutorials/hierarquia_memoria.py`:

```python
import m5
from m5.objects import *
from m5.util import addToPath
from common import ObjectList
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cmd", required=True, help="Executável do workload")
parser.add_argument("--l1-size", default="32KiB")
parser.add_argument("--l1-assoc", type=int, default=4)
parser.add_argument("--l2-size", default="512KiB")
parser.add_argument("--l2-assoc", type=int, default=8)
args = parser.parse_args()

class L1ICache(Cache):
    size = args.l1_size
    assoc = args.l1_assoc
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 20

class L1DCache(Cache):
    size = args.l1_size
    assoc = args.l1_assoc
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 20

class L2Cache(Cache):
    size = args.l2_size
    assoc = args.l2_assoc
    tag_latency = 10
    data_latency = 10
    response_latency = 1
    mshrs = 20
    tgts_per_mshr = 12

system = System()
system.clk_domain = SrcClockDomain(clock="2GHz", voltage_domain=VoltageDomain())
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]

system.cpu = TimingSimpleCPU()
system.membus = SystemXBar()
system.cpu.createInterruptController()
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port

system.l2bus = L2XBar()
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports
system.l2cache = L2Cache()
system.l2cache.cpu_side = system.l2bus.mem_side_ports
system.l2cache.mem_side = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

system.workload = SEWorkload.init_compatible(args.cmd)
process = Process()
process.cmd = [args.cmd]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()
print("Iniciando simulacao")
exit_event = m5.simulate()
print("Fim em", m5.curTick(), "porque", exit_event.getCause())
```

O argumento `--cmd` torna o script reutilizável. `mem_mode = "timing"` é essencial: sem ele, os atrasos de cache não influenciam o tempo simulado de forma representativa.

## Etapa 4 — Executar a configuração-base

```bash
build/X86/gem5.opt --outdir=results/base \
  configs/tutorials/hierarquia_memoria.py \
  --cmd=workloads/acesso_memoria
```

Os arquivos principais estarão em `results/base/`:

- `config.ini`: parâmetros efetivamente usados;
- `stats.txt`: contadores e métricas;
- `simout` e `simerr`: saída padrão e diagnósticos.

## Etapa 5 — Comparar experiências

Execute cada experimento em diretório separado:

```bash
build/X86/gem5.opt --outdir=results/l1_16k \
  configs/tutorials/hierarquia_memoria.py --cmd=workloads/acesso_memoria \
  --l1-size=16KiB --l1-assoc=2

build/X86/gem5.opt --outdir=results/l1_64k \
  configs/tutorials/hierarquia_memoria.py --cmd=workloads/acesso_memoria \
  --l1-size=64KiB --l1-assoc=8

build/X86/gem5.opt --outdir=results/l2_2m \
  configs/tutorials/hierarquia_memoria.py --cmd=workloads/acesso_memoria \
  --l2-size=2MiB --l2-assoc=16
```

Altere **uma variável por vez** ao comparar resultados. Caso contrário, não será possível atribuir a mudança de desempenho a um parâmetro específico.

## Etapa 6 — Examinar `stats.txt`

Use:

```bash
grep -E "simSeconds|system.cpu.numCycles|overallMissRate|overallAccesses" results/base/stats.txt
```

Métricas importantes:

| Métrica | Interpretação |
|---|---|
| `simSeconds` | tempo simulado total |
| `system.cpu.numCycles` | ciclos executados pela CPU |
| `system.cpu.dcache.overallMissRate::total` | fração de acessos à L1D que faltaram |
| `system.l2cache.overallMissRate::total` | fração de acessos que faltaram na L2 |
| `system.l2cache.overallAccesses::total` | tráfego que chegou à L2 |

Os nomes podem variar discretamente entre versões. Localize a seção desejada com `grep -i "dcache" results/base/stats.txt`.

A taxa de faltas é:

\[
\text{miss rate} = \frac{\text{misses}}{\text{accesses}}
\]

Uma L1 maior normalmente reduz faltas de capacidade, mas pode exigir mais área e energia em uma implementação real. Associatividade maior tende a reduzir faltas por conflito, com possível aumento de latência e complexidade.

## Etapa 7 — Registrar uma tabela comparativa

Preencha uma tabela como esta a partir de seus resultados:

| Experimento | L1D | Associatividade L1D | L2 | Ciclos | Miss rate L1D | Miss rate L2 |
|---|---:|---:|---:|---:|---:|---:|
| Base | 32 KiB | 4 | 512 KiB | — | — | — |
| L1 pequena | 16 KiB | 2 | 512 KiB | — | — | — |
| L1 grande | 64 KiB | 8 | 512 KiB | — | — | — |
| L2 grande | 32 KiB | 4 | 2 MiB | — | — | — |

## Conclusão

Você montou uma hierarquia L1–L2 no modo SE, parametrizou capacidade e associatividade pela API Python e comparou métricas de desempenho. Em estudos mais completos, varie também tamanho de linha, latências, número de MSHRs e política de substituição, mantendo fixos workload, compilador, otimização e frequência.