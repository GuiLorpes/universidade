# Avaliação de algoritmos de substituição de linhas de cache associativo no gem5 com cBench

## Introdução e objetivo

Em uma cache **associativa por conjunto** (*set-associative*), cada bloco de memória pode ser colocado em uma dentre várias vias do conjunto ao qual ele pertence. Quando todas as vias do conjunto estão ocupadas e um novo bloco precisa entrar na cache, a política de substituição decide qual linha será removida.

Este tutorial mostra como comparar políticas de substituição no **gem5** usando programas do conjunto de benchmarks **cBench**, no modo **System Emulation (SE)** e por meio de um arquivo de configuração **Python**. Ao final, será possível executar a mesma carga de trabalho com políticas como **LRU**, **Random**, **Tree-PLRU** e **RRIP**, gerar diretórios de saída independentes e analisar `stats.txt` de forma comparável.

> **Escopo:** cache clássica do gem5, processador x86 simples, execução SE e API Python baseada em objetos `m5.objects`. O modo SE simula o processo de usuário; não inicializa kernel, discos nem sistema operacional completo.

---

## 1. Conceitos fundamentais

### 1.1 Cache associativa por conjunto

Uma cache possui `S` conjuntos e `A` vias por conjunto. Um endereço é dividido conceitualmente em:

- **offset:** seleciona um byte dentro do bloco;
- **índice:** seleciona um conjunto;
- **tag:** identifica qual bloco está armazenado naquele conjunto.

Se a cache tem tamanho total `C`, bloco de `B` bytes e associatividade `A`, então:

\[
S = \frac{C}{B \times A}
\]

Por exemplo, uma cache L1 de 32 KiB, blocos de 64 B e 8 vias contém:

\[
S = \frac{32\times1024}{64\times8} = 64 \text{ conjuntos}
\]

Em um *miss* que encontra todas as 8 vias do conjunto ocupadas, entra em ação a política de substituição.

### 1.2 Políticas que serão comparadas

| Política | Ideia | Característica principal |
|---|---|---|
| `lru` | Remove a linha usada há mais tempo. | Boa referência, mas exige metadados de recência. |
| `random` | Escolhe uma via aleatoriamente. | Baixo custo conceitual, comportamento variável. |
| `treeplru` | Usa uma árvore de bits para aproximar LRU. | Menor custo de hardware que LRU exato. |
| `rrip` | Prioriza linhas previstas como reutilizáveis em breve. | Pode ser eficiente para padrões de acesso específicos. |

A comparação não deve ser limitada à taxa de *miss*. Uma política pode reduzir *misses* mas ter implicações de implementação que não são modeladas integralmente nesta configuração. Neste tutorial, o foco é o **efeito no comportamento de memória simulado**.

---

## 2. Pré-requisitos

É necessário ter:

1. gem5 compilado para x86, por exemplo:

   ```bash
   scons build/X86/gem5.opt -j"$(nproc)"
   ```

2. Compilador C/C++ e ferramentas de construção:

   ```bash
   sudo apt update
   sudo apt install -y build-essential git python3
   ```

3. Uma cópia local do **cBench** (versão disponibilizada pelo projeto cTuning ou pelo ambiente da disciplina).

4. Um diretório de trabalho. Os comandos abaixo usam a seguinte organização:

   ```text
   experimento-cache/
   ├── cBench/
   ├── configs/
   │   └── se_cache_rp.py
   ├── bin/
   ├── inputs/
   └── resultados/
   ```

Crie os diretórios:

```bash
mkdir -p experimento-cache/{configs,bin,inputs,resultados}
cd experimento-cache
```

Defina também uma variável para a raiz do gem5:

```bash
export GEM5_HOME=/caminho/para/gem5
```

Confirme que o binário existe:

```bash
ls "$GEM5_HOME/build/X86/gem5.opt"
```

---

## 3. Preparar o cBench

### 3.1 O que é o cBench

O cBench é um conjunto de programas C voltado à avaliação de compiladores e sistemas. Ele contém aplicações com perfis de memória distintos, o que o torna adequado para investigar caches. Em vez de concluir algo a partir de um único programa, execute uma **suite de benchmarks**.

Boas opções iniciais incluem:

- `automotive/basicmath` — perfil computacional simples;
- `network/dijkstra` — estruturas de dados e acessos menos regulares;
- `office/stringsearch1` ou `office/stringsearch2` — pesquisa em dados;
- `consumer_jpeg` — processamento de imagem;
- `automotive/susan` — processamento de imagem com maior pressão de memória.

Os nomes exatos de diretórios, executáveis e arquivos de entrada podem mudar entre distribuições do cBench. Verifique os arquivos `README`, `Makefile` e scripts presentes na cópia obtida antes de prosseguir.

### 3.2 Obter e localizar a suite

Obtenha uma distribuição do cBench por meio do repositório ou pacote indicado pelo seu curso/projeto e extraia-a dentro de `experimento-cache/cBench`. A estrutura esperada é semelhante a:

```text
cBench/
├── automotive/
│   ├── basicmath/
│   └── susan/
├── consumer/
│   └── jpeg/
├── network/
│   └── dijkstra/
└── office/
    └── stringsearch1/
```

Liste os diretórios disponíveis:

```bash
find cBench -maxdepth 2 -type d | sort | head -50
```

### 3.3 Compilar um benchmark para X86/SE

Para executar em `build/X86/gem5.opt`, o executável deve ser compatível com a ISA x86. Em um computador x86-64, uma compilação nativa estática costuma funcionar em SE:

```bash
cd cBench/automotive/basicmath
make clean
make CC=gcc CFLAGS='-O2 -static'
```

Se o `Makefile` não respeitar `CC` e `CFLAGS`, identifique o comando de compilação e gere o binário manualmente. Um padrão possível é:

```bash
gcc -O2 -static -o basicmath *.c -lm
```

Copie o executável final para o diretório de experimentos. Ajuste `basicmath` ao nome que a sua versão produziu:

```bash
cp ./basicmath ../../../bin/basicmath
file ../../../bin/basicmath
```

A saída de `file` deve indicar um executável x86/x86-64. Para uma simulação com `X86`, não use um binário ARM ou RISC-V.

> Se a ligação estática falhar por indisponibilidade de bibliotecas estáticas, instale os pacotes de desenvolvimento apropriados da sua distribuição ou compile dinamicamente. Para reduzir problemas de bibliotecas no SE, prefira binários estáticos quando possível.

### 3.4 Preparar entradas e medir a referência nativa

Alguns programas do cBench não usam arquivo de entrada; outros exigem argumentos e arquivos. Copie para `inputs/` os dados definidos pela suite e registre o comando exato. Por exemplo:

```bash
cp cBench/automotive/basicmath/<arquivo-de-entrada> inputs/ 2>/dev/null || true
```

Antes de simular, valide o benchmark no host:

```bash
./bin/basicmath
printf 'Código de saída: %s\n' "$?"
```

Para um benchmark que precisa de entrada, use o comando especificado pelo cBench, por exemplo:

```bash
./bin/<programa> < ./inputs/<entrada>
```

Essa validação separa problemas de compilação ou de dados de entrada de problemas da configuração do gem5.

---

## 4. Desenho experimental

Para atribuir diferenças de resultado à política de substituição, mantenha **todos os demais fatores constantes**.

### 4.1 Configuração-base proposta

| Parâmetro | Valor inicial | Justificativa |
|---|---:|---|
| ISA | X86 | Compatível com o binário compilado no host x86. |
| Modo | SE | Não requer imagem de disco ou kernel. |
| CPU | `TimingSimpleCPU` | Produz tráfego temporizado à cache. |
| L1 de instruções | 32 KiB, 8 vias | Mantida fixa. |
| L1 de dados | 32 KiB, 8 vias | Cache sob estudo. |
| Linha de cache | 64 B | Valor comum e mantido fixo. |
| Memória | DDR3-1600, 512 MiB | Mesmo subsistema para todos os testes. |
| Frequência | 2 GHz | Mantida fixa. |

O experimento principal altera **somente** `replacement_policy` da L1 de dados. Não altere simultaneamente tamanho, associatividade, CPU, frequência ou dados de entrada.

### 4.2 Repetições

`RandomRP` é não determinística. Execute-a pelo menos três vezes com o mesmo benchmark e registre média e dispersão. Para LRU, Tree-PLRU e RRIP, uma execução pode ser reproduzível sob condições iguais, mas repetições ainda ajudam a verificar a automação.

---

## 5. Etapa prática 1 — criar a configuração Python

Crie o arquivo `configs/se_cache_rp.py` com o conteúdo abaixo.

```python
# configs/se_cache_rp.py
# Executa um processo no modo SE e troca a política da L1 de dados.

import argparse

import m5
from m5.objects import (
    AddrRange,
    Cache,
    DDR3_1600_8x8,
    L2XBar,
    LRURP,
    MemCtrl,
    Process,
    RandomRP,
    Root,
    RRIPRP,
    SEWorkload,
    SrcClockDomain,
    System,
    SystemXBar,
    TimingSimpleCPU,
    TreePLRURP,
    VoltageDomain,
)


class L1ICache(Cache):
    """Cache L1 de instruções, mantida fixa no experimento."""

    def __init__(self):
        super().__init__()
        self.size = "32KiB"
        self.assoc = 8
        self.tag_latency = 1
        self.data_latency = 1
        self.response_latency = 1
        self.mshrs = 4
        self.tgts_per_mshr = 20


class L1DCache(Cache):
    """Cache L1 de dados cuja política é definida por argumento."""

    def __init__(self, replacement_policy):
        super().__init__()
        self.size = "32KiB"
        self.assoc = 8
        self.tag_latency = 1
        self.data_latency = 1
        self.response_latency = 1
        self.mshrs = 4
        self.tgts_per_mshr = 20
        self.replacement_policy = replacement_policy


def selecionar_politica(nome):
    """Cria o SimObject que implementa a política solicitada."""
    politicas = {
        "lru": LRURP,
        "random": RandomRP,
        "treeplru": TreePLRURP,
        "rrip": RRIPRP,
    }

    if nome not in politicas:
        nomes_validos = ", ".join(politicas)
        raise ValueError(f"Política inválida: {nome}. Use: {nomes_validos}")

    return politicas[nome]()


def conectar_cache_l1(cpu, barramento, politica):
    """Cria e conecta as caches privadas da CPU ao barramento do sistema."""
    icache = L1ICache()
    dcache = L1DCache(politica)

    cpu.icache_port = icache.cpu_side
    cpu.dcache_port = dcache.cpu_side
    icache.mem_side = barramento.cpu_side_ports
    dcache.mem_side = barramento.cpu_side_ports

    # A CPU precisa de portas para interrupções em X86.
    cpu.createInterruptController()
    cpu.interrupts[0].pio = barramento.mem_side_ports
    cpu.interrupts[0].int_requestor = barramento.cpu_side_ports
    cpu.interrupts[0].int_responder = barramento.mem_side_ports


def main():
    parser = argparse.ArgumentParser(
        description="gem5 SE: comparação de políticas de substituição da L1D"
    )
    parser.add_argument("--cmd", required=True, help="Caminho do executável do benchmark")
    parser.add_argument(
        "--policy",
        default="lru",
        choices=["lru", "random", "treeplru", "rrip"],
        help="Política da cache L1 de dados",
    )
    parser.add_argument(
        "--options",
        default="",
        help="Argumentos do programa, em uma única string",
    )
    parser.add_argument(
        "--stdin",
        default="",
        help="Arquivo a fornecer como entrada padrão do processo",
    )
    args = parser.parse_args()

    system = System()
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = "2GHz"
    system.clk_domain.voltage_domain = VoltageDomain()
    system.mem_mode = "timing"
    system.mem_ranges = [AddrRange("512MiB")]

    system.cpu = TimingSimpleCPU()
    system.membus = SystemXBar()
    system.cpu.createThreads()

    politica = selecionar_politica(args.policy)
    conectar_cache_l1(system.cpu, system.membus, politica)

    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR3_1600_8x8()
    system.mem_ctrl.dram.range = system.mem_ranges[0]
    system.mem_ctrl.port = system.membus.mem_side_ports

    processo = Process()
    processo.cmd = [args.cmd] + args.options.split()
    if args.stdin:
        processo.input = args.stdin

    system.workload = SEWorkload.init_compatible(args.cmd)
    system.cpu.workload = processo

    root = Root(full_system=False, system=system)
    m5.instantiate()

    print("=" * 72)
    print(f"Benchmark: {args.cmd}")
    print(f"Política da L1D: {args.policy}")
    print(f"Comando simulado: {' '.join(processo.cmd)}")
    print("=" * 72)

    evento = m5.simulate()
    print(f"Fim da simulação em tick {m5.curTick()}: {evento.getCause()}")


if __name__ == "__main__":
    main()
```

### 5.1 Entender os pontos essenciais do arquivo

- `class L1DCache(Cache)`: define a cache L1 de dados.
- `self.assoc = 8`: torna a L1D associativa por conjunto com 8 vias. Uma política de substituição só é exercitada quando um conjunto precisa desalojar uma linha.
- `self.replacement_policy = replacement_policy`: associa à L1D o objeto de política recebido.
- `selecionar_politica()`: traduz o argumento de linha de comando (`lru`, `random`, etc.) para um objeto do gem5, como `LRURP()`.
- `system.mem_mode = "timing"`: usa o modo temporizado, apropriado para observar estatísticas de hierarquia de memória. Não use `atomic` neste experimento.
- `SEWorkload.init_compatible(args.cmd)`: prepara a carga para a execução de processo no modo SE.

A política é aplicada somente à **L1D**. A L1I e a memória permanecem as mesmas em todos os ensaios, isolando a variável experimental.

### 5.2 Verificar as políticas disponíveis na sua versão

As políticas suportadas podem variar com a versão do gem5. Inspecione os objetos disponíveis:

```bash
grep -R "class .*RP" "$GEM5_HOME/src/mem/cache/replacement_policies" -n | head -30
```

Se `RRIPRP` não estiver presente ou tiver outro nome na sua versão, remova temporariamente `rrip` do dicionário, da lista `choices` e da tabela de comparação. Execute primeiro com `lru`, `random` e `treeplru`.

---

## 6. Etapa prática 2 — executar uma simulação de teste

Volte à raiz do experimento e execute `basicmath` com LRU:

```bash
cd experimento-cache
"$GEM5_HOME/build/X86/gem5.opt" \
  --outdir=resultados/basicmath-lru \
  configs/se_cache_rp.py \
  --cmd="$(pwd)/bin/basicmath" \
  --policy=lru
```

A separação é importante:

- argumentos **antes** de `configs/se_cache_rp.py` pertencem ao executável `gem5.opt`, como `--outdir`;
- argumentos **depois** do arquivo Python pertencem à configuração criada no tutorial.

Ao final, confirme o motivo de parada e os arquivos produzidos:

```bash
tail -20 resultados/basicmath-lru/simout
test -f resultados/basicmath-lru/stats.txt && echo "stats.txt criado"
```

Uma finalização esperada normalmente menciona a saída normal do processo simulado. Erros de carregamento de binário, bibliotecas ou argumentos precisam ser corrigidos antes da coleta de resultados.

---

## 7. Etapa prática 3 — executar todas as políticas

Use o mesmo binário e as mesmas opções em todas as execuções:

```bash
for politica in lru random treeplru rrip; do
  "$GEM5_HOME/build/X86/gem5.opt" \
    --outdir="resultados/basicmath-${politica}" \
    configs/se_cache_rp.py \
    --cmd="$(pwd)/bin/basicmath" \
    --policy="$politica"
done
```

Para um benchmark com argumentos, repita a mesma string de argumentos em cada rodada. Exemplo genérico:

```bash
"$GEM5_HOME/build/X86/gem5.opt" \
  --outdir=resultados/dijkstra-lru \
  configs/se_cache_rp.py \
  --cmd="$(pwd)/bin/dijkstra" \
  --options="$(pwd)/inputs/grafo.dat" \
  --policy=lru
```

Para um benchmark que lê a entrada padrão:

```bash
"$GEM5_HOME/build/X86/gem5.opt" \
  --outdir=resultados/stringsearch-lru \
  configs/se_cache_rp.py \
  --cmd="$(pwd)/bin/stringsearch" \
  --stdin="$(pwd)/inputs/texto.txt" \
  --policy=lru
```

> Use os argumentos, arquivos e formato de entrada documentados para o benchmark específico da sua distribuição do cBench. Não compare execuções que processaram entradas diferentes.

### 7.1 Repetir a política aleatória

Para `random`, faça três execuções independentes:

```bash
for repeticao in 1 2 3; do
  "$GEM5_HOME/build/X86/gem5.opt" \
    --outdir="resultados/basicmath-random-r${repeticao}" \
    configs/se_cache_rp.py \
    --cmd="$(pwd)/bin/basicmath" \
    --policy=random
done
```

Registre cada repetição como uma observação distinta. Ao apresentar o resultado de `random`, informe média e desvio padrão, em vez de selecionar apenas a melhor execução.

---

## 8. Etapa prática 4 — extrair e calcular métricas

### 8.1 Estatísticas importantes

Em `stats.txt`, os nomes podem ter pequenas variações entre versões, mas os seguintes campos são usuais:

| Estatística | Interpretação |
|---|---|
| `simTicks` | Tempo simulado em ticks. |
| `simSeconds` | Tempo simulado em segundos. |
| `system.cpu.numCycles` | Ciclos da CPU. |
| `system.cpu.committedInsts` | Instruções efetivamente concluídas. |
| `system.cpu.ipc` | Instruções por ciclo. |
| `system.cpu.dcache.overallHits::total` | Acessos que acertaram na L1D. |
| `system.cpu.dcache.overallMisses::total` | *Misses* na L1D. |
| `system.cpu.dcache.overallAccesses::total` | Total de acessos à L1D. |
| `system.cpu.dcache.demandMissRate::total` | Taxa de *misses* de demanda, quando disponível. |

Procure as métricas de cache em uma execução:

```bash
grep -E 'dcache.*(overall|demand).*::total|simSeconds|numCycles|committedInsts|\.ipc' \
  resultados/basicmath-lru/stats.txt
```

> A árvore de nomes pode mudar conforme a versão e a configuração. Se o comando não encontrar campos, use `grep -i dcache resultados/basicmath-lru/stats.txt | head -80` para descobrir os nomes presentes no seu arquivo.

### 8.2 Calcular a taxa de misses

Quando houver contadores de acessos e misses, calcule:

\[
\text{miss rate} = \frac{\text{overallMisses}}{\text{overallAccesses}}
\]

Em percentual:

\[
\text{miss rate (\%)} = 100 \times \frac{\text{misses}}{\text{acessos}}
\]

Não some estatísticas de diretórios diferentes nem use valores de uma linha `::total` junto com subtotais por tipo de acesso. Use uma única convenção de contagem para todas as políticas.

### 8.3 Gerar uma tabela CSV simples

O script abaixo coleta valores quando os nomes de estatística são os esperados. Salve-o como `extrair_resultados.sh` na raiz do experimento:

```bash
#!/usr/bin/env bash
set -euo pipefail

printf 'benchmark,politica,sim_seconds,ciclos,instrucoes,ipc,l1d_acessos,l1d_misses\n'

for diretorio in resultados/*; do
  arquivo="$diretorio/stats.txt"
  [ -f "$arquivo" ] || continue

  nome=$(basename "$diretorio")
  benchmark=${nome%-*}
  politica=${nome##*-}

  valor() {
    awk -v chave="$1" '$1 == chave { print $2; exit }' "$arquivo"
  }

  sim_seconds=$(valor simSeconds)
  ciclos=$(valor system.cpu.numCycles)
  instrucoes=$(valor system.cpu.committedInsts)
  ipc=$(valor system.cpu.ipc)
  acessos=$(valor system.cpu.dcache.overallAccesses::total)
  misses=$(valor system.cpu.dcache.overallMisses::total)

  printf '%s,%s,%s,%s,%s,%s,%s,%s\n' \
    "$benchmark" "$politica" "$sim_seconds" "$ciclos" "$instrucoes" "$ipc" "$acessos" "$misses"
done
```

Dê permissão e produza o CSV:

```bash
chmod +x extrair_resultados.sh
./extrair_resultados.sh > resultados.csv
column -s, -t resultados.csv
```

Se algum campo estiver vazio, localize o nome correto no `stats.txt` e substitua a chave no script. Isso é preferível a preencher valores manualmente.

### 8.4 Exemplo de tabela para relatório

| Benchmark | Política | Acessos L1D | Misses L1D | Miss rate | Ciclos | IPC |
|---|---:|---:|---:|---:|---:|---:|
| basicmath | LRU | ... | ... | ... | ... | ... |
| basicmath | Random | ... | ... | ... | ... | ... |
| basicmath | Tree-PLRU | ... | ... | ... | ... | ... |
| basicmath | RRIP | ... | ... | ... | ... | ... |

Preencha a tabela somente com resultados coletados. Não espere que uma política vença em todos os benchmarks: a localidade temporal e espacial de cada programa influencia o resultado.

---

## 9. Como interpretar os resultados

### 9.1 Comparação correta

Para cada benchmark, compare:

1. **taxa de misses da L1D** — mede diretamente o efeito observado na cache sob estudo;
2. **número de ciclos** ou `simSeconds` — mostra a consequência no desempenho simulado;
3. **IPC** — ajuda a relacionar atrasos de memória com progresso da CPU;
4. **instruções concluídas** — deve ser igual entre execuções equivalentes. Se não for, investigue entrada, término ou erro antes de comparar desempenho.

Calcule o *speedup* de uma política `P` em relação à LRU usando ciclos:

\[
\text{speedup}_{P/LRU} = \frac{\text{ciclos}_{LRU}}{\text{ciclos}_{P}}
\]

- Valor maior que 1: `P` foi mais rápida que LRU nessa carga e configuração.
- Valor menor que 1: `P` foi mais lenta.

### 9.2 Conclusões que são justificadas

Uma conclusão apropriada é:

> “Com L1D de 32 KiB, 8 vias, linhas de 64 B, `TimingSimpleCPU` e a entrada X do benchmark Y, Tree-PLRU apresentou menor taxa de misses que Random e reduziu os ciclos em Z% em relação a LRU.”

Evite concluir que uma política é “a melhor” de forma universal. O resultado depende de tamanho e associatividade da cache, linhas, pré-busca, latências, CPU, entradas e do padrão de referências do programa.

### 9.3 Sinais de problema experimental

Revise o experimento se observar algum dos casos abaixo:

- o programa termina por falha, mas ainda existe `stats.txt`;
- o total de instruções é muito diferente entre políticas;
- os diretórios de saída foram reutilizados e misturaram arquivos de execuções distintas;
- a entrada ou os argumentos diferem entre políticas;
- múltiplos parâmetros de cache foram alterados ao mesmo tempo;
- foi usado `AtomicSimpleCPU` ou `mem_mode = "atomic"` para inferir tempo de execução;
- o benchmark é tão pequeno que quase não há *replacements* na L1D.

---

## 10. Extensões recomendadas

Depois do experimento-base, altere **uma variável por vez** e refaça toda a comparação:

1. **Associatividade:** compare 2, 4, 8 e 16 vias, mantendo 32 KiB. Isso altera o número de conjuntos e a frequência de conflitos.
2. **Tamanho da L1D:** compare 16, 32 e 64 KiB, mantendo a associatividade.
3. **Conjunto de benchmarks:** execute pelo menos três aplicações do cBench com perfis de acesso diferentes.
4. **Políticas RRIP:** se a sua versão fornecer variantes como BRRIP ou DRRIP, inclua-as e documente seus parâmetros.
5. **Cache L2:** adicione uma L2 compartilhada, mas mantenha sua política fixa ao estudar a L1D. Em um experimento separado, estude a L2.

Para mudar associatividade, ajuste apenas a linha abaixo em `L1DCache`:

```python
self.assoc = 8
```

Use um novo conjunto de diretórios de saída que identifique também a associatividade, por exemplo `resultados/dijkstra-lru-a4/`.

---

## 11. Checklist de reprodutibilidade

Antes de entregar ou publicar resultados, registre:

- versão e *commit* do gem5: `git -C "$GEM5_HOME" rev-parse HEAD`;
- versão/origem do cBench;
- compilador e opções: `gcc --version` e `-O2 -static`;
- ISA alvo e modo SE;
- arquivo Python exato utilizado;
- tamanho, associatividade, linha e latências da L1D;
- política avaliada e parâmetros, se houver;
- benchmark, argumentos e arquivo de entrada;
- número de repetições, especialmente para Random;
- métricas, fórmula e método de agregação usados.

---

## Conclusão

Você criou uma configuração Python de modo SE na qual a **única variável principal é a política de substituição da L1 de dados**. Com o cBench, é possível aplicar essa configuração a cargas de trabalho variadas, coletar dados em `stats.txt` e construir uma comparação fundamentada entre LRU, Random, Tree-PLRU e RRIP. O valor do experimento está no controle das variáveis, na repetição e na interpretação conjunta de *miss rate*, ciclos e IPC.
