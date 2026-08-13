# Tutorial GEM5 — DVFS e Gerenciamento Dinâmico de Frequência

## Introdução

DVFS (*Dynamic Voltage and Frequency Scaling*) é uma técnica de gerenciamento que altera a frequência e, em plataformas que a suportam, a tensão de componentes durante a execução. Em gem5, a frequência pode ser representada por domínios de clock. Este tutorial avalia o efeito de diferentes frequências de CPU sobre tempo simulado, IPC e consumo energético estimado.

> **Nota:** alterar somente a frequência no gem5 não constitui um modelo elétrico completo de DVFS. A tensão e a energia devem ser avaliadas com modelos apropriados, como McPAT, e com premissas explicitadas.

## Objetivo

Construir uma campanha em **System Call Emulation (SE)** e pela **API Python** para comparar configurações de 1 GHz, 2 GHz e 3 GHz usando a mesma aplicação, coletar métricas e interpretar a relação desempenho–energia.

## Pré-requisitos

- gem5 compilado para a ISA escolhida; exemplos usam `X86`;
- Python 3;
- um binário x86-64 compatível com o modo SE;
- conhecimento básico de `stats.txt`.

```bash
cd ~/gem5
scons build/X86/gem5.opt -j"$(nproc)"
mkdir -p workloads scripts resultados
```

## Etapa 1 — Criar a carga de trabalho

Use um programa com trabalho computacional suficiente para reduzir ruído de inicialização.

```c
// workloads/dvfs_workload.c
#include <stdint.h>
#include <stdio.h>

int main(void) {
    uint64_t x = 0x12345678ULL;
    for (uint64_t i = 0; i < 200000000ULL; i++) {
        x = (x * 1664525ULL + 1013904223ULL) ^ (x >> 13);
    }
    printf("resultado=%llu\n", (unsigned long long)x);
    return 0;
}
```

Compile estaticamente quando a instalação permitir:

```bash
gcc -O2 -static -o workloads/dvfs_workload workloads/dvfs_workload.c
```

## Etapa 2 — Entender as métricas

Para uma quantidade fixa de instruções, o número de ciclos depende sobretudo da microarquitetura; o tempo simulado depende do período de clock:

\[
T = \frac{Ciclos}{Frequência}
\]

O IPC é dado por:

\[
IPC = \frac{Instruções\ executadas}{Ciclos}
\]

Portanto, ao manter a mesma CPU e memória, aumentar a frequência normalmente reduz `simSeconds`, mas não necessariamente aumenta o IPC.

## Etapa 3 — Criar o script de simulação Python

Crie `scripts/dvfs_se.py`:

```python
import argparse
import m5
from m5.objects import *

parser = argparse.ArgumentParser()
parser.add_argument("--binary", required=True)
parser.add_argument("--freq", default="2GHz")
args = parser.parse_args()

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = args.freq
system.clk_domain.voltage_domain = VoltageDomain(voltage="1.0V")
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]

system.cpu = O3CPU()
system.cpu.icache = Cache(size="32KiB", assoc=8, tag_latency=1,
                          data_latency=1, response_latency=1,
                          mshrs=16, tgts_per_mshr=20)
system.cpu.dcache = Cache(size="32KiB", assoc=8, tag_latency=1,
                          data_latency=1, response_latency=1,
                          mshrs=16, tgts_per_mshr=20)
system.l2 = Cache(size="1MiB", assoc=16, tag_latency=10,
                  data_latency=10, response_latency=10,
                  mshrs=32, tgts_per_mshr=20)

system.membus = SystemXBar()
system.l2bus = L2XBar()
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports
system.l2.cpu_side = system.l2bus.mem_side_ports
system.l2.mem_side = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

process = Process()
process.cmd = [args.binary]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()
print(f"Iniciando SE: frequencia={args.freq}")
exit_event = m5.simulate()
print(f"Fim: {exit_event.getCause()} em tick {m5.curTick()}")
```

## Etapa 4 — Executar as configurações

Execute cada caso em um diretório exclusivo:

```bash
for f in 1GHz 2GHz 3GHz; do
  build/X86/gem5.opt --outdir=resultados/$f scripts/dvfs_se.py \
    --binary=workloads/dvfs_workload --freq=$f
 done
```

Antes de comparar, confirme que a aplicação terminou normalmente em todos os arquivos `simout`.

## Etapa 5 — Coletar estatísticas

```bash
for f in 1GHz 2GHz 3GHz; do
  echo "=== $f ==="
  grep -E "simSeconds|system.cpu.numCycles|system.cpu.committedInsts|system.cpu.ipc" \
    resultados/$f/stats.txt
 done
```

Registre os resultados em uma tabela:

| Frequência | Ciclos | Instruções | IPC | Tempo simulado |
|---|---:|---:|---:|---:|
| 1 GHz | | | | |
| 2 GHz | | | | |
| 3 GHz | | | | |

## Etapa 6 — Estimar energia de forma responsável

Uma aproximação conceitual para potência dinâmica é:

\[
P_{dinâmica} \propto C \cdot V^2 \cdot f
\]

E energia é aproximadamente `potência × tempo`. Não preencha valores de energia apenas a partir dessa fórmula: exporte a configuração para uma ferramenta energética, mantenha as mesmas premissas de tecnologia e documente tensão, frequência e modelo usados. O tutorial de integração com McPAT pode ser usado como complemento.

## Interpretação

- Se os ciclos e o IPC permanecerem parecidos, a mudança de `simSeconds` será principalmente consequência da frequência.
- Se o IPC mudar, verifique se há parâmetros dependentes de clock ou gargalos de memória modelados em domínios diferentes.
- O menor tempo simulado não implica automaticamente menor energia.
- Relate também tempo de execução do **host**, que mede custo da simulação e não desempenho do sistema modelado.

## Exercícios

1. Repita o experimento com `TimingSimpleCPU` e compare a sensibilidade à frequência.
2. Configure o domínio da memória separadamente e estude CPU rápida com DRAM fixa.
3. Acrescente uma opção `--voltage` ao script e prepare dados de entrada para uma estimativa energética externa.

## Conclusão

Você criou uma campanha reprodutível para estudar frequência em SE. A separação entre ciclos, tempo simulado, IPC e energia estimada evita conclusões incorretas sobre DVFS.