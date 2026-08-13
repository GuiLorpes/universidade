# Tutorial GEM5 — Automação de Campanhas e Visualização de Resultados

## Introdução

Experimentos em arquitetura de computadores raramente envolvem uma única simulação. Variar tamanho de cache, associatividade, política de substituição, modelo de CPU ou benchmark rapidamente gera dezenas de execuções. A automação reduz erros manuais, preserva a rastreabilidade e torna os resultados mais fáceis de analisar.

## Objetivo

Este tutorial ensina a construir uma campanha automatizada no gem5, em modo SE e com API Python. Ao final, você deverá conseguir:

- criar um benchmark simples e uma configuração Python parametrizável;
- definir uma matriz de experimentos em CSV;
- executar todas as combinações por um script Python;
- extrair estatísticas de `stats.txt` para um CSV consolidado;
- gerar gráficos de desempenho e de faltas de cache.

> **Pré-requisitos:** gem5 compilado para `X86`, Python 3, GCC e, para os gráficos, as bibliotecas Python `pandas` e `matplotlib` (`python3 -m pip install pandas matplotlib`).

---

## 1. Conceitos fundamentais

### 1.1 Unidade experimental

Cada linha da campanha deve representar uma configuração completa: benchmark, parâmetros de entrada, CPU, cache, memória e outras variáveis. O diretório de saída precisa permitir identificar essa configuração sem depender de memória ou anotações externas.

### 1.2 Variáveis controladas

Neste tutorial, a variável independente é a cache L1-D:

| Parâmetro | Valores |
|---|---|
| Tamanho L1-D | 16 KiB, 32 KiB, 64 KiB |
| Associatividade L1-D | 1, 2, 4, 8 |
| Benchmark | percurso de matriz |
| CPU | `TimingSimpleCPU` |
| Frequência | 2 GHz |
| Memória | DDR3-1600 |

Como CPU, programa e memória permanecem constantes, diferenças observadas devem ser atribuídas principalmente às configurações de L1-D.

---

## 2. Etapa prática 1 — Organizar os arquivos

```bash
mkdir -p experiments/automacao/{src,bin,configs,scripts,resultados,graficos}
cd experiments/automacao
```

---

## 3. Etapa prática 2 — Criar o benchmark

Crie `src/percurso_matriz.c`:

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define LINHAS 1024
#define COLUNAS 1024
#define REPETICOES 12

int main(void) {
    int *m = malloc((size_t)LINHAS * COLUNAS * sizeof(int));
    if (!m) return 1;

    for (int i = 0; i < LINHAS; i++)
        for (int j = 0; j < COLUNAS; j++)
            m[(size_t)i * COLUNAS + j] = i + 3 * j;

    uint64_t soma = 0;
    for (int r = 0; r < REPETICOES; r++) {
        for (int j = 0; j < COLUNAS; j++)
            for (int i = 0; i < LINHAS; i++)
                soma += m[(size_t)i * COLUNAS + j];
    }

    printf("checksum=%llu\n", (unsigned long long)soma);
    free(m);
    return 0;
}
```

Esse acesso por colunas em uma matriz armazenada por linhas reduz a localidade espacial e torna o benchmark sensível à hierarquia de memória.

Compile:

```bash
gcc -O2 -static -o bin/percurso_matriz src/percurso_matriz.c
./bin/percurso_matriz
```

Registre o checksum: todas as simulações devem imprimir o mesmo valor.

---

## 4. Etapa prática 3 — Criar uma configuração parametrizável

Crie `configs/cache_experimento.py`:

```python
import argparse
import m5
from m5.objects import *

parser = argparse.ArgumentParser()
parser.add_argument("--cmd", required=True)
parser.add_argument("--l1d-size", required=True)
parser.add_argument("--l1d-assoc", type=int, required=True)
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
system.cpu.dcache = Cache(size=args.l1d_size, assoc=args.l1d_assoc,
                          tag_latency=1, data_latency=1,
                          response_latency=1, mshrs=4,
                          tgts_per_mshr=20)
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port
system.cpu.icache.mem_side = system.membus.cpu_side_ports
system.cpu.dcache.mem_side = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

process = Process()
process.cmd = [args.cmd]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()
event = m5.simulate()
print("Fim:", event.getCause())
```

---

## 5. Etapa prática 4 — Definir a matriz de experimentos

Crie `scripts/campanha.csv`:

```csv
id,l1d_size,l1d_assoc
l1_16k_a1,16KiB,1
l1_16k_a2,16KiB,2
l1_16k_a4,16KiB,4
l1_16k_a8,16KiB,8
l1_32k_a1,32KiB,1
l1_32k_a2,32KiB,2
l1_32k_a4,32KiB,4
l1_32k_a8,32KiB,8
l1_64k_a1,64KiB,1
l1_64k_a2,64KiB,2
l1_64k_a4,64KiB,4
l1_64k_a8,64KiB,8
```

O CSV é a fonte de verdade para a campanha. Não altere parâmetros diretamente no script de execução sem também atualizar esse arquivo.

---

## 6. Etapa prática 5 — Automatizar as execuções

Crie `scripts/executar_campanha.py`:

```python
#!/usr/bin/env python3
import csv
import pathlib
import subprocess
import sys

if len(sys.argv) != 2:
    print("uso: executar_campanha.py <raiz_do_gem5>")
    sys.exit(2)

gem5_root = pathlib.Path(sys.argv[1]).resolve()
base = gem5_root / "experiments" / "automacao"
gem5_bin = gem5_root / "build" / "X86" / "gem5.opt"
config = base / "configs" / "cache_experimento.py"
benchmark = base / "bin" / "percurso_matriz"
csv_path = base / "scripts" / "campanha.csv"
resultados = base / "resultados"

if not gem5_bin.exists():
    raise FileNotFoundError(f"gem5 não encontrado: {gem5_bin}")

with csv_path.open(newline="") as arquivo:
    for linha in csv.DictReader(arquivo):
        outdir = resultados / linha["id"]
        stats = outdir / "stats.txt"
        if stats.exists():
            print(f"[pular] {linha['id']}: stats.txt já existe")
            continue

        comando = [
            str(gem5_bin), f"--outdir={outdir}", str(config),
            f"--cmd={benchmark}",
            f"--l1d-size={linha['l1d_size']}",
            f"--l1d-assoc={linha['l1d_assoc']}",
        ]
        print("[executar]", " ".join(comando))
        subprocess.run(comando, cwd=gem5_root, check=True)
```

Torne-o executável e execute a partir da raiz do gem5:

```bash
chmod +x experiments/automacao/scripts/executar_campanha.py
experiments/automacao/scripts/executar_campanha.py .
```

O script pula diretórios que já contêm `stats.txt`. Isso permite retomar uma campanha interrompida, mas só é seguro se os diretórios existentes realmente corresponderem à mesma configuração. Para uma nova campanha, use uma nova pasta de resultados ou remova as saídas antigas conscientemente.

---

## 7. Etapa prática 6 — Extrair `stats.txt` para CSV

Crie `scripts/extrair_stats.py`:

```python
#!/usr/bin/env python3
import csv
import pathlib
import re
import sys

if len(sys.argv) != 2:
    print("uso: extrair_stats.py <raiz_do_gem5>")
    sys.exit(2)

root = pathlib.Path(sys.argv[1]).resolve()
base = root / "experiments" / "automacao"

padroes = {
    "sim_seconds": r"^simSeconds\s+([\deE.+-]+)",
    "sim_insts": r"^simInsts\s+([\deE.+-]+)",
    "ciclos": r"^system\.cpu\.numCycles\s+([\deE.+-]+)",
    "ipc": r"^system\.cpu\.ipc\s+([\deE.+-]+)",
    "miss_rate_l1d": r"^system\.cpu\.dcache\.overallMissRate::total\s+([\deE.+-]+)",
    "misses_l1d": r"^system\.cpu\.dcache\.overallMisses::total\s+([\deE.+-]+)",
}

linhas = []
with (base / "scripts" / "campanha.csv").open(newline="") as arquivo:
    for caso in csv.DictReader(arquivo):
        stats_path = base / "resultados" / caso["id"] / "stats.txt"
        if not stats_path.exists():
            print(f"[aviso] ausente: {stats_path}")
            continue
        texto = stats_path.read_text(errors="replace")
        resultado = dict(caso)
        for coluna, padrao in padroes.items():
            achado = re.search(padrao, texto, re.MULTILINE)
            resultado[coluna] = achado.group(1) if achado else ""
        linhas.append(resultado)

saida = base / "resultados_consolidados.csv"
with saida.open("w", newline="") as arquivo:
    campos = ["id", "l1d_size", "l1d_assoc"] + list(padroes)
    escritor = csv.DictWriter(arquivo, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(linhas)

print(f"CSV criado: {saida}")
```

Execute:

```bash
experiments/automacao/scripts/extrair_stats.py .
column -s, -t < experiments/automacao/resultados_consolidados.csv
```

Se uma estatística estiver vazia, confira o nome real no `stats.txt`; nomes podem variar entre versões e configurações do gem5.

---

## 8. Etapa prática 7 — Gerar gráficos

Crie `scripts/gerar_graficos.py`:

```python
#!/usr/bin/env python3
import pathlib
import sys
import matplotlib.pyplot as plt
import pandas as pd

if len(sys.argv) != 2:
    print("uso: gerar_graficos.py <raiz_do_gem5>")
    sys.exit(2)

root = pathlib.Path(sys.argv[1]).resolve()
base = root / "experiments" / "automacao"
dados = pd.read_csv(base / "resultados_consolidados.csv")
saida = base / "graficos"
saida.mkdir(exist_ok=True)

for coluna in ["sim_seconds", "ipc", "miss_rate_l1d"]:
    dados[coluna] = pd.to_numeric(dados[coluna], errors="coerce")
dados["l1d_assoc"] = pd.to_numeric(dados["l1d_assoc"])

ordem = ["16KiB", "32KiB", "64KiB"]

for metrica, titulo, ylabel, arquivo in [
    ("sim_seconds", "Tempo simulado por configuração", "Tempo simulado (s)", "tempo.png"),
    ("miss_rate_l1d", "Taxa de faltas da L1-D", "Taxa de faltas", "faltas_l1d.png"),
]:
    plt.figure(figsize=(8, 5))
    for assoc, grupo in dados.groupby("l1d_assoc"):
        grupo = grupo.set_index("l1d_size").reindex(ordem).reset_index()
        plt.plot(grupo["l1d_size"], grupo[metrica], marker="o", label=f"assoc={assoc}")
    plt.title(titulo)
    plt.xlabel("Tamanho da L1-D")
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(saida / arquivo, dpi=160)
    plt.close()

print(f"Gráficos criados em: {saida}")
```

Execute:

```bash
experiments/automacao/scripts/gerar_graficos.py .
ls experiments/automacao/graficos
```

Os gráficos devem ser acompanhados da tabela CSV. Um gráfico sem os dados e comandos que o produziram não é suficiente para reprodutibilidade.

---

## 9. Interpretação dos resultados

Procure relações entre taxa de faltas e tempo simulado. Uma redução nas faltas pode não gerar redução proporcional no tempo, pois a aplicação também possui trabalho de CPU e os acessos podem se sobrepor de maneiras diferentes conforme o modelo adotado.

A associatividade pode reduzir faltas de conflito, mas aumentá-la não é sempre benéfico: há custos de complexidade e, dependendo da carga, o efeito pode ser pequeno. Analise os resultados por tamanho e associatividade, não apenas a melhor configuração isolada.

Antes de interpretar uma diferença pequena, confirme que:

- todos os diretórios têm `stats.txt`;
- todos os `simout` apresentam o mesmo checksum;
- o CSV contém a configuração correta;
- a versão do gem5 e o binário são os mesmos em toda a campanha.

---

## 10. Exercícios

1. Inclua `LRU` e `RandomRP` como outra coluna da campanha e parâmetro da configuração.
2. Adicione gráficos de IPC e de faltas absolutas.
3. Execute a campanha com `MinorCPU` e compare os resultados em gráficos separados.
4. Faça o script salvar o comando completo e o hash do binário em cada diretório.
5. Produza uma tabela que destaque a configuração de menor tempo para cada tamanho de cache.

## Conclusão

Você automatizou o ciclo completo de uma campanha: definição de configurações, execução, coleta de estatísticas, consolidação em CSV e visualização. Essa estrutura reduz trabalho repetitivo e, principalmente, permite que resultados sejam auditados e repetidos com segurança.
