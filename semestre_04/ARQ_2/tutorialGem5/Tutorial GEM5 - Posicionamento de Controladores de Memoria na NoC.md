# Tutorial GEM5 — Impacto do Posicionamento de Controladores de Memória na NoC

## Introdução
Em uma NoC, controladores de memória são destinos de pedidos de *cache miss*. Sua posição altera o número de hops, a pressão nos enlaces e a desigualdade de latência entre núcleos.

## Objetivo
Comparar mapeamentos de controladores de memória em uma mesh 2D Ruby/Garnet e relacionar posição, distância e desempenho.

## Pré-requisitos
- gem5 com Ruby e Garnet;
- build X86 funcional;
- GCC/OpenMP;
- familiaridade básica com `configs/topologies/`.

## Conceitos
Uma mesh 4×4 tem coordenadas `(x,y)`. Um controlador pode ficar nos cantos, nas bordas ou distribuído. Com roteamento XY, uma aproximação de distância é:

\[
d((x_1,y_1),(x_2,y_2))=|x_1-x_2|+|y_1-y_2|
\]

A distância média não captura toda a realidade: congestionamento e tráfego de coerência também influenciam.

## Etapa 1 — Criar a carga
O programa percorre um grande vetor em blocos paralelos, gerando pressão de memória.

```c
// stream_triad.c
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#define N (1<<24)
int main(void) {
  double *a=aligned_alloc(64,N*sizeof(double));
  double *b=aligned_alloc(64,N*sizeof(double));
  double *c=aligned_alloc(64,N*sizeof(double));
  for (long i=0;i<N;i++) { b[i]=i*0.5; c[i]=1.0; }
  #pragma omp parallel for schedule(static)
  for (long i=0;i<N;i++) a[i]=b[i]+3.0*c[i];
  printf("%f\n", a[N-1]);
  free(a); free(b); free(c);
}
```

```bash
gcc -O3 -fopenmp stream_triad.c -o stream_triad
```

## Etapa 2 — Identificar a topologia
Localize a classe usada, por exemplo `configs/topologies/Mesh_XY.py`. Ela cria roteadores, enlaces internos e enlaces externos que conectam controladores Ruby à rede. Copie-a para preservar o original:

```bash
cp configs/topologies/Mesh_XY.py configs/topologies/MeshMemMap.py
```

## Etapa 3 — Criar três políticas de posicionamento
No arquivo copiado, identifique a lista de controladores de diretório/memória. A API concreta varia, mas a ideia é atribuir cada controlador a um roteador específico.

- **Cantos:** controladores nos roteadores 0, 3, 12 e 15;
- **Bordas:** roteadores 1, 7, 8 e 14;
- **Distribuído:** roteadores 0, 5, 10 e 15.

Exemplo conceitual de seleção:

```python
# Dentro da construção de links externos; adapte atributos à sua versão.
mem_router_ids = [0, 3, 12, 15]  # política: cantos
for i, ctrl in enumerate(dir_controllers):
    router_id = mem_router_ids[i % len(mem_router_ids)]
    # crie ExternalLink entre ctrl e routers[router_id]
```

Crie uma cópia por política ou exponha uma opção `--mem-map` ao script. Verifique o grafo gerado: cada controlador deve ter exatamente um enlace externo.

## Etapa 4 — Executar configurações equivalentes
Use 16 CPUs, quatro diretórios/controladores e a mesma mesh 4×4.

```bash
for mapa in cantos bordas distribuido; do
  build/X86/gem5.opt -d out/mem-$mapa \
    configs/example/se.py --cmd=./stream_triad --num-cpus=16 \
    --cpu-type=TimingSimpleCPU --ruby --network=garnet \
    --topology=MeshMemMap --num-dirs=4 --mem-map=$mapa
done
```

Caso seu script não aceite `--mem-map`, selecione a política diretamente na cópia de topologia e registre o arquivo usado em cada execução.

## Etapa 5 — Coletar resultados

```bash
grep -E "simSeconds|average_hops|average_packet|overall_misses|mem_ctrl" out/mem-cantos/stats.txt
```

Registre tempo, hops, latência de rede, misses e métricas dos controladores. Mantenha iguais capacidade e latência dos controladores; só a posição deve mudar.

## Interpretação
| Política | Hipótese |
|---|---|
| Cantos | pode penalizar núcleos centrais, mas dispersa destinos |
| Bordas | pode equilibrar distâncias para certos quadrantes |
| Distribuído | tende a reduzir a maior distância, dependendo do tráfego |

Não conclua apenas a partir de hops: se uma política concentra fluxos em poucos enlaces, a fila pode superar o ganho de caminho.

## Exercícios
1. Use apenas um controlador e compare-o no centro e em um canto.
2. Mude a afinidade das threads com `OMP_PROC_BIND` quando suportado.
3. Compare tráfego uniforme e tráfego concentrado em uma região.
4. Calcule a distância média teórica e compare-a à estatística observada.

## Conclusão
O posicionamento é uma forma de projeto de NoC. Ao manter o restante do sistema constante, o experimento identifica efeitos de localidade e congestionamento que não aparecem em uma visão apenas funcional.