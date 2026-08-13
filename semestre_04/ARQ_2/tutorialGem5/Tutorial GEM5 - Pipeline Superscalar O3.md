# Tutorial GEM5 — Pipeline Superscalar com O3CPU

## Introdução e objetivo

O `O3CPU` do gem5 modela uma CPU fora de ordem e permite explorar recursos de um pipeline superscalar. Neste tutorial, em **SE** e com a **API Python**, você variará largura de busca, despacho e retirada de instruções, além do tamanho do *Reorder Buffer* (ROB), para avaliar o impacto em IPC e ciclos.

## Pré-requisitos

- gem5 compilado: `build/X86/gem5.opt`;
- GCC e Python 3;
- repositório do gem5 como diretório atual.

## Etapa 1 — Criar o workload

Crie `workloads/ilp.c`:

```c
#include <stdio.h>

int main(void) {
    double a = 1.0, b = 2.0, c = 3.0, d = 4.0;
    for (long i = 0; i < 15000000L; i++) {
        a = a * 1.000001 + 0.1;
        b = b * 1.000003 + 0.2;
        c = c * 1.000005 + 0.3;
        d = d * 1.000007 + 0.4;
    }
    printf("%.3f\n", a + b + c + d);
    return 0;
}
```

Há quatro cadeias de dependência independentes, o que cria oportunidade de paralelismo no nível de instruções (ILP). Compile:

```bash
mkdir -p workloads
gcc -O2 -static workloads/ilp.c -o workloads/ilp
```

## Etapa 2 — Entender os parâmetros

| Parâmetro | Função |
|---|---|
| `fetchWidth` | máximo de instruções buscadas por ciclo |
| `decodeWidth` | máximo de instruções decodificadas por ciclo |
| `renameWidth` | máximo de instruções renomeadas por ciclo |
| `dispatchWidth` | máximo de instruções enviadas às filas por ciclo |
| `issueWidth` | máximo de instruções emitidas por ciclo |
| `commitWidth` | máximo de instruções retiradas por ciclo |
| `numROBEntries` | número de entradas do ROB |

Aumentar um único estágio pode não elevar o IPC se outro estágio se tornar gargalo. Por isso, o experimento inclui configurações equilibradas.

## Etapa 3 — Criar o script Python

Crie `configs/tutorials/pipeline_o3.py`:

```python
import argparse
import m5
from m5.objects import *

parser = argparse.ArgumentParser()
parser.add_argument("--cmd", required=True)
parser.add_argument("--width", type=int, default=4)
parser.add_argument("--rob", type=int, default=192)
args = parser.parse_args()

class L1Cache(Cache):
    size = "32KiB"
    assoc = 4
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 8
    tgts_per_mshr = 16

system = System()
system.clk_domain = SrcClockDomain(clock="2GHz", voltage_domain=VoltageDomain())
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]
system.cpu = DerivO3CPU()
system.cpu.fetchWidth = args.width
system.cpu.decodeWidth = args.width
system.cpu.renameWidth = args.width
system.cpu.dispatchWidth = args.width
system.cpu.issueWidth = args.width
system.cpu.commitWidth = args.width
system.cpu.numROBEntries = args.rob

system.membus = SystemXBar()
system.cpu.createInterruptController()
system.cpu.icache = L1Cache()
system.cpu.dcache = L1Cache()
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port
system.cpu.icache.mem_side = system.membus.cpu_side_ports
system.cpu.dcache.mem_side = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

system.workload = SEWorkload.init_compatible(args.cmd)
p = Process()
p.cmd = [args.cmd]
system.cpu.workload = p
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()
event = m5.simulate()
print("width=", args.width, "ROB=", args.rob)
print(event.getCause())
```

## Etapa 4 — Definir as experiências

| Nome | Largura | ROB | Hipótese |
|---|---:|---:|---|
| estreito | 2 | 64 | menor capacidade de explorar ILP |
| base | 4 | 192 | configuração intermediária |
| largo | 8 | 384 | maior potencial de vazão |
| ROB pequeno | 4 | 64 | janela de instruções limitada |

## Etapa 5 — Executar

```bash
for cfg in "estreito 2 64" "base 4 192" "largo 8 384" "rob_pequeno 4 64"; do
  set -- $cfg
  build/X86/gem5.opt --outdir="results/o3_$1" \
    configs/tutorials/pipeline_o3.py --cmd=workloads/ilp \
    --width="$2" --rob="$3"
done
```

## Etapa 6 — Avaliar os resultados

```bash
for d in results/o3_*; do
  echo "--- $d ---"
  grep -E "numCycles|numInsts|ipc" "$d/stats.txt"
done
```

Preencha:

| Configuração | Largura | ROB | Instruções | Ciclos | IPC |
|---|---:|---:|---:|---:|---:|
| estreito | 2 | 64 | — | — | — |
| base | 4 | 192 | — | — | — |
| largo | 8 | 384 | — | — | — |
| ROB pequeno | 4 | 64 | — | — | — |

O limite teórico de retirada é a largura de `commit`, porém o IPC real é limitado por dependências, latências, faltas de cache e erros de predição. Se o IPC não aumentar ao ampliar largura, procure indicadores de filas cheias, bloqueios e eventos de cache no `stats.txt`.

## Etapa 7 — Boas práticas experimentais

- Mude um parâmetro por vez quando a pergunta for causal;
- mantenha frequência, cache, memória e binário fixos;
- confirme valores em `config.ini`;
- use o mesmo ponto de término para todas as execuções;
- não trate uma configuração maior como necessariamente melhor: ela pode elevar área, energia e complexidade.

## Conclusão

Você parametrizou recursos centrais do pipeline O3 e relacionou a janela de instruções e a largura superscalar ao IPC. O estudo pode ser estendido variando filas de instruções, registradores físicos e unidades funcionais.