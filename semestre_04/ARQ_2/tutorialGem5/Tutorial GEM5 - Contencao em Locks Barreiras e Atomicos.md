# Tutorial GEM5 — Contenção em Locks, Barreiras e Variáveis Atômicas

## Introdução

Programas paralelos precisam coordenar threads. Essa coordenação pode se tornar o gargalo dominante: vários núcleos disputam uma mesma linha de cache, que migra entre caches privadas e gera tráfego de coerência. Neste tutorial, será comparado o custo de um `pthread_mutex`, de uma operação atômica e de uma redução com contadores locais.

## Objetivo

Medir, em modo **SE** com **Ruby**, como a escolha da sincronização afeta tempo simulado, invalidações, misses e tráfego da interconexão.

## Pré-requisitos

- gem5 compilado para X86: `build/X86/gem5.opt`;
- compilador GCC com pthreads;
- uma configuração Ruby válida, como `configs/example/garnet_synth_traffic.py` para microtestes de rede ou um script SE próprio baseado em `configs/example/gem5_library`.

Os nomes de estatísticas e opções podem variar entre versões do gem5. Confirme sempre em `stats.txt` e com `--help`.

## Conceitos essenciais

- **Lock**: exclusão mútua; cada aquisição contenciosa pode invalidar a cópia do lock em outros núcleos.
- **Barreira**: todos aguardam a chegada dos demais; amplifica o efeito do thread mais lento.
- **Atômico**: uma atualização indivisível, normalmente implementada por read-modify-write.
- **Redução local**: cada thread atualiza dados privados e uma única agregação é feita ao final; reduz compartilhamento.

> Coerência garante que todos observem uma linha de cache de forma compatível. Ela não torna o algoritmo escalável quando todos escrevem a mesma linha.

## Etapa 1 — Criar o benchmark

Crie `sync_contention.c`:

```c
#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MAX_THREADS 16
#define ITERS 200000

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
atomic_long atomic_counter = 0;
long local_counter[MAX_THREADS];
int mode, nthreads;

void *worker(void *arg) {
    long id = (long)arg;
    for (int i = 0; i < ITERS; i++) {
        if (mode == 0) {
            pthread_mutex_lock(&lock);
            atomic_counter++;
            pthread_mutex_unlock(&lock);
        } else if (mode == 1) {
            atomic_fetch_add_explicit(&atomic_counter, 1, memory_order_relaxed);
        } else {
            local_counter[id]++;
        }
    }
    return NULL;
}

int main(int argc, char **argv) {
    if (argc != 3) return 1;
    mode = atoi(argv[1]); nthreads = atoi(argv[2]);
    if (nthreads < 1 || nthreads > MAX_THREADS) return 2;
    pthread_t t[MAX_THREADS];
    for (long i = 0; i < nthreads; i++) pthread_create(&t[i], NULL, worker, (void *)i);
    for (int i = 0; i < nthreads; i++) pthread_join(t[i], NULL);
    long total = atomic_counter;
    for (int i = 0; i < nthreads; i++) total += local_counter[i];
    printf("modo=%d threads=%d total=%ld esperado=%ld\n", mode, nthreads, total,
           (long)nthreads * ITERS);
    return total != (long)nthreads * ITERS;
}
```

Compile estaticamente para facilitar SE:

```bash
gcc -O2 -static -pthread sync_contention.c -o sync_contention
```

Os modos são: `0` mutex, `1` atômico compartilhado e `2` contador local.

## Etapa 2 — Configurar sistema SE multicore com Ruby

Parta de um script SE com Ruby de sua instalação e estabeleça:

- número de CPUs igual ao número de threads;
- uma cache privada L1 por CPU;
- uma rede Garnet;
- um protocolo Ruby disponível no seu build, por exemplo MESI Two Level.

Um comando típico para configurações legadas é:

```bash
build/X86/gem5.opt --outdir=out/mutex-4 \
  configs/example/se.py --cmd=./sync_contention --options="0 4" \
  --cpu-type=TimingSimpleCPU --num-cpus=4 --ruby --network=garnet
```

Em versões recentes, prefira um script baseado na API Python e na configuração Ruby fornecida pela própria árvore de fontes. Mantenha **a mesma topologia, protocolo, caches e CPU** em todas as execuções.

## Etapa 3 — Executar a campanha

Execute 1, 2, 4 e 8 threads para os três modos:

```bash
for mode in 0 1 2; do
  for n in 1 2 4 8; do
    build/X86/gem5.opt --outdir=out/m${mode}-n${n} \
      configs/example/se.py --cmd=./sync_contention --options="$mode $n" \
      --cpu-type=TimingSimpleCPU --num-cpus=$n --ruby --network=garnet
  done
done
```

Ajuste o script de configuração ao layout da sua versão, mas preserve o diretório de saída por experimento.

## Etapa 4 — Extrair métricas

```bash
for f in out/*/stats.txt; do
  echo "--- $f"
  grep -E "simTicks|simSeconds|system.*numCycles|overall_misses|inv|network" "$f" | head -30
done
```

Registre, no mínimo:

| Métrica | Interpretação |
|---|---|
| `simTicks` ou ciclos | tempo total simulado |
| misses L1/L2 | pressão na hierarquia de cache |
| mensagens/injeções Ruby | atividade de coerência |
| latência de rede | custo de transportar requisições |

Os contadores específicos de invalidação dependem do protocolo. Se não houver uma estatística explícita, use mensagens Ruby e misses como evidência indireta.

## Interpretação esperada

Com uma thread, os três modos podem ter custos próximos. À medida que o número de threads cresce, mutex e contador atômico concentram escritas numa mesma linha, causando transferência de propriedade e invalidações. A redução local tende a escalar melhor porque cada thread escreve predominantemente em uma linha privada.

Não conclua apenas pelo tempo: confirme que o total impresso é o esperado. Um resultado rápido e incorreto não é uma otimização válida.

## Exercícios

1. Alinhe cada contador local em 64 bytes e compare com o vetor original; investigue falsa compartilhação.
2. Acrescente uma barreira a cada 10 000 iterações e observe o desequilíbrio entre threads.
3. Compare `TimingSimpleCPU` e `O3CPU`, mantendo o restante da plataforma fixo.
4. Repita com 2, 4 e 8 controladores de memória e relacione a contenção à topologia.

## Conclusão

A sincronização é também um problema de comunicação entre caches. Projetos paralelos escaláveis minimizam escritas compartilhadas, mantêm dados locais e usam sincronização apenas onde ela é semanticamente necessária.
