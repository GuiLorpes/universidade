# Tutorial GEM5 — Workloads de Inteligência Artificial

## Introdução

Cargas de inteligência artificial podem apresentar grande volume de operações aritméticas e acessos regulares ou irregulares à memória. Antes de usar frameworks complexos, um kernel de inferência simples permite isolar efeitos de cache, tamanho de dados e microarquitetura.

## Objetivo

Criar e simular, no modo **SE** com **API Python**, uma camada totalmente conectada (*fully connected*) com ReLU. Avaliar como tamanho de cache e dimensão do problema afetam ciclos, IPC e faltas de cache.

## Pré-requisitos

```bash
cd ~/gem5
scons build/X86/gem5.opt -j"$(nproc)"
mkdir -p workloads scripts resultados
```

## Etapa 1 — Implementar o kernel de inferência

A operação computa:

\[
y_j = \max\left(0, b_j + \sum_{i=0}^{N-1} x_i W_{j,i}\right)
\]

Crie `workloads/camada_fc.c`:

```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    int n = argc > 1 ? atoi(argv[1]) : 512;
    float *x = malloc((size_t)n * sizeof(float));
    float *w = malloc((size_t)n * n * sizeof(float));
    float *b = malloc((size_t)n * sizeof(float));
    float *y = malloc((size_t)n * sizeof(float));
    if (!x || !w || !b || !y) return 1;

    for (int i = 0; i < n; i++) {
        x[i] = (float)(i % 31) / 31.0f;
        b[i] = (float)(i % 7) - 3.0f;
    }
    for (int j = 0; j < n; j++)
        for (int i = 0; i < n; i++)
            w[(size_t)j * n + i] = (float)((i + j) % 19) / 19.0f;

    for (int j = 0; j < n; j++) {
        float acc = b[j];
        for (int i = 0; i < n; i++) acc += x[i] * w[(size_t)j * n + i];
        y[j] = acc > 0.0f ? acc : 0.0f;
    }

    double soma = 0;
    for (int j = 0; j < n; j++) soma += y[j];
    printf("n=%d soma=%f\n", n, soma);
    free(x); free(w); free(b); free(y);
    return 0;
}
```

Compile sem vetorização automática para estabelecer uma linha de base arquitetural mais simples:

```bash
gcc -O2 -fno-tree-vectorize -static -o workloads/camada_fc workloads/camada_fc.c
```

> Remova `-fno-tree-vectorize` em uma segunda campanha caso sua ISA e CPU simulada suportem as instruções geradas. Valide o binário antes de simular.

## Etapa 2 — Planejar a campanha

| Fator | Valores |
|---|---|
| Dimensão `n` | 128, 512, 1024 |
| Cache L2 | 256 KiB, 1 MiB, 4 MiB |
| CPU | O3CPU, fixa |
| Frequência | 2 GHz, fixa |

Altere apenas um fator por vez quando o objetivo for atribuir causalidade.

## Etapa 3 — Criar o script Python

Salve como `scripts/ia_se.py`:

```python
import argparse
import m5
from m5.objects import *

p = argparse.ArgumentParser()
p.add_argument("--binary", required=True)
p.add_argument("--n", required=True)
p.add_argument("--l2", default="1MiB")
a = p.parse_args()

system = System()
system.clk_domain = SrcClockDomain(clock="2GHz", voltage_domain=VoltageDomain())
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("1GiB")]
system.cpu = O3CPU()

system.cpu.icache = Cache(size="32KiB", assoc=8, tag_latency=1, data_latency=1,
                          response_latency=1, mshrs=16, tgts_per_mshr=20)
system.cpu.dcache = Cache(size="32KiB", assoc=8, tag_latency=1, data_latency=1,
                          response_latency=1, mshrs=16, tgts_per_mshr=20)
system.l2 = Cache(size=a.l2, assoc=16, tag_latency=12, data_latency=12,
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
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

process = Process(cmd=[a.binary, a.n])
system.cpu.workload = process
system.cpu.createThreads()
root = Root(full_system=False, system=system)
m5.instantiate()
print(m5.simulate().getCause())
```

## Etapa 4 — Executar a matriz de experimentos

```bash
for n in 128 512 1024; do
  for l2 in 256KiB 1MiB 4MiB; do
    out="resultados/n${n}_l2${l2}"
    build/X86/gem5.opt --outdir="$out" scripts/ia_se.py \
      --binary=workloads/camada_fc --n="$n" --l2="$l2"
  done
done
```

Cada diretório deve conter `config.ini`, `simout` e `stats.txt`. Verifique o checksum impresso em `simout`; resultados numéricos iguais indicam que as configurações executaram a mesma computação.

## Etapa 5 — Extrair dados

```bash
for d in resultados/*; do
  echo "=== $d ==="
  grep -E "simSeconds|system.cpu.numCycles|system.cpu.ipc|system.l2.overallMissRate" \
    "$d/stats.txt"
done
```

Se `overallMissRate` não estiver presente, procure no `stats.txt` os contadores de acessos e faltas da L2 e calcule:

\[
Taxa\ de\ faltas = \frac{Faltas}{Acessos}
\]

## Etapa 6 — Interpretar os resultados

- `n=128` pode caber em caches; aumentar L2 tende a ter efeito pequeno.
- `n=1024` usa uma matriz de pesos maior e pode apresentar mais pressão na L2 e DRAM.
- Uma L2 maior pode reduzir faltas, mas também pode aumentar latência de acesso; avalie ciclos e IPC, não apenas a taxa de faltas.
- Este kernel é CPU-only. Ele não representa execução em GPU, acelerador tensorial ou framework completo de IA.

## Exercícios

1. Meça uma versão com duas camadas totalmente conectadas.
2. Reordene os laços e compare localidade de memória.
3. Compare `TimingSimpleCPU` e `O3CPU` mantendo todas as demais configurações.
4. Aplique quantização simples com inteiros de 8 bits e discuta efeitos sobre capacidade de cache.

## Conclusão

Você construiu uma carga de inferência controlada para correlacionar tamanho de dados, hierarquia de cache e desempenho. O mesmo método pode ser estendido a convoluções, atenção e outros kernels, desde que o modelo e as métricas sejam documentados.