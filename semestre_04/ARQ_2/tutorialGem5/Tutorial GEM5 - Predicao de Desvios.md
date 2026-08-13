# Tutorial GEM5 — Avaliação de Predição de Desvios

## Introdução e objetivo

Instruções condicionais podem interromper o fluxo do pipeline. Um preditor de desvios tenta antecipar o próximo caminho de execução; quando erra, o processador precisa recuperar o estado correto. Neste tutorial você comparará preditores de desvio no gem5 em **SE**, por meio de um script da **API Python**, usando `O3CPU`.

## Pré-requisitos

- `build/X86/gem5.opt` disponível;
- GCC e Python 3;
- diretório raiz do gem5.

## Etapa 1 — Criar um workload com desvios

Crie `workloads/desvios.c`:

```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    uint32_t estado = 123456789u;
    long soma = 0;
    for (long i = 0; i < 30000000L; i++) {
        estado = estado * 1664525u + 1013904223u;
        if (estado & 0x80000000u)
            soma += i;
        else
            soma -= i;
    }
    printf("soma=%ld\n", soma);
    return 0;
}
```

Esse gerador produz um padrão de decisão difícil de prever com precisão. Compile:

```bash
mkdir -p workloads
gcc -O2 -static workloads/desvios.c -o workloads/desvios
```

## Etapa 2 — Conceitos essenciais

| Resultado | Consequência |
|---|---|
| Predição correta | a CPU segue especulativamente pelo caminho certo |
| Predição incorreta | instruções especulativas são descartadas e há penalidade |

Uma forma de medir a qualidade é:

\[
\text{taxa de erros} = \frac{\text{mispredictions}}{\text{predições}}
\]

A redução da taxa de erros normalmente reduz ciclos, mas preditores mais complexos podem consumir mais armazenamento e energia em hardware real.

## Etapa 3 — Criar o script de simulação

Crie `configs/tutorials/predicao_desvios.py`:

```python
import argparse
import m5
from m5.objects import *

parser = argparse.ArgumentParser()
parser.add_argument("--cmd", required=True)
parser.add_argument("--predictor", choices=["local", "tournament", "bimode"], default="tournament")
args = parser.parse_args()

predictors = {
    "local": LocalBP,
    "tournament": TournamentBP,
    "bimode": BiModeBP,
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
system.cpu = DerivO3CPU()
system.cpu.branchPred = predictors[args.predictor]()
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
print("Preditor:", args.predictor)
print(event.getCause())
```

## Etapa 4 — Executar a campanha

```bash
for p in local tournament bimode; do
  build/X86/gem5.opt --outdir="results/bp_$p" \
    configs/tutorials/predicao_desvios.py \
    --cmd=workloads/desvios --predictor="$p"
done
```

## Etapa 5 — Encontrar métricas de predição

Os nomes variam entre versões e preditores. Primeiro localize as linhas disponíveis:

```bash
grep -inE "branch|mispred|incorrect|condPred" results/bp_tournament/stats.txt | head -50
```

Depois colete, quando presentes, campos como `condPredicted`, `condIncorrect`, `BTBLookups` e `BTBHits`, além de `system.cpu.numCycles` e `system.cpu.ipc`.

> Não compare métricas com nomes parecidos sem verificar a descrição e a unidade na versão do gem5 usada. Alguns contadores incluem apenas desvios condicionais; outros abrangem mais tipos de controle.

## Etapa 6 — Construir a análise

| Preditor | Predições condicionais | Erros condicionais | Taxa de erro | Ciclos | IPC |
|---|---:|---:|---:|---:|---:|
| Local | — | — | — | — | — |
| Tournament | — | — | — | — | — |
| BiMode | — | — | — | — | — |

Calcule a taxa de erro em uma planilha ou script:

\[
\text{taxa de erro (\%)} = 100 \times \frac{\text{erros}}{\text{predições}}
\]

Se o preditor com menos erros não tiver menos ciclos, investigue outros gargalos: cache, dependências de dados, largura do pipeline ou custo de desvios indiretos.

## Etapa 7 — Experimentar padrões diferentes

Altere apenas o corpo do programa para criar: (a) desvio sempre tomado, (b) padrão alternado, e (c) padrão dependente de um vetor. Recompile e repita a campanha. Um bom preditor para um padrão pode não ser o melhor para outro.

## Conclusão

Você configurou o preditor como parâmetro da CPU, realizou execuções controladas e relacionou taxa de erros com IPC e ciclos. Para resultados rigorosos, guarde o commit do gem5, opções do compilador, binário, `config.ini` e `stats.txt` de cada execução.