# Tutorial GEM5 — Simulação de GPUs

## Introdução
O gem5 pode modelar sistemas CPU–GPU, mas o suporte a GPU depende da versão compilada e da integração disponível (por exemplo, modelos baseados em AMD GCN). Este tutorial apresenta uma campanha inicial de simulação, com foco em configuração, execução e leitura das métricas.

## Objetivo
Executar uma carga paralela suportada pela instalação, variar a configuração da GPU e avaliar desempenho e pressão sobre a memória.

## Pré-requisitos
- gem5 compilado com o suporte GPU documentado pela versão utilizada;
- runtime, imagem ou benchmark compatível com esse suporte;
- uma carga de teste GPU validada pelo repositório da instalação.

> **Nota:** interfaces e scripts de GPU variam significativamente entre versões. Antes de criar uma configuração própria, valide um exemplo oficial da árvore `configs` da sua versão.

## Conceitos
Uma GPU executa muitos *threads* organizados em grupos de trabalho. A configuração relevante inclui unidades de computação, número de *wavefronts*, caches próximos à GPU, memória e interconexão CPU–GPU. Aumentar paralelismo pode reduzir o tempo, mas também saturar memória.

## Prática

### Etapa 1 — Identificar os exemplos disponíveis
Na raiz do gem5, localize configurações e testes de GPU:

```bash
find configs tests -iname '*gpu*' -o -iname '*gcn*'
```

Leia o `README` associado e registre o comando recomendado para a sua revisão.

### Etapa 2 — Validar uma execução de referência
Crie uma área de resultados e execute o exemplo oficial sem alterar parâmetros:

```bash
mkdir -p resultados/gpu/base
# Substitua <script-oficial> e os argumentos pelo exemplo da sua versão
build/NULL/gem5.opt <script-oficial> --outdir=resultados/gpu/base <argumentos-da-carga>
```

O alvo de build não é necessariamente `NULL`; use o indicado pela documentação do exemplo.

### Etapa 3 — Definir o experimento
Escolha uma carga com paralelismo de dados, como multiplicação de matrizes ou *vector add*. Mantenha fixos: entrada, binário, frequência e memória. Varie somente uma dimensão por vez:

| Configuração | Unidades de computação | Finalidade |
|---|---:|---|
| `cu4` | 4 | referência |
| `cu8` | 8 | paralelismo intermediário |
| `cu16` | 16 | verificar saturação |

### Etapa 4 — Parametrizar o script Python
No script oficial, exponha o parâmetro correspondente à quantidade de unidades de computação. O nome exato é dependente da configuração; preserve a construção de objetos já validada e acrescente um argumento:

```python
parser.add_argument("--num-cu", type=int, default=4)
args = parser.parse_args()
# Atribua args.num_cu ao campo de unidades de computação usado pelo script oficial.
```

Não misture modelos incompatíveis de CPU, GPU ou protocolo de memória.

### Etapa 5 — Executar a campanha

```bash
for cu in 4 8 16; do
  dir="resultados/gpu/cu${cu}"
  mkdir -p "$dir"
  build/NULL/gem5.opt configs/exemplo_gpu.py \
    --outdir="$dir" --num-cu="$cu" <argumentos-da-carga>
done
```

### Etapa 6 — Coletar métricas
Em cada `stats.txt`, procure `simTicks`, `simSeconds`, estatísticas de memória e contadores específicos da GPU. Os nomes exatos dependem do modelo; liste-os com:

```bash
grep -Ei 'gpu|gcn|dram|mem|simSeconds|simTicks' resultados/gpu/cu4/stats.txt | head -80
```

Consolide em uma tabela com tempo simulado, acessos à memória, latência média e utilização, quando disponível.

## Análise
Calcule o *speedup* relativo à configuração de 4 unidades:

\[
Speedup(n)=\frac{T_{4}}{T_n}
\]

Se o *speedup* deixar de crescer enquanto acessos ou latência de memória aumentam, a carga provavelmente está limitada pela memória. Se a utilização das unidades cair, verifique tamanho do problema, ocupação e sincronizações.

## Boas práticas
- Faça uma execução curta para validar a carga antes da campanha completa.
- Mantenha a mesma entrada e a mesma semente quando houver aleatoriedade.
- Registre a revisão do gem5 e o comando completo de cada resultado.
- Não compare valores de modelos de GPU distintos como se fossem diretamente equivalentes.

## Exercícios
1. Compare 4, 8 e 16 unidades de computação para duas entradas.
2. Varie o tamanho de cache próximo à GPU, se o modelo o expuser.
3. Explique com métricas por que o *speedup* observado é sublinear ou superlinear.