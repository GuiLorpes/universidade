# Tutorial GEM5: Avaliação de Mapeamentos de Cache com PolyBench em Full System e API Python

## Introdução e objetivo

A organização da cache determina como blocos da memória principal podem ser posicionados nas linhas de cache. Essa decisão influencia diretamente conflitos, taxa de faltas (*miss rate*), latência e tempo de execução. Neste tutorial, você executará o benchmark **PolyBench/C** no gem5 em modo **Full System (FS)** e comparará três organizações para a cache L1 de dados:

- **Mapeamento direto**: cada bloco de memória só pode ocupar uma linha específica da cache;
- **Totalmente associativo**: cada bloco pode ocupar qualquer linha da cache;
- **Associativo por conjunto**: cada bloco pode ocupar uma das linhas de um conjunto específico.

O experimento será controlado por um arquivo Python de configuração do gem5. Ao final, você terá resultados comparáveis em `stats.txt`, uma tabela de métricas e uma interpretação dos efeitos de cada mapeamento.

> **Escopo:** arquitetura x86, um núcleo, CPU `TimingSimpleCPU`, caches clássicas do gem5 e execução completa de um sistema operacional convidado. O método é aplicável a outras ISAs, mas kernel, imagem de disco e comandos de compilação devem ser compatíveis com a arquitetura escolhida.

---

## 1. Fundamentos: como os três mapeamentos funcionam

Considere uma cache com capacidade $C$, tamanho de bloco $B$ e associatividade $A$. O número de linhas é:

$$
N = \frac{C}{B}
$$

E o número de conjuntos é:

$$
S = \frac{N}{A}
$$

Para um endereço de memória, o gem5 divide a identificação do bloco em **tag**, **índice do conjunto** e **deslocamento no bloco**.

| Organização | Associatividade $A$ | Número de conjuntos | Consequência principal |
|---|---:|---:|---|
| Direta | 1 | $N$ | Simples e rápida, porém propensa a faltas por conflito. |
| Associativa por conjunto | 2, 4, 8, ... | $N/A$ | Compromisso entre custo, latência e redução de conflitos. |
| Totalmente associativa | $N$ | 1 | Minimiza faltas por conflito, mas tem maior complexidade de busca. |

Neste tutorial, a cache L1D terá sempre **32 KiB** e blocos de **64 bytes**. Portanto:

$$
N = \frac{32\ \mathrm{KiB}}{64\ \mathrm{B}} = 512\ \text{linhas}
$$

Os cenários serão:

| Cenário | `l1d_assoc` | Organização |
|---|---:|---|
| `direta` | `1` | Direta: 512 conjuntos, 1 linha por conjunto. |
| `conjunto4` | `4` | 4 vias: 128 conjuntos, 4 linhas por conjunto. |
| `total` | `512` | Totalmente associativa: 1 conjunto, 512 linhas. |

> Uma cache é considerada totalmente associativa quando sua associatividade é igual ao número total de linhas. Para outros tamanhos de cache ou blocos, recalcule esse valor.

---

## 2. Visão geral do experimento

A sequência de trabalho será:

1. Preparar o gem5, o PolyBench e uma imagem de disco FS.
2. Selecionar e compilar um benchmark PolyBench no sistema convidado.
3. Criar um arquivo de comandos que será executado no boot do Linux convidado.
4. Criar o script Python do gem5 com a associatividade parametrizável.
5. Rodar os três cenários, alterando apenas `--l1d-assoc`.
6. Extrair métricas de cada `stats.txt` e comparar os resultados.

### Por que usar PolyBench?

O **PolyBench/C** é uma suíte de kernels numéricos com laços aninhados e matrizes. Ela é especialmente útil para estudos de cache porque seus acessos à memória podem ser intensos e regulares. Entre seus grupos de kernels estão:

- `linear-algebra/blas`: por exemplo, `gemm`, `gemver` e `gesummv`;
- `linear-algebra/kernels`: por exemplo, `2mm`, `3mm`, `atax` e `bicg`;
- `datamining`: por exemplo, `correlation` e `covariance`;
- `stencils`: por exemplo, `jacobi-1d`, `jacobi-2d`, `fdtd-2d`.

Usaremos o kernel **`gemm`** (*General Matrix Multiply*), que calcula uma multiplicação de matrizes. Ele apresenta reutilização de dados e pressão significativa sobre a hierarquia de memória.

---

## 3. Pré-requisitos

No computador hospedeiro, parta de uma instalação do gem5 que já consiga executar x86 em FS. Você precisará de:

- repositório do gem5 e binário `build/X86/gem5.opt`;
- kernel Linux x86 compatível;
- imagem de disco x86 com Linux e ferramentas básicas de compilação;
- acesso à Internet no sistema convidado **ou** uma cópia do PolyBench previamente colocada na imagem;
- Python 3 no hospedeiro.

Compile o binário otimizado do gem5, se necessário:

```bash
cd ~/gem5
scons build/X86/gem5.opt -j"$(nproc)"
```

Crie um diretório de trabalho no hospedeiro:

```bash
mkdir -p ~/gem5-cache-polybench/{configs,readfiles,resultados}
cd ~/gem5-cache-polybench
```

> Os nomes de recursos disponíveis podem mudar entre versões do gem5-resources. Caso sua instalação use caminhos locais em vez de `obtain_resource`, substitua as chamadas por caminhos absolutos para o kernel e a imagem de disco.

---

## 4. Etapa prática 1 — Preparar o PolyBench no sistema convidado

Há duas estratégias. A **Estratégia A** é mais simples para aprendizagem, pois baixa e compila o PolyBench durante o boot. A **Estratégia B** é preferível para experimentos repetidos, pois cria uma imagem já preparada e evita que download/compilação contaminem a execução medida.

### Estratégia A: instalação automatizada no boot

Crie o arquivo `readfiles/preparar_e_executar_gemm.rcS` no hospedeiro:

```bash
cat > readfiles/preparar_e_executar_gemm.rcS <<'EOF'
#!/bin/bash
set -e

MNT=/mnt/gem5
mkdir -p "$MNT"
mount /dev/sdb1 "$MNT" 2>/dev/null || true

# O diretório de saída deve estar no disco montado pelo gem5.
OUT="$MNT/cache-polybench"
mkdir -p "$OUT"

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y git build-essential time

cd /root
if [ ! -d polybench-c-4.2.1-beta ]; then
    git clone --depth 1 https://github.com/MatthiasJReisinger/PolyBenchC-4.2.1.git polybench-c-4.2.1-beta
fi

cd polybench-c-4.2.1-beta

# Compila o kernel gemm com tamanho DATASET_LARGE.
# --no-flush-cache evita adicionar uma limpeza artificial da cache antes do kernel.
gcc -O3 -march=x86-64 -DPOLYBENCH_TIME -DDATASET_LARGE \
    utilities/polybench.c \
    linear-algebra/blas/gemm/gemm.c \
    -I utilities -o "$OUT/gemm"

sync
printf 'INICIO_GEMM\n' > "$OUT/status.txt"
"$OUT/gemm" > "$OUT/gemm.stdout" 2> "$OUT/gemm.stderr"
printf 'FIM_GEMM\n' >> "$OUT/status.txt"
sync

# Solicita encerramento limpo; o gem5 detectará o evento de saída.
poweroff -f
EOF
chmod +x readfiles/preparar_e_executar_gemm.rcS
```

**Limitação importante:** o `apt-get`, `git clone` e a compilação tornam esta primeira execução longa e introduzem atividade de cache que não pertence ao benchmark. As estatísticas devem ser reiniciadas imediatamente antes do programa medido; isso será feito no script Python. Ainda assim, para estudos rigorosos, adote a Estratégia B.

### Estratégia B: imagem previamente preparada — recomendada

Inicialize uma vez uma imagem FS de forma interativa, copie o PolyBench para ela e compile o binário. Em seguida, mantenha a imagem-base sem modificações ou crie uma cópia exclusiva para cada experimento.

Dentro do convidado Linux:

```bash
apt-get update
apt-get install -y git build-essential
cd /root
git clone --depth 1 https://github.com/MatthiasJReisinger/PolyBenchC-4.2.1.git polybench
cd polybench
mkdir -p /root/bench

gcc -O3 -march=x86-64 -DPOLYBENCH_TIME -DDATASET_LARGE \
    utilities/polybench.c linear-algebra/blas/gemm/gemm.c \
    -I utilities -o /root/bench/gemm
```

Depois, crie um `readfile` mínimo para cada execução:

```bash
cat > readfiles/executar_gemm.rcS <<'EOF'
#!/bin/bash
set -e
MNT=/mnt/gem5
mkdir -p "$MNT"
mount /dev/sdb1 "$MNT" 2>/dev/null || true
/root/bench/gemm > "$MNT/gemm.stdout" 2> "$MNT/gemm.stderr"
sync
poweroff -f
EOF
chmod +x readfiles/executar_gemm.rcS
```

> Em imagens Linux diferentes, o dispositivo do disco secundário pode não ser `/dev/sdb1`. Confirme com `lsblk` durante uma execução interativa e ajuste o script.

---

## 5. Etapa prática 2 — Criar a configuração FS em Python

Crie `configs/fs_polybench_cache.py`:

```python
"""Executa PolyBench/GEMM em x86 FS, variando a associatividade da L1D.

Exemplos:
  build/X86/gem5.opt configs/fs_polybench_cache.py \
      --l1d-assoc 1 --readfile readfiles/executar_gemm.rcS

  build/X86/gem5.opt configs/fs_polybench_cache.py \
      --l1d-assoc 4 --readfile readfiles/executar_gemm.rcS

  build/X86/gem5.opt configs/fs_polybench_cache.py \
      --l1d-assoc 512 --readfile readfiles/executar_gemm.rcS
"""

import argparse

from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator


parser = argparse.ArgumentParser(
    description="Experimento FS: PolyBench/GEMM e associatividade da cache L1D"
)
parser.add_argument(
    "--l1d-assoc", type=int, required=True,
    help="Associatividade da L1D: 1=direta; 4=4 vias; 512=totalmente associativa"
)
parser.add_argument(
    "--readfile", required=True,
    help="Arquivo de comandos a executar no Linux convidado"
)
parser.add_argument(
    "--kernel", default="x86-linux-kernel-5.4.49",
    help="ID do recurso do kernel ou adapte o script para usar um caminho local"
)
parser.add_argument(
    "--disk", default="x86-ubuntu-18.04-img",
    help="ID do recurso da imagem de disco ou adapte o script para usar um caminho local"
)
args = parser.parse_args()

# L1D de 32 KiB e blocos de 64 B: há 512 linhas de cache.
L1D_SIZE = "32KiB"
L1D_LINES = 512

if args.l1d_assoc not in (1, 4, L1D_LINES):
    raise ValueError(
        f"Valor inválido para --l1d-assoc: {args.l1d_assoc}. "
        "Use 1 (direta), 4 (por conjunto de 4 vias) ou 512 (totalmente associativa)."
    )

# Mantemos todos os demais parâmetros constantes para isolar o efeito do mapeamento L1D.
cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1i_size="32KiB",
    l1i_assoc=8,
    l1d_size=L1D_SIZE,
    l1d_assoc=args.l1d_assoc,
    l2_size="256KiB",
    l2_assoc=8,
)

memory = SingleChannelDDR3_1600(size="3GiB")
processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING,
    isa=ISA.X86,
    num_cores=1,
)

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# Os IDs abaixo dependem da versão instalada de gem5-resources.
# Se a sua versão não possuir esses IDs, use recursos equivalentes ou caminhos locais.
kernel = obtain_resource(args.kernel)
disk_image = obtain_resource(args.disk)

board.set_kernel_disk_workload(
    kernel=kernel,
    disk_image=disk_image,
    readfile=args.readfile,
)

simulator = Simulator(board=board)
print(f"Iniciando FS com L1D={L1D_SIZE}, associatividade={args.l1d_assoc}")
simulator.run()
print("Causa de saída:", simulator.get_last_exit_event_cause())
```

### Entendendo os pontos essenciais do script

| Trecho | Papel no experimento |
|---|---|
| `PrivateL1PrivateL2CacheHierarchy(...)` | Constrói uma hierarquia clássica privada: L1I, L1D e L2. |
| `l1d_assoc=args.l1d_assoc` | Define diretamente o mapeamento avaliado na L1 de dados. |
| `TimingSimpleCPU` | Modela temporização e permite observar efeitos de latência de cache. Não use `ATOMIC` para esta comparação. |
| `X86Board` | Monta uma plataforma x86 para Full System. |
| `set_kernel_disk_workload(...)` | Informa kernel, disco e script a executar no Linux convidado. |
| `Simulator(board=board)` | Cria e executa a simulação usando a API Python do gem5. |

> Dependendo da versão do gem5, o construtor `PrivateL1PrivateL2CacheHierarchy` pode não expor os argumentos `l1i_assoc`, `l1d_assoc` ou `l2_assoc`. Nesse caso, use uma versão atual do gem5 ou crie uma hierarquia clássica personalizada que instancie `L1DCache` com o atributo `assoc` desejado. O princípio experimental permanece: `assoc=1`, `assoc=4` e `assoc=512`.

---

## 6. Etapa prática 3 — Garantir uma janela de medição limpa

No modo FS, o boot do Linux produz muitas referências à memória. Se você analisar o `stats.txt` final sem controle, as estatísticas incluirão boot, serviços do sistema e o benchmark. Para medir somente o `gemm`, use instruções especiais do gem5 no programa ou no script do convidado para:

1. zerar as estatísticas imediatamente antes do benchmark;
2. gerar um *dump* imediatamente depois;
3. encerrar a simulação.

Uma forma comum é instalar o utilitário **m5** na imagem convidada. Em muitas imagens de recursos do gem5, ele está em `/sbin/m5` ou `/usr/local/bin/m5`. Verifique com:

```bash
which m5 || find / -name m5 -type f 2>/dev/null
```

Com o utilitário disponível, use o seguinte `readfile` no lugar da versão simples:

```bash
cat > readfiles/executar_gemm_medido.rcS <<'EOF'
#!/bin/bash
set -e
M5=$(command -v m5 || true)
if [ -z "$M5" ]; then
    echo "ERRO: utilitário m5 não encontrado" >&2
    poweroff -f
fi

MNT=/mnt/gem5
mkdir -p "$MNT"
mount /dev/sdb1 "$MNT" 2>/dev/null || true

# Delimita a região de interesse (ROI): apenas a execução do GEMM.
"$M5" resetstats
/root/bench/gemm > "$MNT/gemm.stdout" 2> "$MNT/gemm.stderr"
"$M5" dumpstats
sync
"$M5" exit
EOF
chmod +x readfiles/executar_gemm_medido.rcS
```

Se você estiver usando a Estratégia A, mantenha a preparação da imagem e inclua somente as três operações abaixo ao redor da chamada ao `gemm`:

```bash
m5 resetstats
"$OUT/gemm" > "$OUT/gemm.stdout" 2> "$OUT/gemm.stderr"
m5 dumpstats
m5 exit
```

> Confirme no `stats.txt` que há uma seção posterior a `Begin Simulation Statistics`. A seção relevante é aquela gerada após `resetstats`, contendo apenas a região de interesse.

---

## 7. Etapa prática 4 — Executar os três cenários

Partindo de `~/gem5`, execute os comandos abaixo. Use um diretório de saída diferente por cenário; o gem5 grava `stats.txt`, `config.ini` e outros arquivos em `--outdir`.

```bash
cd ~/gem5

build/X86/gem5.opt --outdir=~/gem5-cache-polybench/resultados/direta \
  ~/gem5-cache-polybench/configs/fs_polybench_cache.py \
  --l1d-assoc 1 \
  --readfile ~/gem5-cache-polybench/readfiles/executar_gemm_medido.rcS

build/X86/gem5.opt --outdir=~/gem5-cache-polybench/resultados/conjunto4 \
  ~/gem5-cache-polybench/configs/fs_polybench_cache.py \
  --l1d-assoc 4 \
  --readfile ~/gem5-cache-polybench/readfiles/executar_gemm_medido.rcS

build/X86/gem5.opt --outdir=~/gem5-cache-polybench/resultados/total \
  ~/gem5-cache-polybench/configs/fs_polybench_cache.py \
  --l1d-assoc 512 \
  --readfile ~/gem5-cache-polybench/readfiles/executar_gemm_medido.rcS
```

### Verificação da configuração efetiva

Após cada execução, confirme a associatividade no arquivo gerado pelo gem5:

```bash
grep -n '^assoc=' ~/gem5-cache-polybench/resultados/direta/config.ini | head
grep -n '^assoc=' ~/gem5-cache-polybench/resultados/conjunto4/config.ini | head
grep -n '^assoc=' ~/gem5-cache-polybench/resultados/total/config.ini | head
```

Localize a seção correspondente à L1D, normalmente semelhante a `[system.cache_hierarchy.l1d_cache]`. Ela deve conter `assoc=1`, `assoc=4` ou `assoc=512` conforme o cenário.

---

## 8. Etapa prática 5 — Coletar dados de `stats.txt`

Os nomes exatos podem variar conforme a versão e a configuração, mas caches clássicas normalmente expõem estatísticas semelhantes a:

- `...l1d_cache.overallHits::total`;
- `...l1d_cache.overallMisses::total`;
- `...l1d_cache.overallAccesses::total`;
- `...l1d_cache.demandMisses::total`;
- `simSeconds`, `simTicks` e `hostSeconds`.

Procure os campos da L1D:

```bash
grep -E 'l1d_cache.*(overall(Hits|Misses|Accesses)|demandMisses)' \
  ~/gem5-cache-polybench/resultados/direta/stats.txt
```

Compare o tempo simulado:

```bash
grep -E '^(simSeconds|simTicks|hostSeconds)' \
  ~/gem5-cache-polybench/resultados/direta/stats.txt
```

### Script de extração automática

Crie `extrair_resultados.py` no diretório do experimento:

```python
#!/usr/bin/env python3
"""Extrai métricas L1D dos resultados de três execuções gem5."""

from pathlib import Path
import re

BASE = Path.home() / "gem5-cache-polybench" / "resultados"
CENARIOS = ["direta", "conjunto4", "total"]


def ultimo_valor(texto: str, padrao: str):
    """Retorna a última ocorrência numérica de uma estatística no stats.txt."""
    achados = re.findall(padrao, texto, flags=re.MULTILINE)
    return float(achados[-1]) if achados else None


def stat(texto: str, sufixo: str):
    # Aceita qualquer prefixo de caminho até l1d_cache.
    padrao = rf"^\S*l1d_cache\.{re.escape(sufixo)}\s+([0-9.eE+-]+)"
    return ultimo_valor(texto, padrao)


print("cenario,acessos_l1d,hits_l1d,misses_l1d,miss_rate,sim_seconds")
for cenario in CENARIOS:
    arquivo = BASE / cenario / "stats.txt"
    texto = arquivo.read_text(errors="replace")

    acessos = stat(texto, "overallAccesses::total")
    hits = stat(texto, "overallHits::total")
    misses = stat(texto, "overallMisses::total")
    tempo = ultimo_valor(texto, r"^simSeconds\s+([0-9.eE+-]+)")

    # Algumas versões não publicam overallAccesses; nesse caso, use hits + misses.
    if acessos is None and hits is not None and misses is not None:
        acessos = hits + misses
    taxa = (misses / acessos) if acessos and misses is not None else None

    def fmt(valor):
        return "NA" if valor is None else f"{valor:.8g}"

    print(
        f"{cenario},{fmt(acessos)},{fmt(hits)},{fmt(misses)},"
        f"{fmt(taxa)},{fmt(tempo)}"
    )
```

Execute:

```bash
cd ~/gem5-cache-polybench
python3 extrair_resultados.py | tee resultados/resumo.csv
```

O arquivo `resumo.csv` terá estrutura semelhante a:

```csv
cenario,acessos_l1d,hits_l1d,misses_l1d,miss_rate,sim_seconds
direta,valor,valor,valor,valor,valor
conjunto4,valor,valor,valor,valor,valor
total,valor,valor,valor,valor,valor
```

---

## 9. Etapa prática 6 — Analisar os resultados

Monte uma tabela final, preenchendo-a com os valores do seu `resumo.csv`.

| Cenário | Associatividade L1D | Acessos L1D | Faltas L1D | Taxa de faltas | `simSeconds` | Variação de tempo vs. direta |
|---|---:|---:|---:|---:|---:|---:|
| Direta | 1 |  |  |  |  | 0% |
| Por conjunto | 4 |  |  |  |  |  |
| Totalmente associativa | 512 |  |  |  |  |  |

Calcule a variação percentual de tempo de um cenário $X$ em relação ao direto por:

$$
\Delta T_X(\%) = \frac{T_X - T_{direta}}{T_{direta}} \times 100
$$

E a taxa de faltas da L1D por:

$$
\mathrm{miss\ rate} = \frac{\mathrm{overallMisses}}{\mathrm{overallAccesses}}
$$

### Interpretação esperada

Em igualdade de capacidade, bloco e política de substituição, aumentar a associatividade normalmente reduz ou preserva as faltas por conflito:

$$
\mathrm{misses}_{total} \leq \mathrm{misses}_{4\ vias} \leq \mathrm{misses}_{direta}
$$

Na prática, essa relação pode não aparecer de forma estrita em todas as métricas por causa de políticas de prefetch, substituição, comportamento do sistema operacional e interferências de outras caches. Ainda assim, examine principalmente:

1. **Faltas L1D:** uma queda ao passar de 1 para 4 vias indica conflitos no mapeamento direto.
2. **Acessos e faltas na L2:** se a L1D reduz faltas, a L2 tende a receber menos requisições.
3. **Tempo simulado:** menos faltas pode reduzir `simSeconds`, pois reduz acessos mais lentos à L2 e à DRAM.
4. **Custo do modelo:** uma cache totalmente associativa não representa necessariamente uma implementação física barata. O gem5 modela a configuração funcional e de temporização selecionada; não conclua automaticamente que ela tem o mesmo custo de acesso de uma cache direta real.

### Como identificar faltas por conflito

Uma falta de conflito ocorre quando blocos distintos competem pelo mesmo conjunto, apesar de a cache possuir capacidade total suficiente para comportá-los. Evidências no experimento:

- a cache direta apresenta mais faltas que a 4-way, mantendo capacidade igual;
- a 4-way se aproxima do resultado totalmente associativo;
- o tempo de simulação reduz junto com as faltas da L1D.

Se os três resultados forem muito parecidos, o `gemm` escolhido pode não estar produzindo conflitos relevantes para esses tamanhos. Nesse caso, experimente outros kernels do PolyBench (`2mm`, `atax`, `bicg`, `fdtd-2d`) ou reduza a capacidade da L1D, sempre documentando a mudança.

---

## 10. Validade experimental e boas práticas

Para que a comparação seja válida, altere **somente** a associatividade da L1D entre as execuções. Mantenha constantes:

- binário do PolyBench, flags de compilação e tamanho de dataset;
- tamanho da L1D (`32KiB`) e tamanho de bloco (`64B`);
- L1I, L2, memória, CPU, frequência e número de núcleos;
- kernel, imagem de disco e conteúdo do `readfile`;
- versão do gem5;
- aquecimento e delimitação da região de interesse (`m5 resetstats` e `m5 dumpstats`).

Também é recomendável:

- fazer ao menos três repetições por cenário se houver fontes de não determinismo;
- registrar o `config.ini` junto ao resultado;
- guardar o `gem5.out` e o `stats.txt` de cada execução;
- usar uma imagem de disco de trabalho por execução para não alterar o estado entre cenários;
- separar o boot e a preparação da medição do benchmark.

---

## 11. Exercícios de extensão

1. Adicione cenários de 2, 8 e 16 vias, respeitando que a associatividade deve dividir o total de linhas.
2. Mantenha a associatividade em 4 vias e compare L1D de 16 KiB, 32 KiB e 64 KiB.
3. Execute `atax` e `fdtd-2d`; compare quais kernels são mais sensíveis ao aumento de associatividade.
4. Avalie as faltas e acessos da L2 para explicar se a melhoria da L1D propaga-se pela hierarquia.
5. Substitua a `TimingSimpleCPU` por um modelo mais detalhado, documentando cuidadosamente quais parâmetros foram modificados.

---

## Conclusão

Neste tutorial, você configurou um sistema x86 em **Full System** usando a **API Python** do gem5 e usou o PolyBench/GEMM para comparar cache L1D direta, associativa por conjunto e totalmente associativa. A variável independente foi `l1d_assoc`: `1`, `4` e `512`. A análise deve combinar a taxa de faltas da L1D, o tráfego para níveis inferiores e o tempo simulado, sempre com uma região de interesse delimitada para excluir o boot do sistema operacional.
