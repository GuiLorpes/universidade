# Tutorial GEM5 — Modelagem de Memória DDR

## Introdução e objetivo

A memória principal é um componente decisivo quando o conjunto de dados não cabe em cache. Neste tutorial, você configurará modelos DDR no gem5 usando **SE** e **API Python**, executará um workload com alta pressão de memória e analisará latência, largura de banda e tráfego.

## Pré-requisitos

- gem5 x86 compilado (`build/X86/gem5.opt`);
- GCC e Python 3;
- execução na raiz do repositório.

## Etapa 1 — Criar um programa sensível à memória

Crie `workloads/stream_memoria.c`:

```c
#include <stdio.h>
#include <stdlib.h>

#ifndef N
#define N (16 * 1024 * 1024)
#endif

int main(void) {
    int *a = malloc((size_t)N * sizeof(int));
    int *b = malloc((size_t)N * sizeof(int));
    if (!a || !b) return 1;

    for (int i = 0; i < N; i++) a[i] = i;
    for (int r = 0; r < 8; r++)
        for (int i = 0; i < N; i++) b[i] = a[i] + r;

    printf("ultimo=%d\n", b[N - 1]);
    free(a); free(b);
    return 0;
}
```

Compile:

```bash
mkdir -p workloads
gcc -O2 -static workloads/stream_memoria.c -o workloads/stream_memoria
```

O conjunto de dados é muito maior que a L1 e L2 propostas; portanto, uma parcela relevante dos acessos alcançará a DRAM.

## Etapa 2 — Escolher modelos de memória

O gem5 oferece diversos modelos de DRAM. Neste exemplo serão usados `DDR3_1600_8x8` e `DDR4_2400_8x8`. A disponibilidade exata depende da versão; liste os controladores em `src/mem/DRAMInterface.py` ou consulte a configuração produzida.

| Modelo | Uso no experimento |
|---|---|
| `DDR3_1600_8x8` | base |
| `DDR4_2400_8x8` | alternativa com parâmetros diferentes |

A troca de modelo não reproduz automaticamente um sistema físico completo: topologia, canais, controladores e carga de trabalho precisam ser coerentes com a pergunta de pesquisa.

## Etapa 3 — Criar o arquivo Python

Crie `configs/tutorials/memoria_ddr.py`:

```python
import argparse
import m5
from m5.objects import *

parser = argparse.ArgumentParser()
parser.add_argument("--cmd", required=True)
parser.add_argument("--dram", choices=["ddr3", "ddr4"], default="ddr3")
args = parser.parse_args()

dram_classes = {
    "ddr3": DDR3_1600_8x8,
    "ddr4": DDR4_2400_8x8,
}

class L1Cache(Cache):
    size = "32KiB"
    assoc = 4
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 16
    tgts_per_mshr = 16

system = System()
system.clk_domain = SrcClockDomain(clock="2GHz", voltage_domain=VoltageDomain())
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("1GiB")]
system.cpu = TimingSimpleCPU()
system.membus = SystemXBar()
system.cpu.createInterruptController()

system.cpu.icache = L1Cache()
system.cpu.dcache = L1Cache()
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port
system.cpu.icache.mem_side = system.membus.cpu_side_ports
system.cpu.dcache.mem_side = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = dram_classes[args.dram]()
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
print("DRAM:", args.dram)
print(event.getCause())
```

## Etapa 4 — Executar as simulações

```bash
build/X86/gem5.opt --outdir=results/ddr3 \
  configs/tutorials/memoria_ddr.py --cmd=workloads/stream_memoria --dram=ddr3

build/X86/gem5.opt --outdir=results/ddr4 \
  configs/tutorials/memoria_ddr.py --cmd=workloads/stream_memoria --dram=ddr4
```

## Etapa 5 — Localizar estatísticas de memória

```bash
grep -inE "mem_ctrl|dram|bandwidth|latency|bytesRead|bytesWritten" results/ddr3/stats.txt | head -80
```

Em muitas versões, estatísticas relevantes incluem médias de latência de leitura/escrita, bytes lidos/escritos, número de requisições e utilização do controlador. Como nomes e hierarquias variam, localize primeiro a seção da sua execução e registre os campos usados.

Também colete:

```bash
grep -E "simSeconds|numCycles|overallMissRate" results/ddr3/stats.txt
```

## Etapa 6 — Calcular métricas derivadas

Caso `bytesRead` esteja disponível, uma aproximação da largura de banda média é:

\[
BW_{leitura} = \frac{\text{bytesRead}}{\text{simSeconds}}
\]

Caso os resultados sejam fornecidos em *ticks*, converta-os usando a frequência de *tick* registrada em `stats.txt` ou em `config.ini`. Não misture unidades.

Registre:

| Configuração | Ciclos | Tempo simulado | Latência média de leitura | Bytes lidos | Largura de banda média |
|---|---:|---:|---:|---:|---:|
| DDR3 | — | — | — | — | — |
| DDR4 | — | — | — | — | — |

## Etapa 7 — Interpretar limites do experimento

Se a taxa de faltas de L1 for baixa, as diferenças entre DRAMs serão pouco visíveis. Para aumentar a sensibilidade, reduza o tamanho de cache, aumente o conjunto de dados ou use acessos com menor localidade. Mantenha essas mudanças documentadas e iguais entre as alternativas.

## Conclusão

Você comparou modelos DDR em uma plataforma SE controlada. A análise correta associa comportamento da DRAM ao tráfego que realmente chegou a ela, e não apenas ao tempo total de simulação. Experimentos seguintes podem explorar múltiplos controladores, diferentes políticas de escalonamento e cargas concorrentes.