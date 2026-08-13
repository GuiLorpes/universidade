# Tutorial GEM5 — Multiprogramação no Modo SE

## Introdução

O modo **System-call Emulation (SE)** do gem5 permite executar aplicações de espaço de usuário sem inicializar um sistema operacional completo. Embora não modele o escalonador de um kernel real, ele permite simular múltiplos processos e observar a competição por núcleos, caches, interconexão e memória.

## Objetivo

Ao final, você deverá ser capaz de:

- compilar duas aplicações independentes para a ISA simulada;
- criar um script Python que inicia múltiplas cargas de trabalho em SE;
- associar processos a núcleos simulados;
- executar cenários isolados e concorrentes;
- comparar tempo simulado, instruções, IPC e faltas de cache.

> **Pré-requisitos:** gem5 compilado para `X86`, Python 3, compilador C/C++ e noções básicas de modo SE. Os comandos assumem a raiz do repositório como diretório atual.

---

## 1. Conceitos fundamentais

### 1.1 Processo, núcleo e contexto

No gem5, uma carga de trabalho SE é representada por um objeto `Process`. O processo é atribuído a um `CPU` por meio da lista `workload`. Com dois objetos de CPU e dois processos, é possível executar um processo por núcleo.

Isso **não equivale** a reproduzir o comportamento completo de um sistema operacional: chamadas de sistema são emuladas e não há escalonamento de kernel, interrupções ou isolamento de processos como em Full System (FS). Ainda assim, o experimento é apropriado para estudar contenção de recursos microarquiteturais.

### 1.2 Desenho experimental

Serão comparados três cenários:

| Cenário | Núcleos | Processos | Finalidade |
|---|---:|---:|---|
| A | 1 | 1 | Referência: aplicação de memória isolada |
| B | 1 | 1 | Referência: aplicação computacional isolada |
| C | 2 | 2 | Execução concorrente e compartilhamento de memória |

A aplicação `stride` percorre um vetor com saltos regulares e enfatiza a memória. A aplicação `compute` realiza operações aritméticas intensivas.

---

## 2. Etapa prática 1 — Preparar o diretório

```bash
mkdir -p experiments/multiprogramacao/{src,bin,configs,resultados}
cd experiments/multiprogramacao
```

Copie ou crie os arquivos das etapas seguintes nos diretórios indicados.

---

## 3. Etapa prática 2 — Implementar as aplicações

Crie `src/stride.c`:

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N (1 << 20)
#define REPETICOES 40

int main(void) {
    int *dados = malloc(N * sizeof(int));
    if (!dados) return 1;

    for (int i = 0; i < N; i++) dados[i] = i;

    uint64_t soma = 0;
    for (int r = 0; r < REPETICOES; r++) {
        for (int i = 0; i < N; i += 16)
            soma += dados[i];
    }

    printf("stride: %llu\n", (unsigned long long)soma);
    free(dados);
    return 0;
}
```

Crie `src/compute.c`:

```c
#include <stdint.h>
#include <stdio.h>

#define ITERACOES 80000000UL

int main(void) {
    uint64_t x = 0x12345678ULL;
    for (unsigned long i = 0; i < ITERACOES; i++) {
        x = x * 1664525ULL + 1013904223ULL;
        x ^= x >> 13;
    }
    printf("compute: %llu\n", (unsigned long long)x);
    return 0;
}
```

As constantes podem ser reduzidas para testes rápidos ou ampliadas para experiências mais longas. Não altere-as entre cenários comparados.

---

## 4. Etapa prática 3 — Compilar os programas

Para simulação x86 no host x86-64:

```bash
gcc -O2 -static -o bin/stride src/stride.c
gcc -O2 -static -o bin/compute src/compute.c
file bin/stride bin/compute
```

Use binários estaticamente ligados quando possível. Eles reduzem dependências de bibliotecas dinâmicas no ambiente SE.

Teste fora do simulador:

```bash
./bin/stride
./bin/compute
```

---

## 5. Etapa prática 4 — Criar o script Python

Crie `configs/multiprogramacao.py`:

```python
import argparse
import m5
from m5.objects import *

parser = argparse.ArgumentParser()
parser.add_argument("--programas", nargs="+", required=True,
                    help="Um executável por núcleo")
parser.add_argument("--freq", default="2GHz")
args = parser.parse_args()

if len(args.programas) not in (1, 2):
    parser.error("Informe um ou dois programas")

system = System()
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = args.freq
system.clk_domain.voltage_domain = VoltageDomain()
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]

ncpus = len(args.programas)
system.cpu = [TimingSimpleCPU(cpu_id=i) for i in range(ncpus)]

system.membus = SystemXBar()

# L1 privada para cada núcleo.
for cpu in system.cpu:
    cpu.icache = Cache(size="32KiB", assoc=4,
                       tag_latency=1, data_latency=1,
                       response_latency=1, mshrs=4,
                       tgts_per_mshr=20)
    cpu.dcache = Cache(size="32KiB", assoc=4,
                       tag_latency=1, data_latency=1,
                       response_latency=1, mshrs=4,
                       tgts_per_mshr=20)
    cpu.icache.cpu_side = cpu.icache_port
    cpu.dcache.cpu_side = cpu.dcache_port
    cpu.icache.mem_side = system.membus.cpu_side_ports
    cpu.dcache.mem_side = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Cria e associa cada processo ao CPU de mesmo índice.
for i, executavel in enumerate(args.programas):
    processo = Process()
    processo.cmd = [executavel]
    system.cpu[i].workload = processo
    system.cpu[i].createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

print("Iniciando simulacao com", ncpus, "processo(s)")
evento = m5.simulate()
print("Encerrada em tick", m5.curTick(), "por:", evento.getCause())
```

O script escolhe o número de núcleos a partir do número de executáveis. Cada CPU recebe caches L1 privados; o barramento e a DRAM são compartilhados.

---

## 6. Etapa prática 5 — Executar os cenários de referência

A partir da raiz do gem5, execute:

```bash
build/X86/gem5.opt \
  --outdir=experiments/multiprogramacao/resultados/stride_isolado \
  experiments/multiprogramacao/configs/multiprogramacao.py \
  --programas experiments/multiprogramacao/bin/stride

build/X86/gem5.opt \
  --outdir=experiments/multiprogramacao/resultados/compute_isolado \
  experiments/multiprogramacao/configs/multiprogramacao.py \
  --programas experiments/multiprogramacao/bin/compute
```

Verifique a saída de cada aplicação em `simout` e a causa de término em `simout` ou no terminal.

---

## 7. Etapa prática 6 — Executar o cenário concorrente

```bash
build/X86/gem5.opt \
  --outdir=experiments/multiprogramacao/resultados/concorrente \
  experiments/multiprogramacao/configs/multiprogramacao.py \
  --programas experiments/multiprogramacao/bin/stride \
             experiments/multiprogramacao/bin/compute
```

Neste cenário, os processos executam em CPUs diferentes. Eles não compartilham as L1, mas competem pelo barramento e pelo controlador de memória. Para estudar competição por uma L2 compartilhada, acrescente uma L2 entre as L1 e a memória em uma extensão controlada do experimento.

---

## 8. Etapa prática 7 — Extrair estatísticas

Para obter métricas relevantes:

```bash
for d in stride_isolado compute_isolado concorrente; do
  echo "=== $d ==="
  grep -E 'simSeconds|simInsts|system.cpu[0-9]+.numCycles|system.cpu[0-9]+.ipc|dcache.overallMissRate|mem_ctrl.dram.bwTotal' \
    experiments/multiprogramacao/resultados/$d/stats.txt
done
```

Métricas úteis:

- `simSeconds`: tempo simulado até a conclusão de todas as cargas;
- `system.cpuN.ipc`: instruções por ciclo de cada CPU;
- `system.cpuN.dcache.overallMissRate::total`: taxa de faltas na L1 de dados;
- `mem_ctrl.dram.bwTotal`: tráfego ou largura de banda observada na DRAM, quando disponível.

Calcule a degradação individual de uma aplicação como:

\[
Degradacao(\%) = \frac{T_{concorrente} - T_{isolado}}{T_{isolado}} \times 100
\]

Em execuções com término conjunto, o `simSeconds` global não fornece diretamente o tempo de cada processo. Para uma análise individual precisa, use contadores por CPU, checkpoints/markers ou execute cargas com quantidade de trabalho comparável.

---

## 9. Interpretação dos resultados

Espera-se que `stride` gere mais acessos à memória e sofra mais com a competição do que `compute`. Porém, o resultado depende do tamanho dos vetores, da associatividade das caches, da frequência e do modelo de memória.

Não conclua que uma aplicação “é mais lenta” usando apenas ciclos globais. Compare a mesma carga isolada e concorrente, mantenha todas as demais configurações constantes e registre a versão do gem5, os comandos, os binários e as configurações.

---

## 10. Exercícios

1. Substitua `TimingSimpleCPU` por `MinorCPU` e compare o comportamento.
2. Aumente a L1-D de 32 KiB para 64 KiB. Qual aplicação se beneficia mais?
3. Adicione uma L2 compartilhada e repita o experimento.
4. Execute duas instâncias de `stride`. A contenção aumenta em relação ao par heterogêneo?
5. Registre os resultados em uma tabela CSV com cenário, IPC por CPU, faltas de cache e tempo simulado.

## Conclusão

Você configurou uma experiência de multiprogramação em modo SE, atribuindo aplicações a CPUs distintos por uma API Python. Esse método isola o efeito de recursos microarquiteturais compartilhados, mas não substitui estudos que dependem do comportamento de um sistema operacional real; para esses casos, use o modo FS.
