# Tutorial GEM5 — Segurança de Arquitetura

## Introdução
Este tutorial usa um experimento controlado de observação de latência de cache para explicar isolamento de memória, canais laterais temporais e contramedidas arquiteturais. O objetivo é medir efeitos, não produzir exploração contra sistemas reais.

## Objetivo
Construir uma microcarga segura em SE, medir diferenças entre acessos quentes e frios de cache e comparar configurações que reduzem o compartilhamento de recursos.

## Pré-requisitos
- gem5 compilado para X86;
- conhecimento de caches e `stats.txt`;
- ambiente isolado para a simulação.

## Conceitos
Um canal lateral de cache ocorre quando o tempo de um acesso revela indiretamente se um dado estava em cache. Em simulação, a latência pode ser obtida por métricas agregadas ou instrumentação controlada. Resultados de um microbenchmark não demonstram vulnerabilidade de um processador real: o modelo, o SO, o compilador e o ambiente têm impacto.

## Prática

### Etapa 1 — Criar a microcarga
Crie `cache_latency.c`:

```c
#include <stdint.h>
#include <stdio.h>
#define N (1<<20)
static volatile unsigned char data[N];
static uint64_t sum;
static void touch(int stride) {
  for (int i=0;i<N;i+=stride) sum += data[i];
}
int main(void) {
  for (int i=0;i<N;i++) data[i]=(unsigned char)i;
  touch(64);                 // aquece linhas selecionadas
  for (int r=0;r<100;r++) touch(64);
  printf("%llu\n", (unsigned long long)sum);
  return 0;
}
```

Compile sem remover os acessos:

```bash
gcc -O2 -fno-tree-vectorize cache_latency.c -o cache_latency
```

### Etapa 2 — Criar uma configuração SE com cache privada
Em uma configuração Python, use uma hierarquia com L1 privada por núcleo e execute um único processo. Essa é a linha de base para o comportamento da carga.

```python
cache = PrivateL1PrivateL2CacheHierarchy(l1i_size="32KiB", l1d_size="32KiB", l2_size="512KiB")
```

### Etapa 3 — Executar e registrar as métricas

```bash
build/X86/gem5.opt --outdir=out/baseline configs/tutorial/cache_security.py
grep -E 'numCycles|overallMissRate|overallAvgMissLatency' out/baseline/stats.txt
```

### Etapa 4 — Avaliar isolamento por configuração
Execute três cenários:

| Cenário | Organização | Pergunta |
|---|---|---|
| A | uma carga, L1 privada | referência |
| B | duas cargas, L2 compartilhada | há pressão adicional na L2? |
| C | duas cargas, L2 privada ou particionada | o efeito agregado diminui? |

A implementação de particionamento depende da versão e do modelo de cache. Quando não houver suporte nativo, compare hierarquias privadas e compartilhadas, deixando explícita essa limitação.

### Etapa 5 — Coletar resultados por região
Use marcadores `m5 resetstats` e `m5 dumpstats` em uma imagem FS caso necessite separar fases. Em SE, mantenha a inicialização curta ou use as estatísticas de fase disponíveis na configuração.

## Análise
Compare faltas, latência média de faltas, acessos a L2 e ciclos. Um aumento de latência ou faltas no cenário compartilhado indica interferência de recursos, mas não quantifica por si só capacidade de exfiltração. Para conclusões de segurança, seriam necessários modelo de ameaça, repetição estatística, ruído e validação independente.

## Ética e limites
Use esta atividade apenas para aprendizado e avaliação defensiva em ambiente autorizado. Não trate resultados simulados como evidência direta sobre um hardware comercial sem validação experimental.

## Exercícios
1. Varie a associatividade de L2.
2. Compare padrões sequenciais e aleatórios de acesso.
3. Avalie o efeito de aumentar o tamanho do conjunto de dados além de L2.
