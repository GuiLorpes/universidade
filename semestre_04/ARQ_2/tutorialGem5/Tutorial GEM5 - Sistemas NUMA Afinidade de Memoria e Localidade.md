# Tutorial GEM5 — Sistemas NUMA: Afinidade de Memória e Localidade

## Introdução

Em uma arquitetura **NUMA** (*Non-Uniform Memory Access*), a latência e a largura de banda de acesso à memória dependem do nó em que a página está localizada e do núcleo que realiza o acesso. Diferentemente de um sistema UMA, a memória não tem custo uniforme para todos os processadores.

## Objetivo

Modelar uma plataforma com múltiplos domínios de memória, construir um benchmark paralelo sensível a localidade e comparar acessos locais, remotos e distribuição intercalada de dados.

## Pré-requisitos

- gem5 com suporte à ISA escolhida, preferencialmente X86 ou ARM;
- uma imagem Linux para Full System, recomendada para políticas reais de alocação NUMA;
- noções de páginas, afinidade de CPU e threads POSIX.

## SE versus FS

No modo **SE**, o gem5 emula processos e não reproduz integralmente a política de páginas do kernel. É útil para criar uma topologia com diferentes distâncias e executar microbenchmarks, mas políticas como `numactl --membind` exigem um sistema operacional. Para avaliar afinidade e alocação de páginas de modo realista, utilize **FS**.

## Conceitos essenciais

- **Nó NUMA**: grupo de CPUs e memória com proximidade comum.
- **Acesso local**: CPU acessa memória do seu próprio nó.
- **Acesso remoto**: requisição atravessa uma interconexão até outro nó.
- **First touch**: em muitos SOs, a página é alocada no nó da CPU que primeiro a escreve.
- **Interleaving**: páginas são distribuídas entre nós, favorecendo largura de banda agregada, mas aumentando parte dos acessos remotos.

## Etapa 1 — Preparar o benchmark

Crie `numa_stride.c`:

```c
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N (64 * 1024 * 1024)
#define REPS 8

long *data;
int nthreads;

typedef struct { int id; } arg_t;

void *worker(void *p) {
    int id = ((arg_t *)p)->id;
    size_t begin = (N / nthreads) * id;
    size_t end = (id == nthreads - 1) ? N : begin + N / nthreads;
    long sum = 0;
    for (int r = 0; r < REPS; r++)
        for (size_t i = begin; i < end; i += 8) sum += data[i];
    return (void *)(uintptr_t)sum;
}

int main(int argc, char **argv) {
    if (argc != 2) return 1;
    nthreads = atoi(argv[1]);
    data = aligned_alloc(4096, N * sizeof(long));
    if (!data) return 2;
    for (size_t i = 0; i < N; i++) data[i] = (long)(i & 255);
    pthread_t th[16]; arg_t args[16];
    for (int i = 0; i < nthreads; i++) {
        args[i].id = i;
        pthread_create(&th[i], NULL, worker, &args[i]);
    }
    unsigned long total = 0;
    for (int i = 0; i < nthreads; i++) {
        void *r; pthread_join(th[i], &r); total += (uintptr_t)r;
    }
    printf("threads=%d checksum=%lu\n", nthreads, total);
    free(data);
    return 0;
}
```

Compile para o sistema convidado:

```bash
gcc -O2 -pthread numa_stride.c -o numa_stride
```

## Etapa 2 — Construir uma plataforma NUMA

Uma configuração NUMA requer, conceitualmente:

1. dois ou mais grupos de CPUs;
2. um controlador de memória por nó;
3. intervalos de endereços associados aos controladores;
4. links locais mais curtos/rápidos e links remotos mais caros;
5. caches e coerência compatíveis com o número de núcleos.

No gem5, essa topologia é normalmente implementada em um script Python específico, conectando *boards* ou controladores ao sistema de interconexão. Não basta aumentar `--num-cpus`: é necessário que o mapeamento de endereços e as latências diferenciem nós.

Use como ponto de partida a configuração de sistema multiprocessado/NoC já empregada na coleção e crie dois domínios: CPUs 0–3 próximos à memória 0 e CPUs 4–7 próximos à memória 1. Documente explicitamente latências e faixas físicas escolhidas.

## Etapa 3 — Executar em Full System

Copie o binário para a imagem e inicialize o sistema com oito CPUs. Dentro do convidado, verifique a topologia:

```bash
lscpu
numactl --hardware
```

Instale `numactl` na imagem, se necessário. Execute com memória e CPUs no mesmo nó:

```bash
numactl --cpunodebind=0 --membind=0 ./numa_stride 4
```

Agora force acesso remoto:

```bash
numactl --cpunodebind=0 --membind=1 ./numa_stride 4
```

E teste interleaving:

```bash
numactl --cpunodebind=0 --interleave=all ./numa_stride 4
```

Use checkpoints de boot para não incluir a inicialização do Linux nas comparações.

## Etapa 4 — Coletar dados

No host, preserve um diretório de saída por política. Em `stats.txt`, procure ciclos, misses de cache, estatísticas dos controladores e da rede:

```bash
grep -E "simTicks|numCycles|overall_misses|mem_ctrl|network" m5out/stats.txt
```

No convidado, registre também o tempo de parede do programa apenas como dado complementar. O tempo simulado e os contadores do gem5 são a base da comparação arquitetural.

## Tabela de resultados

| Política | CPUs | Memória | Hipótese |
|---|---:|---:|---|
| Local | nó 0 | nó 0 | menor latência |
| Remota | nó 0 | nó 1 | maior tráfego e latência |
| Intercalada | nó 0 | todos | maior banda agregada, custo misto |

## Interpretação

Acesso remoto deve aumentar a latência média e pode elevar a ocupação da rede. Entretanto, o efeito depende do padrão de acesso, da capacidade de cache e da saturação dos controladores. Interleaving pode vencer a alocação local em workloads limitados por largura de banda, mesmo que alguns acessos sejam mais longos.

## Exercícios

1. Inicialize cada faixa do vetor pela própria thread que a consumirá e avalie o efeito de *first touch*.
2. Compare acesso sequencial (`i += 1`) e estridado (`i += 8`).
3. Crie um workload em que todas as threads leem a mesma faixa remota.
4. Varie a latência do link entre nós e construa um gráfico de sensibilidade.

## Conclusão

NUMA transforma localidade em uma propriedade do mapeamento entre threads, páginas e controladores. Uma avaliação confiável deve declarar a topologia, a política de páginas, a afinidade de CPUs e a distribuição física dos dados.
