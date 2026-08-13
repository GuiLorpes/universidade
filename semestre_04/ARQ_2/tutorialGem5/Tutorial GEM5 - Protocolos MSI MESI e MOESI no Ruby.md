# Tutorial GEM5 — Protocolos de Coerência MSI, MESI e MOESI no Ruby

## Introdução
Protocolos de coerência mantêm uma visão coerente de uma mesma linha de cache em vários núcleos. MSI, MESI e MOESI diferem principalmente nos estados permitidos e nas mensagens necessárias.

## Objetivo
Entender os estados dos protocolos e comparar seu tráfego e desempenho no gem5 Ruby, sem confundir **coerência** com **consistência de memória**.

## Pré-requisitos
- gem5 compilado para X86;
- Ruby habilitado;
- protocolos SLICC disponíveis no checkout;
- GCC e OpenMP.

> Nem todo checkout fornece implementações diretamente comparáveis de MSI, MESI e MOESI. Use somente protocolos efetivamente existentes na sua árvore e documente as diferenças estruturais, como tipo de diretório ou topologia.

## Estados fundamentais
| Protocolo | Estados típicos | Ideia central |
|---|---|---|
| MSI | Modified, Shared, Invalid | escrita exige exclusividade; não há estado exclusivo limpo |
| MESI | MSI + Exclusive | leitura sem compartilhadores pode ficar exclusiva e limpa |
| MOESI | MESI + Owned | uma cache suja pode fornecer dados a leitores compartilhados |

Os detalhes de transição dependem da implementação SLICC. Leia os arquivos `.sm` do protocolo selecionado antes de atribuir significado a cada contador.

## Etapa 1 — Localizar protocolos disponíveis

```bash
find src/mem/ruby/protocol -maxdepth 1 -type d | sort
find build/X86 -iname '*MESI*' -o -iname '*MOESI*' -o -iname '*MSI*'
```

Se for necessário recompilar com outro protocolo:

```bash
scons build/X86/gem5.opt PROTOCOL=MESI_Two_Level -j$(nproc)
```

O nome `MESI_Two_Level` é um exemplo comum; substitua pelo protocolo disponível. Cada protocolo pode exigir uma compilação própria.

## Etapa 2 — Criar benchmark de compartilhamento

```c
// compartilhamento.c
#include <omp.h>
#include <stdint.h>
#include <stdio.h>
volatile long contador = 0;
int main(void) {
  #pragma omp parallel num_threads(4)
  for (long i=0; i<200000; i++) {
    #pragma omp atomic
    contador++;
  }
  printf("contador=%ld\n", contador);
}
```

```bash
gcc -O2 -fopenmp compartilhamento.c -o compartilhamento
```

Este teste produz muita invalidação por escrita. Para medir leituras compartilhadas, faça a variável somente leitura após inicializá-la.

## Etapa 3 — Executar cada protocolo
Adapte o nome da configuração Ruby ao seu checkout.

```bash
build/X86/gem5.opt -d out/mesi \
  configs/example/se.py --cmd=./compartilhamento --num-cpus=4 \
  --cpu-type=TimingSimpleCPU --ruby --num-dirs=1
```

Repita após compilar/configurar cada protocolo, sempre com os mesmos caches, CPUs, memória, topologia e binário. Execute uma vez por diretório de saída distinto.

## Etapa 4 — Inspecionar estatísticas

```bash
grep -Ei "simSeconds|miss|inval|request|response|forward|writeback" out/mesi/stats.txt
```

Além de `simSeconds`, procure contadores de mensagens e transições nos controladores Ruby. Os nomes não são padronizados entre protocolos; liste os campos uma vez:

```bash
grep -i ruby out/mesi/stats.txt | head -80
```

## Etapa 5 — Montar a comparação

| Protocolo | Tempo | Misses L1 | Invalidações | Mensagens de dados | Writebacks |
|---|---:|---:|---:|---:|---:|
| MSI | | | | | |
| MESI | | | | | |
| MOESI | | | | | |

Interprete somente métricas semanticamente equivalentes. Um contador com o mesmo nome em dois protocolos não garante a mesma definição.

## Discussão esperada
- MESI pode evitar uma transação de atualização quando uma linha lida não tem outros compartilhadores.
- MOESI pode reduzir escrita de volta à memória ao permitir que um dono sujo responda a leitores.
- No benchmark atômico, a serialização e a contenção podem dominar; resultados não generalizam para todas as aplicações.

## Cuidados experimentais
- Garanta que o programa realmente usou o número de threads desejado.
- Não compare um protocolo de dois níveis com outro de três níveis como se a diferença fosse exclusivamente de estados.
- Valide o resultado do programa e procure mensagens de erro em `simout` e `simerr`.

## Exercícios
1. Substitua o contador por quatro contadores em linhas de cache separadas.
2. Compare uma fase de leitura compartilhada com uma fase de escrita privada.
3. Varie 2, 4 e 8 núcleos.
4. Desenhe as transições de uma leitura seguida de escrita para MSI e MESI.

## Conclusão
Protocolos são avaliados por custo de mensagens, latência e escalabilidade para padrões específicos de compartilhamento. Ruby permite observar esses efeitos em nível de controladores e rede.