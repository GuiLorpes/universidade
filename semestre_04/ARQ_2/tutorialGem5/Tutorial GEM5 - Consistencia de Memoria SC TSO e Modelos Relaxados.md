# Tutorial GEM5 — Consistência de Memória: SC, TSO e Modelos Relaxados

## Introdução

Em sistemas paralelos, **coerência de cache** e **consistência de memória** são conceitos distintos. A coerência define regras para uma mesma linha de cache; a consistência define quais ordens de observação entre leituras e escritas são permitidas para o programa inteiro. Este tutorial usa um teste *store buffering* para estudar o assunto e mostra os limites de uma avaliação em gem5.

## Objetivo

Compreender SC, TSO e modelos relaxados, executar um litmus test em modo SE e identificar quando a arquitetura simulada, o compilador e as primitivas de sincronização alteram resultados observáveis.

## Pré-requisitos

- gem5 para X86 ou ARM;
- compilador GCC;
- sistema SE multicore, idealmente com `TimingSimpleCPU` ou `O3CPU`;
- conhecimento básico de threads e variáveis atômicas C11.

## Conceitos fundamentais

### Coerência

Para uma localização `x`, todos devem concordar com uma ordem de escritas em `x`. Isso não exige uma ordem única entre escritas em `x` e em outra localização `y`.

### Consistência sequencial (SC)

SC exige uma única ordem global de operações de memória compatível com a ordem de programa de cada thread. É simples para raciocinar, mas pode restringir otimizações.

### Total Store Order (TSO)

TSO, associado ao x86, permite que uma escrita permaneça temporariamente em um *store buffer*. Assim, uma leitura posterior de outra localização pode ocorrer antes de a escrita anterior se tornar visível aos demais núcleos.

### Modelos relaxados

Arquiteturas como ARM e RISC-V permitem mais reordenações. Programas corretos devem expressar sincronização com operações atômicas, *acquire/release* ou barreiras.

## Etapa 1 — O teste Store Buffering

Crie `store_buffering.c`:

```c
#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>

#define ROUNDS 100000
atomic_int x, y, start_flag;
int r0, r1;

void *thread0(void *arg) {
    for (int i = 0; i < ROUNDS; i++) {
        while (atomic_load_explicit(&start_flag, memory_order_relaxed) != 1) {}
        atomic_store_explicit(&x, 1, memory_order_relaxed);
        r0 = atomic_load_explicit(&y, memory_order_relaxed);
        atomic_store_explicit(&start_flag, 2, memory_order_relaxed);
        while (atomic_load_explicit(&start_flag, memory_order_relaxed) != 0) {}
    }
    return NULL;
}

void *thread1(void *arg) {
    for (int i = 0; i < ROUNDS; i++) {
        while (atomic_load_explicit(&start_flag, memory_order_relaxed) != 1) {}
        atomic_store_explicit(&y, 1, memory_order_relaxed);
        r1 = atomic_load_explicit(&x, memory_order_relaxed);
        while (atomic_load_explicit(&start_flag, memory_order_relaxed) != 2) {}
        atomic_store_explicit(&start_flag, 0, memory_order_relaxed);
    }
    return NULL;
}

int main(void) {
    pthread_t a, b;
    int both_zero = 0;
    atomic_init(&x, 0); atomic_init(&y, 0); atomic_init(&start_flag, 0);
    pthread_create(&a, NULL, thread0, NULL);
    pthread_create(&b, NULL, thread1, NULL);
    for (int i = 0; i < ROUNDS; i++) {
        atomic_store(&x, 0); atomic_store(&y, 0);
        atomic_store(&start_flag, 1);
        while (atomic_load(&start_flag) != 0) {}
        if (r0 == 0 && r1 == 0) both_zero++;
    }
    pthread_join(a, NULL); pthread_join(b, NULL);
    printf("rounds=%d r0=r1=0: %d\n", ROUNDS, both_zero);
    return 0;
}
```

Compile:

```bash
gcc -O2 -static -pthread store_buffering.c -o store_buffering
```

> Este programa é didático, mas a coordenação também faz parte do comportamento observado. Litmus tests rigorosos normalmente usam *harnesses* especializados. Não use este exemplo como prova formal de um modelo de memória.

## Etapa 2 — Executar em X86 no modo SE

```bash
build/X86/gem5.opt --outdir=out/x86-sb \
  configs/example/se.py --cmd=./store_buffering \
  --cpu-type=O3CPU --num-cpus=2 --caches --l2cache
```

Para uma experiência multicore mais detalhada, utilize uma configuração Ruby com duas CPUs e execute o mesmo binário. Garanta que cada thread possa ser escalonada em um contexto de hardware distinto.

## Etapa 3 — Testar uma versão com ordenação forte

Troque as operações sobre `x` e `y` de `memory_order_relaxed` para `memory_order_seq_cst`. Recompile como `store_buffering_sc` e execute com a mesma configuração.

```bash
sed 's/memory_order_relaxed/memory_order_seq_cst/g' store_buffering.c > store_buffering_sc.c
gcc -O2 -static -pthread store_buffering_sc.c -o store_buffering_sc
```

Compare o resultado funcional, `simTicks` e a quantidade de instruções. Ordenação mais forte pode inserir instruções adicionais ou restringir reordenações.

## Etapa 4 — Comparar ISAs com cuidado

Se você tiver builds e binários equivalentes para ARM ou RISC-V, repita o experimento. Não compare somente contagens de `r0=r1=0`: compare também a semântica da ISA, as opções do compilador, a versão do gem5 e o modelo de CPU utilizado.

## Etapa 5 — Analisar estatísticas

```bash
grep -E "simTicks|simInsts|numCycles|committedInsts|overall_misses" out/x86-sb/stats.txt
```

As estatísticas de cache explicam custo de comunicação, mas não definem sozinhas a consistência. A evidência principal é o resultado permitido pelo programa sob a ISA e a ordenação C11 escolhida.

## Interpretação

- Usar `memory_order_relaxed` é adequado apenas quando não há dependência de ordenação entre threads.
- `memory_order_seq_cst` simplifica o raciocínio, mas pode custar desempenho.
- Barreiras e operações acquire/release devem ser selecionadas pela relação de sincronização necessária, não apenas para “fazer o teste passar”.

## Limitações e validação

O comportamento depende de detalhes como modelo de CPU, ISA, implementação de atômicos, compilador e versão do simulador. Consulte a documentação da ISA e valide resultados relevantes com ferramentas próprias de litmus testing ou em hardware real. Evite generalizar um único experimento para toda uma arquitetura.

## Exercícios

1. Implemente o teste *message passing*: uma thread publica dados e depois uma flag; a outra espera a flag antes de ler os dados.
2. Use `memory_order_release` na publicação e `memory_order_acquire` no consumo.
3. Compare `AtomicSimpleCPU`, `TimingSimpleCPU` e `O3CPU`; explique quais diferenças são funcionais e quais são de temporização.
4. Relacione barreiras de memória com mensagens de coerência observadas em uma configuração Ruby.

## Conclusão

Coerência não substitui sincronização correta. Ao simular programas paralelos, trate o modelo de memória como parte da especificação do experimento: ISA, compilador, ordenação atômica e modelo de CPU devem ser documentados junto com as métricas de desempenho.
