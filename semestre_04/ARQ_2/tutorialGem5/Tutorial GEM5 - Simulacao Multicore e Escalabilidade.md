# Tutorial GEM5 — Simulação Multicore e Escalabilidade

## Introdução

Aumentar o número de núcleos não garante aumento proporcional de desempenho. Partes seriais, sincronização, comunicação e pressão sobre a memória limitam o ganho de aplicações paralelas. O gem5 permite controlar a configuração multicore e observar esses efeitos com estatísticas detalhadas.

## Objetivo

Este tutorial ensina a avaliar a escalabilidade de uma aplicação paralela em modo **SE**, usando uma configuração criada pela **API Python**. Ao final, você poderá:

- implementar uma aplicação paralela baseada em OpenMP;
- compilar o programa para a ISA x86;
- configurar 1, 2, 4 e 8 núcleos no gem5;
- coletar ciclos, IPC, faltas de cache e speedup;
- interpretar limites de escalabilidade.

> **Pré-requisitos:** gem5 compilado para `X86`, GCC com suporte a OpenMP, Python 3 e ambiente Linux. Este tutorial usa modo SE; a aplicação usa threads de usuário e requer suporte compatível no binário e no ambiente do gem5.

---

## 1. Conceitos fundamentais

### 1.1 Speedup e eficiência

Para um problema de tamanho fixo, o speedup com $p$ núcleos é:

\[
S(p) = \frac{T(1)}{T(p)}
\]

A eficiência é:

\[
E(p) = \frac{S(p)}{p}
\]

Valores de eficiência abaixo de 1 são esperados. Eles refletem overhead de criação/sincronização de threads, regiões seriais e disputa por recursos.

### 1.2 Lei de Amdahl

Se $f$ é a fração serial do programa, o limite teórico do speedup é:

\[
S(p) \leq \frac{1}{f + \frac{1-f}{p}}
\]

O experimento real também inclui efeitos de cache e de memória, que podem reduzir ainda mais o resultado.

---

## 2. Etapa prática 1 — Preparar o diretório

```bash
mkdir -p experiments/escalabilidade/{src,bin,configs,resultados}
cd experiments/escalabilidade
```

---

## 3. Etapa prática 2 — Implementar uma soma de redução paralela

Crie `src/reducao_omp.c`:

```c
#include <omp.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N (1UL << 25)

int main(void) {
    int *v = malloc(N * sizeof(int));
    if (v == NULL) return 1;

    for (unsigned long i = 0; i < N; i++)
        v[i] = (int)(i % 97);

    uint64_t soma = 0;

    #pragma omp parallel for reduction(+:soma) schedule(static)
    for (unsigned long i = 0; i < N; i++)
        soma += (uint64_t)v[i] * (uint64_t)(v[i] + 3);

    printf("threads=%d soma=%llu\n", omp_get_max_threads(),
           (unsigned long long)soma);
    free(v);
    return 0;
}
```

O vetor é inicializado sequencialmente e a redução é paralela. A inicialização representa uma parcela serial deliberada, útil para observar a Lei de Amdahl.

---

## 4. Etapa prática 3 — Compilar

```bash
gcc -O2 -fopenmp -static -o bin/reducao_omp src/reducao_omp.c
file bin/reducao_omp
```

Antes de simular, valide no host:

```bash
OMP_NUM_THREADS=2 ./bin/reducao_omp
```

> Dependendo da distribuição e da versão do compilador, a vinculação estática de OpenMP pode não estar disponível. Nesse caso, use vinculação dinâmica e forneça as bibliotecas necessárias, ou utilize uma implementação com `pthread` apropriada ao seu ambiente SE.

---

## 5. Etapa prática 4 — Criar o script de simulação

Crie `configs/multicore.py`:

```python
import argparse
import m5
from m5.objects import *

parser = argparse.ArgumentParser()
parser.add_argument("--num-cpus", type=int, required=True)
parser.add_argument("--cmd", required=True)
parser.add_argument("--threads", type=int, required=True)
args = parser.parse_args()

if args.threads > args.num_cpus:
    parser.error("Use no máximo uma thread de trabalho por CPU simulado")

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "2GHz"
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("1GiB")]

system.cpu = [TimingSimpleCPU(cpu_id=i) for i in range(args.num_cpus)]
system.membus = SystemXBar()

# L1 privadas. A memória principal é compartilhada.
for cpu in system.cpu:
    cpu.icache = Cache(size="32KiB", assoc=4, tag_latency=1,
                       data_latency=1, response_latency=1,
                       mshrs=4, tgts_per_mshr=20)
    cpu.dcache = Cache(size="32KiB", assoc=4, tag_latency=1,
                       data_latency=1, response_latency=1,
                       mshrs=4, tgts_per_mshr=20)
    cpu.icache.cpu_side = cpu.icache_port
    cpu.dcache.cpu_side = cpu.dcache_port
    cpu.icache.mem_side = system.membus.cpu_side_ports
    cpu.dcache.mem_side = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

process = Process()
process.cmd = [args.cmd]
process.env = ["OMP_NUM_THREADS=" + str(args.threads),
               "OMP_DYNAMIC=FALSE"]

# O mesmo processo multithread é inicializado na CPU 0.
# As threads podem ser distribuídas pelos CPUs pelo suporte de threading do SE.
system.cpu[0].workload = process
system.cpu[0].createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()
event = m5.simulate()
print("Fim:", event.getCause(), "tick:", m5.curTick())
```

### Observação importante sobre threads em SE

O comportamento de aplicações multithread em SE depende da ISA, do modelo de CPU, da versão do gem5 e do suporte a clonagem de threads. Se sua versão não executar OpenMP adequadamente, não interprete resultados incompletos como dados de escalabilidade. Valide primeiro a criação das threads no `simout` e consulte a documentação da sua versão. Uma alternativa é executar processos independentes, como no tutorial de multiprogramação, mas isso mede throughput e não speedup de uma única aplicação paralela.

---

## 6. Etapa prática 5 — Executar a campanha

A partir da raiz do gem5:

```bash
for n in 1 2 4 8; do
  build/X86/gem5.opt \
    --outdir=experiments/escalabilidade/resultados/n${n} \
    experiments/escalabilidade/configs/multicore.py \
    --num-cpus=${n} \
    --threads=${n} \
    --cmd=experiments/escalabilidade/bin/reducao_omp
done
```

Cada experimento deve usar o mesmo binário, tamanho de problema, frequência, cache e memória. O único parâmetro que muda é o número de CPUs e threads.

---

## 7. Etapa prática 6 — Consolidar resultados

Crie `extrair_resultados.sh`:

```bash
#!/usr/bin/env bash
printf "nucleos,sim_seconds,sim_insts,ipc_cpu0,miss_l1d_cpu0\n"
for n in 1 2 4 8; do
  f="resultados/n${n}/stats.txt"
  tempo=$(awk '$1=="simSeconds" {print $2}' "$f")
  inst=$(awk '$1=="simInsts" {print $2}' "$f")
  ipc=$(awk '$1=="system.cpu0.ipc" {print $2}' "$f")
  miss=$(awk '$1=="system.cpu0.dcache.overallMissRate::total" {print $2}' "$f")
  printf "%s,%s,%s,%s,%s\n" "$n" "$tempo" "$inst" "$ipc" "$miss"
done
```

Execute:

```bash
chmod +x extrair_resultados.sh
./extrair_resultados.sh > resultados.csv
cat resultados.csv
```

Complete uma tabela de análise com o tempo de cada execução e calcule $S(p)$ e $E(p)$ usando o tempo de 1 núcleo como referência.

| Núcleos | Tempo $T(p)$ | Speedup $S(p)$ | Eficiência $E(p)$ |
|---:|---:|---:|---:|
| 1 | $T(1)$ | 1,00 | 1,00 |
| 2 |  |  |  |
| 4 |  |  |  |
| 8 |  |  |  |

---

## 8. Interpretação dos resultados

Um speedup inferior ao ideal não é, por si só, um erro. Verifique:

- se o `simout` informa o número de threads esperado;
- se o trabalho foi realmente distribuído entre CPUs;
- se a soma final é idêntica em todas as execuções;
- se o tráfego e as faltas de cache aumentam com o número de núcleos;
- se há saturação da memória compartilhada.

O aumento de IPC em um núcleo não mede, sozinho, escalabilidade. A métrica central é o tempo total para a **mesma quantidade de trabalho**, complementado por estatísticas de cada CPU e da memória.

---

## 9. Exercícios

1. Mude `schedule(static)` para `schedule(dynamic, 1024)` e compare overhead e balanceamento.
2. Aumente o tamanho do vetor para deslocar o conjunto de trabalho além das caches.
3. Acrescente uma L2 compartilhada ao sistema e avalie a mudança no speedup.
4. Varie a frequência da CPU sem alterar a DRAM. O gargalo se desloca para a memória?
5. Estime a fração serial pela Lei de Amdahl a partir de dois ou mais pontos medidos.

## Conclusão

Você estruturou uma campanha multicore com uma carga paralela, uma configuração Python parametrizada e métricas de speedup e eficiência. A validade dos resultados depende da confirmação de que a biblioteca de threads funciona no seu ambiente SE e de que todas as execuções realizam a mesma quantidade de trabalho.
