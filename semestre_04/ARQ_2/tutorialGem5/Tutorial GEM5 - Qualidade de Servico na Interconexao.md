# Tutorial GEM5 — Qualidade de Serviço na Interconexão: Priorização e Isolamento de Tráfego

## Introdução

Em sistemas multicore, aplicações compartilham caches, controladores de memória e a rede on-chip. Um workload intensivo em memória pode elevar a latência de outro workload sensível a atrasos. **Qualidade de Serviço (QoS)** busca controlar essa interferência com prioridades, filas, classes de tráfego, reservas ou limitação de injeção.

## Objetivo

Construir uma campanha de simulação que mede interferência entre aplicações e compara políticas de priorização/isolamento disponíveis na configuração de interconexão e memória do gem5.

## Pré-requisitos

- gem5 com suporte a múltiplas CPUs e, preferencialmente, Ruby/Garnet;
- dois programas compilados para a ISA alvo;
- uma configuração SE multicore que permita atribuir uma carga a cada processo;
- conhecimento do tutorial de multiprogramação e do tutorial de NoC.

## Conceitos essenciais

- **Aplicação sensível à latência**: desempenho degrada fortemente quando requisições individuais demoram mais; por exemplo, um serviço com pequenas estruturas de dados.
- **Aplicação intensiva em banda**: emite muitas requisições e pode saturar links ou DRAM.
- **Justiça**: evitar que uma aplicação seja desproporcionalmente prejudicada.
- **Prioridade**: atender uma classe antes de outra; reduz latência da classe prioritária, mas pode causar fome.
- **Isolamento**: separar recursos ou impor limites para limitar interferência.

## Etapa 1 — Criar duas cargas contrastantes

Crie a carga sensível à latência, `pointer_chase.c`:

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N (1 << 20)
#define STEPS (1 << 25)
int main(void) {
    uint32_t *next = aligned_alloc(64, N * sizeof(uint32_t));
    if (!next) return 1;
    for (uint32_t i = 0; i < N; i++) next[i] = (i * 8191u + 17u) & (N - 1);
    uint32_t p = 0;
    for (uint64_t i = 0; i < STEPS; i++) p = next[p];
    printf("resultado=%u\n", p);
    free(next);
    return 0;
}
```

Crie a carga de banda, `stream_write.c`:

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N (32 * 1024 * 1024)
#define REPS 6
int main(void) {
    uint64_t *a = aligned_alloc(64, N * sizeof(uint64_t));
    if (!a) return 1;
    for (size_t r = 0; r < REPS; r++)
        for (size_t i = 0; i < N; i += 8) a[i] = (uint64_t)i + r;
    printf("resultado=%lu\n", a[N - 8]);
    free(a);
    return 0;
}
```

Compile:

```bash
gcc -O2 -static pointer_chase.c -o pointer_chase
gcc -O2 -static stream_write.c -o stream_write
```

## Etapa 2 — Medir baselines isolados

Execute cada programa sozinho, usando a mesma CPU, caches, frequência e número de controladores que serão usados na execução conjunta. Guarde `simTicks`, ciclos, misses e tráfego de rede.

```bash
build/X86/gem5.opt --outdir=out/lat-alone \
  configs/example/se.py --cmd=./pointer_chase --cpu-type=TimingSimpleCPU \
  --num-cpus=1 --ruby --network=garnet
```

Repita para `stream_write`.

## Etapa 3 — Executar as cargas em coexecução

A maneira de fornecer múltiplos processos depende da versão do script SE. Em configurações legadas, uma opção típica é separar comandos por ponto e vírgula:

```bash
build/X86/gem5.opt --outdir=out/best-effort \
  configs/example/se.py --cmd="./pointer_chase;./stream_write" \
  --cpu-type=TimingSimpleCPU --num-cpus=2 --ruby --network=garnet
```

Se sua configuração usa a API Python, crie dois objetos de processo, atribua um a cada CPU e confirme que ambos têm contextos de execução independentes. Não compare resultados antes de validar no `simout` que as duas aplicações terminaram corretamente.

## Etapa 4 — Definir políticas de QoS

O suporte exato a QoS depende de versão, topologia e protocolo; não existe uma opção universal que habilite todas as políticas. Explore os parâmetros expostos por sua configuração:

```bash
build/X86/gem5.opt configs/example/se.py --help | grep -i -E "qos|prio|traffic|vc|buffer|throttle"
```

Avalie as alternativas que sua instalação disponibilizar, sempre contra o mesmo caso base *best effort*:

1. **Prioridade de tráfego**: atribuir maior prioridade à classe da aplicação de ponteiros.
2. **Filas/VCs separadas**: impedir que tráfego de classes distintas compartilhe integralmente o mesmo buffer.
3. **Limitação de injeção**: limitar a aplicação de streaming para preservar capacidade.
4. **Particionamento**: separar CPUs em regiões ou recursos de rede, quando a topologia permitir.

Quando um mecanismo não estiver implementado no modelo escolhido, registre-o como limitação experimental em vez de inferir seu efeito.

## Etapa 5 — Automatizar a coleta

Para cada política, salve resultados separados e extraia estatísticas:

```bash
for d in out/lat-alone out/bw-alone out/best-effort out/prioridade out/limitacao; do
  echo "=== $d ==="
  grep -E "simTicks|numCycles|average_flit_latency|packets|flits|mem_ctrl" "$d/stats.txt" | head -40
done
```

Calcule o *slowdown* de cada aplicação:

\[
Slowdown_i = \frac{T_{i,\;coexecucao}}{T_{i,\;isolado}}
\]

Uma métrica simples de justiça é:

\[
Fairness = \frac{\min_i(Slowdown_i)}{\max_i(Slowdown_i)}
\]

Quanto mais perto de 1, mais equilibrada é a degradação entre aplicações.

## Tabela de análise

| Política | Tempo latência | Tempo banda | Slowdown latência | Slowdown banda | Justiça |
|---|---:|---:|---:|---:|---:|
| Isolado |  |  | 1,00 | 1,00 | 1,00 |
| Best effort |  |  |  |  |  |
| Priorização |  |  |  |  |  |
| Limitação |  |  |  |  |  |

## Interpretação

Uma prioridade bem-sucedida deve reduzir o slowdown da carga sensível à latência. Isso pode aumentar a degradação da carga de banda; portanto, não avalie QoS apenas pelo melhor resultado individual. Verifique também utilização dos links, latência média e, se disponível, percentis de latência. Médias podem esconder picos prejudiciais a aplicações críticas.

## Ameaças à validade

- Uma carga pode terminar antes da outra, reduzindo a janela de contenção.
- Cache compartilhada pode ser a fonte de interferência, e não a NoC.
- Alterar simultaneamente topologia, largura de link e prioridade impede atribuir causalidade.
- Resultados dependem da política de escalonamento de processos e do modelo de CPU.

## Exercícios

1. Execute duas instâncias de `stream_write` e compare justiça com o caso misto.
2. Aumente controladores de memória e determine se a interferência migra da DRAM para a rede.
3. Use uma mesh maior e varie a distância entre as CPUs das duas cargas.
4. Compare prioridade fixa com limitação de banda, quando ambas forem suportadas.

## Conclusão

QoS não elimina limites físicos; ela decide como recursos escassos serão distribuídos. Uma campanha bem desenhada compara execução isolada e coexecução, mede desempenho e justiça, e documenta claramente os mecanismos realmente modelados pela configuração do gem5.
