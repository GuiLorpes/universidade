# Tutorial GEM5 — Falsa Compartilhação em Programas Paralelos

## Introdução
**Falsa compartilhação** ocorre quando threads atualizam variáveis logicamente independentes que residem na mesma linha de cache. Embora não compartilhem o mesmo dado, as escritas causam invalidações e transferências de propriedade.

## Objetivo
Reproduzir falsa compartilhação no gem5, medir seu impacto com Ruby e corrigir o programa usando *padding* e alinhamento.

## Pré-requisitos
- gem5 com Ruby;
- GCC e OpenMP;
- build para X86.

## Conceitos
Coerência opera na granularidade da **linha de cache**, frequentemente 64 B. Se cada contador ocupa 8 B, até oito contadores podem cair na mesma linha. Ao alinhar cada contador em 64 B, cada thread atualiza uma linha diferente.

## Etapa 1 — Versão com falsa compartilhação

```c
// false_sharing.c
#include <omp.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#define THREADS 4
#define ITER 5000000L
int main(void) {
  long *cont = calloc(THREADS, sizeof(long));
  #pragma omp parallel num_threads(THREADS)
  {
    int id = omp_get_thread_num();
    for (long i=0; i<ITER; i++) cont[id]++;
  }
  long total=0;
  for (int i=0;i<THREADS;i++) total += cont[i];
  printf("total=%ld\n", total);
  free(cont);
}
```

## Etapa 2 — Versão corrigida

```c
// padded.c
#include <omp.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#define THREADS 4
#define ITER 5000000L
struct slot { long value; char pad[56]; } __attribute__((aligned(64)));
int main(void) {
  struct slot *cont = aligned_alloc(64, THREADS*sizeof(*cont));
  for (int i=0;i<THREADS;i++) cont[i].value=0;
  #pragma omp parallel num_threads(THREADS)
  {
    int id=omp_get_thread_num();
    for (long i=0;i<ITER;i++) cont[id].value++;
  }
  long total=0;
  for (int i=0;i<THREADS;i++) total+=cont[i].value;
  printf("total=%ld\n", total);
  free(cont);
}
```

O `pad[56]` pressupõe `long` de 8 B e linha de 64 B. Ajuste o valor se o tamanho de linha configurado for diferente.

```bash
gcc -O2 -fopenmp false_sharing.c -o false_sharing
gcc -O2 -fopenmp padded.c -o padded
```

## Etapa 3 — Simular com Ruby

```bash
for app in false_sharing padded; do
  build/X86/gem5.opt -d out/$app \
    configs/example/se.py --cmd=./$app --num-cpus=4 \
    --cpu-type=TimingSimpleCPU --ruby --num-dirs=1
done
```

Para uma análise mais fiel de desempenho, repita com `O3CPU`, ciente de que a simulação ficará mais lenta. Mantenha a configuração idêntica entre as versões.

## Etapa 4 — Confirmar o experimento
O resultado deve ser `total=20000000`. Confirme também que existem quatro CPUs/threads ativas e que o compilador não removeu o laço. Se necessário, examine o código gerado ou use uma dependência observável.

## Etapa 5 — Coletar métricas

```bash
grep -Ei "simSeconds|inval|upgrade|writeback|request|response|miss" out/false_sharing/stats.txt
```

| Versão | Tempo | Invalidações/Upgrades | Misses | Mensagens Ruby |
|---|---:|---:|---:|---:|
| Contadores adjacentes | | | | |
| Contadores alinhados | | | | |

Os nomes dos contadores variam por protocolo. Compare campos com a mesma semântica na mesma configuração Ruby.

## Interpretação
A versão corrigida deve reduzir tráfego de escrita compartilhada. Ela pode ainda ter misses compulsórios e tráfego de inicialização; o objetivo não é eliminá-los, mas remover a disputa artificial pela mesma linha.

## Variações
- Use 2, 4 e 8 threads.
- Altere `pad` para 0, 8, 32 e 56 bytes.
- Faça cada thread atualizar dois contadores; avalie layout *array of structs* versus *struct of arrays*.
- Troque incremento local por `#pragma omp atomic` para observar contenção verdadeira, distinta de falsa compartilhação.

## Conclusão
A proximidade no arranjo de dados pode ser invisível funcionalmente e cara arquiteturalmente. O gem5 permite ligar essa decisão de layout a eventos de coerência e desempenho.