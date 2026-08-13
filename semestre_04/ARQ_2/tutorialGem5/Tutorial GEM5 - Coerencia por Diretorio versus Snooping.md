# Tutorial GEM5 — Coerência por Diretório versus Snooping

## Introdução
Sistemas coerentes precisam descobrir quais caches possuem uma linha. Em **snooping**, pedidos são observados por todos em um meio compartilhado; em **diretório**, metadados localizam ou representam os compartilhadores e mensagens são direcionadas.

## Objetivo
Projetar uma comparação justa entre uma configuração baseada em difusão e uma baseada em diretório, identificando custo de tráfego, metadados e escalabilidade.

## Pré-requisitos
- gem5 e Ruby/Garnet compilados;
- conhecimento de topologias;
- compilador C com OpenMP.

## Limite importante
O gem5 não fornece necessariamente um par “snooping vs diretório” idêntico e pronto em todos os checkouts. Um barramento clássico coerente pode usar mecanismos distintos do Ruby. Portanto, trate este tutorial como um método de comparação: documente exatamente os modelos, caches e protocolos escolhidos.

## Conceitos
| Abordagem | Vantagem | Limitação |
|---|---|---|
| Snooping | implementação conceitualmente simples em barramento | broadcasts escalam mal |
| Diretório | mensagens seletivas e melhor adequação a NoC | metadados e latência de consulta |

Um diretório pode ser centralizado, distribuído ou limitado em número de ponteiros. O custo depende também do padrão de compartilhamento.

## Etapa 1 — Benchmark de leitura e escrita compartilhada

```c
// pingpong.c
#include <omp.h>
#include <stdio.h>
#include <stdint.h>
volatile int token = 0;
int main(void) {
  const int n = 200000;
  #pragma omp parallel num_threads(2)
  {
    int id = omp_get_thread_num();
    for (int i=0; i<n; i++) {
      while (token != id) { }
      token = 1 - id;
    }
  }
  printf("token=%d\n", token);
}
```

```bash
gcc -O2 -fopenmp pingpong.c -o pingpong
```

O padrão é intencionalmente adverso: duas CPUs alternam escrita na mesma linha.

## Etapa 2 — Configuração baseada em snooping
Use um sistema clássico com interconexão compartilhada e caches coerentes disponíveis na versão instalada. Um ponto de partida é um script SE clássico com `SystemXBar` e caches privados, mas confirme que a coerência está efetivamente habilitada para sua combinação de CPU/cache.

```bash
build/X86/gem5.opt -d out/snoop \
  configs/example/se.py --cmd=./pingpong --num-cpus=2 \
  --cpu-type=TimingSimpleCPU --caches --l2cache
```

Registre: tipo de barramento, tamanho/associatividade de cache, modelo de memória e política de coerência.

## Etapa 3 — Configuração baseada em diretório
Use Ruby com um protocolo baseado em diretório, como uma configuração MESI de dois níveis que exista no checkout.

```bash
build/X86/gem5.opt -d out/diretorio \
  configs/example/se.py --cmd=./pingpong --num-cpus=2 \
  --cpu-type=TimingSimpleCPU --ruby --num-dirs=1 \
  --network=garnet --topology=Mesh_XY
```

Se a mesh exigir número quadrado de nós, escolha uma topologia válida para dois núcleos ou execute com quatro núcleos, mantendo duas threads ativas.

## Etapa 4 — Escalar a experiência
Execute 2, 4, 8 e 16 CPUs. Para ampliar o compartilhamento, substitua o par de threads por um conjunto de threads que lê e escreve uma estrutura compartilhada protegida por barreiras.

## Etapa 5 — Coletar e normalizar dados

```bash
grep -Ei "simSeconds|miss|snoop|broadcast|inval|request|response|packets|flits" out/diretorio/stats.txt
```

| Núcleos | Modelo | Tempo | Tráfego/interconexão | Invalidações | Metadados do diretório |
|---:|---|---:|---:|---:|---:|
| 2 | Snooping | | | | N/A |
| 2 | Diretório | | | | |

Não use “número de mensagens” como comparação direta se os subsistemas contabilizam mensagens em granularidades diferentes. Prefira tendências por modelo e explique a limitação.

## Interpretação
Em baixa contagem de núcleos, um barramento pode ter latência competitiva. À medida que a demanda cresce, broadcasts e arbitragem tornam-se gargalos. Diretórios eliminam difusão desnecessária quando há poucos compartilhadores, mas introduzem consulta e armazenamento de estado.

## Exercícios
1. Compare a carga ping-pong com uma carga somente de leitura compartilhada.
2. Calcule o armazenamento de um diretório com vetor de bits para 16, 64 e 256 núcleos.
3. Varie o número de diretórios e sua posição na NoC.
4. Investigue se o programa sofre de falsa compartilhação.

## Conclusão
Snooping e diretório representam compromissos diferentes. Uma boa avaliação separa efeitos de protocolo, topologia, hierarquia de cache e padrão de compartilhamento.