# Tutorial GEM5 — Topologias Hierárquicas para Muitos Núcleos

## Introdução

Uma malha 2D plana é uma escolha comum para sistemas *manycore*, mas seu custo cresce com a distância entre roteadores e com a contenção global. Topologias hierárquicas agrupam núcleos em clusters locais e conectam esses clusters por uma rede de nível superior. A ideia é explorar localidade sem perder escalabilidade.

## Objetivo

Projetar e avaliar, com gem5 e Garnet, uma organização de 16 núcleos baseada em clusters. Comparar uma mesh plana com uma alternativa hierárquica em termos de latência, tráfego entre clusters e desempenho de workloads paralelos.

## Pré-requisitos

- gem5 compilado com Ruby e Garnet;
- benchmark multithread compilado para a ISA alvo;
- familiaridade com controladores Ruby, roteadores e links da NoC;
- um script de configuração Python para sistemas multicore.

## Conceitos essenciais

- **Mesh plana**: todos os roteadores pertencem à mesma malha; a distância cresce com o número de saltos.
- **Cluster**: subconjunto de CPUs, caches e roteadores com comunicação local frequente.
- **Rede global**: conecta clusters e transporta somente tráfego remoto.
- **Concentração**: vários nós compartilham um roteador; reduz roteadores, mas pode criar gargalos.
- **Bisseção**: largura de banda disponível ao dividir a rede em duas partes; influencia escalabilidade.

## Etapa 1 — Escolher o benchmark

Use um programa com compartilhamento controlável. O exemplo abaixo calcula um histograma paralelo; os contadores por thread reduzem contenção, enquanto a fase final agrega resultados.

```c
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N (8 * 1024 * 1024)
#define BINS 256
#define MAX_T 16
unsigned char *input;
unsigned long partial[MAX_T][BINS];
int nt;

typedef struct { int id; } arg_t;
void *worker(void *p) {
    int id = ((arg_t *)p)->id;
    size_t begin = (N / nt) * id, end = (id == nt - 1) ? N : begin + N / nt;
    for (size_t i = begin; i < end; i++) partial[id][input[i]]++;
    return NULL;
}
int main(int argc, char **argv) {
    nt = argc > 1 ? atoi(argv[1]) : 4;
    input = malloc(N);
    for (size_t i = 0; i < N; i++) input[i] = (unsigned char)((i * 17) & 255);
    pthread_t th[MAX_T]; arg_t a[MAX_T];
    for (int i = 0; i < nt; i++) { a[i].id = i; pthread_create(&th[i], 0, worker, &a[i]); }
    for (int i = 0; i < nt; i++) pthread_join(th[i], 0);
    unsigned long total = 0;
    for (int t = 0; t < nt; t++) for (int b = 0; b < BINS; b++) total += partial[t][b];
    printf("total=%lu esperado=%d\n", total, N);
    return total != N;
}
```

Compile:

```bash
gcc -O2 -static -pthread histogram.c -o histogram
```

## Etapa 2 — Criar o caso base: mesh plana

Configure 16 CPUs, uma L1 privada por CPU, L2 compartilhada ou *slices* distribuídos, controladores de memória e uma mesh 4×4. Fixe:

- modelo de CPU;
- tamanho e associatividade de caches;
- frequência;
- número de controladores de memória;
- protocolo Ruby;
- número de *virtual networks* e largura de links.

Execute o benchmark com 16 threads e salve em `out/mesh-plana`.

## Etapa 3 — Modelar a organização hierárquica

Divida os 16 núcleos em quatro clusters de quatro CPUs. Há duas estratégias práticas:

1. **Dois níveis explícitos**: uma pequena rede local em cada cluster e roteadores de gateway conectados por uma rede global. Essa alternativa requer uma topologia Python personalizada em Garnet.
2. **Aproximação por clusters em mesh**: mantenha a mesh física, posicione CPUs e bancos de L2 por cluster, e altere latências/larguras de links de fronteira. É mais simples e útil para estudos iniciais, mas não representa duas redes independentes.

Em ambos os casos, associe cada cluster a uma região de L2 e, quando possível, preserve afinidade entre threads e dados. Nomeie roteadores e links para separar estatísticas locais e globais.

Esqueleto conceitual de uma topologia Python:

```python
# Pseudocódigo estrutural: adapte às classes da sua versão do gem5.
clusters = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
for cluster_id, cpus in enumerate(clusters):
    criar_roteadores_locais(cluster_id, cpus)
    conectar_cpu_a_cluster(cluster_id, cpus)
    conectar_l2_local(cluster_id)
conectar_gateways_em_mesh_2x2()
conectar_memoria_a_rede_global()
```

Não copie esse pseudocódigo como configuração executável: os construtores de controladores e links variam por versão e protocolo Ruby.

## Etapa 4 — Executar cenários de localidade

Rode ao menos três variantes do workload:

1. **Local**: cada thread processa dados e atualiza estruturas do próprio cluster.
2. **Misto**: parte dos dados é compartilhada entre clusters vizinhos.
3. **Global**: todas as threads atualizam uma estrutura comum.

Isso evita uma conclusão baseada em um único padrão de comunicação.

## Etapa 5 — Coletar e comparar métricas

```bash
grep -E "simTicks|numCycles|network|average_flit_latency|packets|flits" out/mesh-plana/stats.txt
grep -E "simTicks|numCycles|network|average_flit_latency|packets|flits" out/hierarquica/stats.txt
```

Monte uma tabela:

| Configuração | Cenário | Ciclos | Latência média | Flits/packets | Observação |
|---|---|---:|---:|---:|---|
| Mesh plana | Local |  |  |  |  |
| Hierárquica | Local |  |  |  |  |
| Mesh plana | Global |  |  |  |  |
| Hierárquica | Global |  |  |  |  |

## Interpretação

A topologia hierárquica tende a beneficiar comunicação predominantemente local, pois reduz competição na rede global. Em comunicação global intensa, gateways podem virar gargalos e a mesh plana pode ser competitiva. Compare percentis ou distribuição de latência, se disponíveis, além da média: congestionamento frequentemente aparece primeiro na cauda.

## Exercícios

1. Compare clusters de 2, 4 e 8 núcleos mantendo 16 CPUs totais.
2. Varie a largura dos links globais e encontre o ponto de saturação.
3. Posicione controladores de memória nos gateways e depois nas bordas da rede.
4. Use um benchmark de falsa compartilhação para observar tráfego de coerência entre clusters.

## Conclusão

Hierarquia é uma troca entre localidade e capacidade de comunicação global. Para avaliá-la corretamente, deve-se controlar topologia, mapeamento de dados, padrão de comunicação e capacidade dos links de fronteira.
