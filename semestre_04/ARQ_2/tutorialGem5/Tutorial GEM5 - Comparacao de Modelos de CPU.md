# Tutorial GEM5 — Comparação de Modelos de CPU

## Introdução e objetivo

O gem5 oferece modelos de CPU com diferentes níveis de detalhe. Este tutorial ensina a comparar `TimingSimpleCPU`, `MinorCPU` e `O3CPU` no modo **SE**, utilizando uma configuração construída pela **API Python**. O objetivo é identificar como a microarquitetura afeta ciclos, IPC e tempo simulado.

## Pré-requisitos

- gem5 x86 compilado: `build/X86/gem5.opt`;
- GCC e Python 3;
- execução a partir da raiz do gem5.

## Etapa 1 — Criar um workload computacional

Crie `workloads/calculo_numerico.c`:

```c
#include <stdio.h>

int main(void) {
    double x = 1.0, y = 1.000001;
    for (long i = 0; i < 20000000L; i++) {
        x = x * y + 0.25;
        y = y + 0.00000001;
    }
    printf("resultado=%.6f\n", x);
    return 0;
}
```

Compile-o:

```bash
mkdir -p workloads
gcc -O2 -static workloads/calculo_numerico.c -o workloads/calculo_numerico
```

## Etapa 2 — Escolher os modelos

| Modelo | Característica | Uso recomendado |
|---|---|---|
| `TimingSimpleCPU` | execução simples com temporização | referência de baixo custo |
| `MinorCPU` | pipeline in-order configurável | estudos de pipeline simples |
| `O3CPU` | execução fora de ordem | estudos de desempenho microarquitetural |

Não compare o tempo de execução no computador hospedeiro: compare as métricas simuladas. `O3CPU` costuma demandar mais tempo real para simular, mas representa recursos mais sofisticados.

## Etapa 3 — Criar o script Python

Crie `configs/tutorials/comparar_cpu.py`:

```python
import argparse
import m5
from m5.objects import *

parser = argparse.ArgumentParser()
parser.add_argument("--cmd", required=True)
parser.add_argument("--cpu", choices=["timing", "minor", "o3"], default="timing")
args = parser.parse_args()

cpu_classes = {
    "timing": TimingSimpleCPU,
    "minor": MinorCPU,
    "o3": DerivO3CPU,
}

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
system.cpu = cpu_classes[args.cpu]()
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
process = Process()
process.cmd = [args.cmd]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()
event = m5.simulate()
print("CPU:", args.cpu)
print("Fim:", event.getCause())
```

A mesma frequência, memória, caches e programa devem ser mantidos em todos os testes. Assim, o tipo de CPU é a única variável independente.

## Etapa 4 — Executar os testes

```bash
build/X86/gem5.opt --outdir=results/cpu_timing \
  configs/tutorials/comparar_cpu.py --cmd=workloads/calculo_numerico --cpu=timing

build/X86/gem5.opt --outdir=results/cpu_minor \
  configs/tutorials/comparar_cpu.py --cmd=workloads/calculo_numerico --cpu=minor

build/X86/gem5.opt --outdir=results/cpu_o3 \
  configs/tutorials/comparar_cpu.py --cmd=workloads/calculo_numerico --cpu=o3
```

## Etapa 5 — Coletar estatísticas

```bash
for d in results/cpu_*; do
  echo "--- $d ---"
  grep -E "simSeconds|numCycles|numInsts|ipc" "$d/stats.txt"
done
```

As métricas principais são:

| Métrica | Significado |
|---|---|
| `simSeconds` | tempo da máquina simulada |
| `system.cpu.numCycles` | número de ciclos |
| `system.cpu.numInsts` | instruções executadas |
| `system.cpu.ipc` | instruções por ciclo |

O IPC pode ser conferido por:

\[
IPC = \frac{\text{instruções}}{\text{ciclos}}
\]

Em geral, um modelo fora de ordem consegue esconder parte da latência de operações independentes. Isso não é garantido: programas dominados por dependências de dados ou faltas de memória podem ter ganho pequeno.

## Etapa 6 — Interpretar e documentar

| CPU | Instruções | Ciclos | IPC | Tempo simulado | Observação |
|---|---:|---:|---:|---:|---|
| Timing | — | — | — | — | referência |
| Minor | — | — | — | — | in-order |
| O3 | — | — | — | — | fora de ordem |

Verifique em `config.ini` se a CPU selecionada é a esperada. Também compare `simInsts` entre execuções: diferenças indicam que os workloads ou os pontos de término não foram equivalentes.

## Conclusão

Você comparou três modelos de CPU mantendo a plataforma fixa. O próximo passo é usar workloads com diferentes perfis — computação, acesso intenso à memória e desvios — para observar quando cada microarquitetura oferece vantagem.