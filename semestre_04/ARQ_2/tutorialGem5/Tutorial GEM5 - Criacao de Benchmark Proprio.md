# Tutorial GEM5 — Criação de um Benchmark Próprio

## Introdução

Benchmarks públicos facilitam comparações com outros estudos, mas nem sempre representam o algoritmo, o padrão de acesso à memória ou as entradas de interesse de um projeto. Um benchmark próprio permite controlar esses fatores, desde que seja implementado, validado e documentado com rigor.

## Objetivo

Este tutorial ensina a criar um benchmark parametrizável de **histograma de imagem em tons de cinza** e a executá-lo em modo SE por uma configuração Python. Ao final, você deverá conseguir:

- especificar uma carga de trabalho antes de implementá-la;
- criar entradas reproduzíveis com diferentes tamanhos e distribuições;
- compilar e validar o programa;
- executar a carga no gem5 usando argumentos;
- registrar métricas e construir uma campanha experimental.

> **Pré-requisitos:** gem5 compilado para `X86`, GCC ou Clang, Python 3 e modo SE funcional.

---

## 1. Conceitos fundamentais

### 1.1 O que torna um benchmark útil

Um benchmark deve ter uma finalidade clara. Documente pelo menos:

- **algoritmo:** o que é calculado;
- **métrica de corretude:** como verificar a saída;
- **parâmetros de entrada:** quais dimensões ou sementes variam;
- **comportamento desejado:** computacional, cache-friendly, intensivo em memória ou misto;
- **critério de término:** o que representa uma execução completa.

Evite usar apenas uma entrada pequena: ela pode permanecer inteiramente na cache e ocultar o comportamento que se pretende estudar.

### 1.2 Benchmark proposto

O programa lê uma imagem sintética em tons de cinza, calcula o histograma de 256 níveis e produz um checksum. O tamanho da imagem e a semente são argumentos. O algoritmo realiza leituras sequenciais e atualizações em um vetor pequeno de contadores, permitindo estudar efeitos de localidade e capacidade.

---

## 2. Etapa prática 1 — Organizar o projeto

```bash
mkdir -p experiments/benchmark_proprio/{src,bin,configs,entradas,resultados,docs}
cd experiments/benchmark_proprio
```

Crie `docs/especificacao.md` com o seguinte conteúdo inicial:

```markdown
# Especificação — Histograma

- Entrada: quantidade de pixels e semente numérica.
- Saída: checksum do histograma e total de pixels.
- Corretude: o total deve ser igual à quantidade de pixels; o checksum deve ser reproduzível para a mesma semente.
- Padrão de acesso: varredura sequencial da imagem e atualizações em 256 contadores.
- Métricas: ciclos, instruções, IPC, faltas de L1-D e tempo simulado.
```

Esse registro evita que detalhes importantes sejam perdidos quando o experimento crescer.

---

## 3. Etapa prática 2 — Implementar o benchmark

Crie `src/histograma.c`:

```c
#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static uint32_t proximo(uint32_t *estado) {
    *estado = *estado * 1664525u + 1013904223u;
    return *estado;
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "uso: %s <pixels> <semente>\n", argv[0]);
        return 2;
    }

    errno = 0;
    unsigned long pixels = strtoul(argv[1], NULL, 10);
    uint32_t estado = (uint32_t)strtoul(argv[2], NULL, 10);
    if (errno || pixels == 0) {
        fprintf(stderr, "parametros invalidos\n");
        return 2;
    }

    unsigned char *imagem = malloc(pixels);
    uint64_t hist[256] = {0};
    if (!imagem) {
        fprintf(stderr, "falha de alocacao\n");
        return 1;
    }

    for (unsigned long i = 0; i < pixels; i++)
        imagem[i] = (unsigned char)(proximo(&estado) >> 24);

    for (unsigned long i = 0; i < pixels; i++)
        hist[imagem[i]]++;

    uint64_t total = 0;
    uint64_t checksum = 0;
    for (unsigned int i = 0; i < 256; i++) {
        total += hist[i];
        checksum += hist[i] * (uint64_t)(i + 1);
    }

    printf("pixels=%lu total=%" PRIu64 " checksum=%" PRIu64 "\n",
           pixels, total, checksum);
    free(imagem);
    return total == pixels ? 0 : 1;
}
```

### Decisões de projeto

- O gerador pseudoaleatório é implementado no próprio programa; logo, a entrada é reproduzível pela semente.
- O checksum permite comparar execuções sem armazenar um arquivo grande de saída.
- O vetor de histograma é pequeno e tende a permanecer na cache; a imagem determina a pressão de capacidade e tráfego de leitura.

---

## 4. Etapa prática 3 — Compilar e validar

Compile com GCC:

```bash
gcc -O2 -Wall -Wextra -static -o bin/histograma_gcc src/histograma.c
```

Ou com Clang:

```bash
clang -O2 -Wall -Wextra -static -o bin/histograma_clang src/histograma.c
```

Teste a corretude no host:

```bash
./bin/histograma_gcc 1048576 42
./bin/histograma_gcc 1048576 42
```

As duas saídas devem ser idênticas e `total` deve ser igual a `pixels`. Teste também entradas de tamanhos diferentes:

```bash
./bin/histograma_gcc 32768 42
./bin/histograma_gcc 8388608 42
```

Não compare desempenho de binários GCC e Clang sem registrar versões, flags e bibliotecas. Eles podem gerar código substancialmente diferente.

---

## 5. Etapa prática 4 — Definir os conjuntos de entrada

Crie `entradas/casos.csv`:

```csv
nome,pixels,semente
pequeno,32768,42
medio,1048576,42
grande,8388608,42
grande_outra_semente,8388608,2026
```

Os tamanhos foram escolhidos para atravessar escalas típicas de cache. Confirme os tamanhos reais da hierarquia simulada antes de formular hipóteses. A variação de semente testa se o resultado depende indevidamente de uma distribuição específica de valores.

---

## 6. Etapa prática 5 — Criar a configuração Python

Crie `configs/benchmark.py`:

```python
import argparse
import m5
from m5.objects import *

parser = argparse.ArgumentParser()
parser.add_argument("--cmd", required=True)
parser.add_argument("--pixels", required=True)
parser.add_argument("--semente", required=True)
parser.add_argument("--l1d", default="32KiB")
args = parser.parse_args()

system = System()
system.clk_domain = SrcClockDomain(clock="2GHz",
                                   voltage_domain=VoltageDomain())
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]
system.cpu = TimingSimpleCPU(cpu_id=0)
system.membus = SystemXBar()

system.cpu.icache = Cache(size="32KiB", assoc=4, tag_latency=1,
                          data_latency=1, response_latency=1,
                          mshrs=4, tgts_per_mshr=20)
system.cpu.dcache = Cache(size=args.l1d, assoc=4, tag_latency=1,
                          data_latency=1, response_latency=1,
                          mshrs=4, tgts_per_mshr=20)
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port
system.cpu.icache.mem_side = system.membus.cpu_side_ports
system.cpu.dcache.mem_side = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

process = Process()
process.cmd = [args.cmd, args.pixels, args.semente]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()
event = m5.simulate()
print("Fim:", event.getCause())
```

A lista `process.cmd` transmite os argumentos para o executável simulado. Essa abordagem é preferível a recompilar o programa para cada tamanho de entrada.

---

## 7. Etapa prática 6 — Executar uma campanha manual

A partir da raiz do gem5:

```bash
build/X86/gem5.opt \
  --outdir=experiments/benchmark_proprio/resultados/medio_l1_32k \
  experiments/benchmark_proprio/configs/benchmark.py \
  --cmd=experiments/benchmark_proprio/bin/histograma_gcc \
  --pixels=1048576 --semente=42 --l1d=32KiB
```

Valide em `simout` que `total=1048576`. Só então use `stats.txt` como resultado de desempenho.

Execute também os casos pequeno e grande. Para uma comparação de cache, repita cada entrada com `--l1d=16KiB`, `32KiB` e `64KiB`.

---

## 8. Etapa prática 7 — Coletar métricas

Em cada `stats.txt`, procure:

```bash
grep -E '^simSeconds|^simInsts|^system.cpu.numCycles|^system.cpu.ipc|dcache.overallMissRate::total' \
  resultados/medio_l1_32k/stats.txt
```

Registre uma tabela de resultados:

| Entrada | L1-D | Ciclos | Instruções | IPC | Faltas L1-D | Tempo |
|---|---:|---:|---:|---:|---:|---:|
| pequeno | 16 KiB |  |  |  |  |  |
| médio | 16 KiB |  |  |  |  |  |
| grande | 16 KiB |  |  |  |  |  |

Diferencie métricas de trabalho fixo, como instruções, de métricas dependentes da configuração, como ciclos e faltas. Se as instruções divergirem inesperadamente para a mesma entrada, investigue antes de comparar desempenho.

---

## 9. Boas práticas de reprodutibilidade

- mantenha código, scripts e resultados versionados;
- registre versão e commit do gem5, compilador e flags;
- preserve os comandos de cada execução;
- use nomes de diretório que revelem parâmetros relevantes;
- valide funcionalmente todas as configurações;
- execute mais de uma repetição apenas quando houver fonte de variação; simulações determinísticas com configuração fixa em geral reproduzem o mesmo resultado.

## 10. Exercícios

1. Acrescente um modo de acesso com salto (`stride`) como terceiro argumento e compare localidade espacial.
2. Faça a imagem ser lida de um arquivo e compare o custo com a geração sintética.
3. Use `uint32_t hist[256]` e avalie se há diferença de cache.
4. Inclua uma fase de transformação da imagem antes do histograma.
5. Escreva um script que leia `casos.csv` e dispare todos os experimentos.

## Conclusão

Você criou uma carga de trabalho parametrizável, verificável e adequada para campanhas no gem5. Um benchmark próprio tem valor quando suas entradas e métricas representam a pergunta arquitetural de interesse, e quando sua corretude e condições de execução são explicitamente registradas.
