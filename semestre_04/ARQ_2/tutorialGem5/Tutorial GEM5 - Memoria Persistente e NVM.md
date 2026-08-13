# Tutorial GEM5 — Memória Persistente e NVM

## Introdução

Memórias não voláteis (NVM), como PCM, STT-MRAM e tecnologias persistentes, retêm dados sem alimentação e podem apresentar latência, largura de banda e custos de escrita diferentes da DRAM. O gem5 permite modelar parâmetros de controladores e dispositivos de memória para investigar seus efeitos arquiteturais.

## Objetivo

Executar uma aplicação em **SE**, configurada pela **API Python**, e comparar uma memória DRAM de referência com uma memória de maior latência, usada como aproximação controlada de um dispositivo NVM. O foco é analisar desempenho; persistência funcional exige software e modelos específicos.

## Pré-requisitos

```bash
cd ~/gem5
scons build/X86/gem5.opt -j"$(nproc)"
mkdir -p workloads scripts resultados
```

## Etapa 1 — Implementar uma carga sensível à memória

O programa percorre um vetor grande com leituras e escritas. Ajuste `N` de acordo com a memória disponível no host.

```c
// workloads/memoria_nvm.c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N (32 * 1024 * 1024)

int main(void) {
    uint32_t *v = malloc((size_t)N * sizeof(*v));
    if (!v) return 1;

    for (size_t i = 0; i < N; i++) v[i] = (uint32_t)i;
    for (int r = 0; r < 4; r++) {
        for (size_t i = 0; i < N; i += 16)
            v[i] = v[i] * 1664525u + 1013904223u;
    }
    printf("checksum=%u\n", v[N - 16]);
    free(v);
    return 0;
}
```

```bash
gcc -O2 -static -o workloads/memoria_nvm workloads/memoria_nvm.c
```

## Etapa 2 — Definir as hipóteses

| Caso | Tecnologia representada | Latência | Objetivo |
|---|---|---:|---|
| `dram` | DRAM de referência | menor | estabelecer baseline |
| `nvm` | NVM simplificada | maior | observar impacto de acessos lentos |

A comparação é válida apenas se CPU, caches, binário e entrada forem idênticos.

## Etapa 3 — Criar o script Python

Crie `scripts/nvm_se.py`:

```python
import argparse
import m5
from m5.objects import *

parser = argparse.ArgumentParser()
parser.add_argument("--binary", required=True)
parser.add_argument("--memory", choices=["dram", "nvm"], default="dram")
args = parser.parse_args()

system = System()
system.clk_domain = SrcClockDomain(clock="2GHz", voltage_domain=VoltageDomain())
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]
system.cpu = O3CPU()

system.cpu.icache = Cache(size="32KiB", assoc=8, tag_latency=1, data_latency=1,
                          response_latency=1, mshrs=16, tgts_per_mshr=20)
system.cpu.dcache = Cache(size="32KiB", assoc=8, tag_latency=1, data_latency=1,
                          response_latency=1, mshrs=16, tgts_per_mshr=20)
system.l2 = Cache(size="1MiB", assoc=16, tag_latency=12, data_latency=12,
                  response_latency=12, mshrs=32, tgts_per_mshr=20)
system.l2bus = L2XBar()
system.membus = SystemXBar()
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports
system.l2.cpu_side = system.l2bus.mem_side_ports
system.l2.mem_side = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
if args.memory == "dram":
    system.mem_ctrl.dram = DDR3_1600_8x8()
else:
    # Modelo didático: NVM aproximada por timings mais altos.
    # Não representa fielmente uma tecnologia persistente específica.
    system.mem_ctrl.dram = DDR3_1600_8x8()
    system.mem_ctrl.dram.tCL = "60ns"
    system.mem_ctrl.dram.tRCD = "60ns"
    system.mem_ctrl.dram.tRP = "60ns"
    system.mem_ctrl.dram.tBURST = "10ns"

system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

process = Process(cmd=[args.binary])
system.cpu.workload = process
system.cpu.createThreads()
root = Root(full_system=False, system=system)
m5.instantiate()
print("Memoria:", args.memory)
print(m5.simulate().getCause())
```

> Os nomes e parâmetros disponíveis podem variar entre versões do gem5. Consulte `src/mem/DRAMInterface.py` da sua árvore de fontes e valide a configuração pelo arquivo `config.ini`.

## Etapa 4 — Executar os casos

```bash
for caso in dram nvm; do
  build/X86/gem5.opt --outdir=resultados/$caso scripts/nvm_se.py \
    --binary=workloads/memoria_nvm --memory=$caso
done
```

## Etapa 5 — Validar a configuração

```bash
grep -E "tCL|tRCD|tRP|tBURST" resultados/nvm/config.ini
grep -E "tCL|tRCD|tRP|tBURST" resultados/dram/config.ini
```

Não avance para a interpretação se os parâmetros observados não forem os desejados.

## Etapa 6 — Extrair métricas

```bash
for caso in dram nvm; do
  echo "=== $caso ==="
  grep -E "simSeconds|system.cpu.numCycles|system.cpu.ipc|mem_ctrl.*(readReqs|writeReqs|avgMemAccLat)" \
    resultados/$caso/stats.txt
done
```

Métricas disponíveis dependem da versão. Procure por `mem_ctrl` e por `system.l2` no `stats.txt` antes de automatizar a coleta.

## Interpretação

- Maior latência da memória deve aumentar tempo de execução ou reduzir IPC quando há faltas que chegam à memória.
- Se os resultados quase não mudarem, o conjunto de trabalho pode caber em caches; aumente `N`, reduza a L2 ou use acesso menos local.
- Escritas em NVM podem exigir modelo de largura de banda, fila e energia específico; não conclua durabilidade apenas por alterar timings.

## Exercícios

1. Separe os testes em leitura predominante e escrita predominante.
2. Compare L2 de 256 KiB, 1 MiB e 4 MiB nos dois casos.
3. Registre taxa de faltas de L2 e relacione-a à latência média observada.

## Conclusão

O experimento fornece uma forma controlada de medir a sensibilidade de uma aplicação à latência de memória. Para conclusões sobre uma NVM real, substitua a aproximação didática por parâmetros validados da tecnologia e declare as limitações do modelo.