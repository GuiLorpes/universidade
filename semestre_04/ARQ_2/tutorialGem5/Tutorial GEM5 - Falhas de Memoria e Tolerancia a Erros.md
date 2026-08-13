# Tutorial GEM5 — Falhas de Memória e Tolerância a Erros

## Introdução

Falhas de memória podem ser transitórias (*soft errors*), permanentes ou intermitentes. O gem5 é útil para estudos arquiteturais de tolerância a erros, mas a disponibilidade de modelos de injeção e ECC depende da versão, da ISA e de extensões usadas. Este tutorial propõe um experimento reprodutível com **injeção de corrupção em nível de aplicação** em SE, distinguindo-o de uma falha física real de DRAM.

## Objetivo

Avaliar como redundância e checksum detectam corrupção de dados em um programa executado no modo **SE** por uma configuração **Python**. Comparar uma versão sem proteção com uma versão que detecta erro.

## Limites do experimento

A injeção implementada no programa altera um dado propositalmente. Ela não modela radiação, células defeituosas, ECC real, propagação elétrica ou falhas silenciosas de hardware. Para esses objetivos, use um modelo de falhas ou extensão apropriada e documente seu mecanismo.

## Pré-requisitos

```bash
cd ~/gem5
scons build/X86/gem5.opt -j"$(nproc)"
mkdir -p workloads scripts resultados
```

## Etapa 1 — Criar o programa com proteção opcional

```c
// workloads/tolerancia.c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 1048576

static uint64_t checksum(const uint32_t *v, size_t n) {
    uint64_t s = 0;
    for (size_t i = 0; i < n; i++) s = (s << 5) - s + v[i];
    return s;
}

int main(int argc, char **argv) {
    int injetar = argc > 1 && strcmp(argv[1], "--falha") == 0;
    uint32_t *dados = malloc(N * sizeof(*dados));
    if (!dados) return 2;

    for (size_t i = 0; i < N; i++) dados[i] = (uint32_t)(i * 17u + 3u);
    uint64_t antes = checksum(dados, N);

    if (injetar) {
        dados[N / 2] ^= 0x00010000u;
        printf("Falha injetada no indice %d\n", N / 2);
    }

    uint64_t depois = checksum(dados, N);
    free(dados);

    if (antes != depois) {
        puts("ERRO DETECTADO: checksum divergente");
        return 1;
    }
    puts("Dados inteiros: checksum confere");
    return 0;
}
```

```bash
gcc -O2 -static -o workloads/tolerancia workloads/tolerancia.c
```

## Etapa 2 — Executar nativamente para validar

```bash
./workloads/tolerancia
./workloads/tolerancia --falha
echo $?
```

O primeiro caso deve informar integridade; o segundo deve detectar erro e retornar código diferente de zero.

## Etapa 3 — Criar a configuração SE

Crie `scripts/falhas_se.py`:

```python
import argparse
import m5
from m5.objects import *

p = argparse.ArgumentParser()
p.add_argument("--binary", required=True)
p.add_argument("--inject", action="store_true")
a = p.parse_args()

system = System()
system.clk_domain = SrcClockDomain(clock="2GHz", voltage_domain=VoltageDomain())
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("256MiB")]
system.cpu = TimingSimpleCPU()
system.membus = SystemXBar()
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

cmd = [a.binary] + (["--falha"] if a.inject else [])
process = Process(cmd=cmd)
system.cpu.workload = process
system.cpu.createThreads()
root = Root(full_system=False, system=system)
m5.instantiate()
event = m5.simulate()
print("Causa de parada:", event.getCause())
```

## Etapa 4 — Rodar os cenários

```bash
build/X86/gem5.opt --outdir=resultados/sem_falha scripts/falhas_se.py \
  --binary=workloads/tolerancia

build/X86/gem5.opt --outdir=resultados/com_falha scripts/falhas_se.py \
  --binary=workloads/tolerancia --inject
```

Examine `simout` e `simerr` nos dois diretórios. Em SE, a terminação do processo pode ser reportada como uma causa normal de saída; o texto emitido pelo programa é a evidência de detecção.

## Etapa 5 — Comparar custo da proteção

Para medir overhead, crie uma versão compilada sem checksum ou introduza uma opção de linha de comando que o desative. Execute ambas com a mesma entrada e compare:

```bash
for caso in sem_falha com_falha; do
  echo "=== $caso ==="
  grep -E "simSeconds|system.cpu.numCycles|system.cpu.committedInsts" \
    resultados/$caso/stats.txt
done
```

O cenário `com_falha` não mede somente o custo de detecção, pois termina com erro. Para estimar overhead, execute o checksum com dados não corrompidos e compare-o com uma implementação sem checksum.

## Interpretação

- **Cobertura de detecção:** uma alteração que muda o checksum foi identificada.
- **Overhead:** aumento de instruções, ciclos ou tempo decorrente da verificação.
- **Falha silenciosa:** ocorre se a corrupção não for detectada; um checksum simples não garante cobertura completa.
- **Correção:** este programa apenas detecta. Para corrigir, use duplicação, códigos de correção ou cópia redundante.

## Exercícios

1. Substitua o checksum por duplicação modular redundante: calcule o resultado duas vezes e compare.
2. Injete falhas em índices e bits variados e calcule a taxa de detecção observada.
3. Pesquise na sua versão do gem5 por suporte a ECC, modelos de falha ou pontos de instrumentação e adapte o experimento para injeção abaixo do nível da aplicação.

## Conclusão

Você configurou um experimento que separa claramente detecção em software de modelagem física de falhas. Essa distinção é essencial para produzir resultados interpretáveis sobre tolerância a erros.