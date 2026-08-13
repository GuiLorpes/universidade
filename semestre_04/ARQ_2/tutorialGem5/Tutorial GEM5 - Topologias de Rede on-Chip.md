# Tutorial GEM5 — Topologias de Rede on-Chip: Mesh, Torus, Ring e Crossbar

## Introdução
Em sistemas com muitos núcleos, a interconexão determina como pedidos de cache e memória atravessam o chip. Este tutorial compara **Mesh**, **Torus**, **Ring** e **Crossbar** com o subsistema Ruby/Garnet do gem5.

## Objetivo
Medir como topologia, número de saltos e contenção afetam latência e desempenho de um programa paralelo.

## Pré-requisitos
- gem5 compilado com `build/X86/gem5.opt`;
- Python 3, compilador GCC e OpenMP;
- um checkout recente do gem5 com Ruby e Garnet.

> Os nomes exatos dos protocolos e opções podem variar entre versões. Consulte `--help` do script de configuração da sua árvore.

## Conceitos essenciais
- **Router** encaminha pacotes entre enlaces.
- **Link** é o canal entre dois roteadores/controladores.
- **Hop** é uma travessia de roteador; mais hops normalmente elevam a latência.
- **Mesh** escala bem em área; **Torus** adiciona enlaces de contorno; **Ring** é simples, mas pode concentrar tráfego; **Crossbar** tem baixa distância, porém custo quadrático.

## Etapa 1 — Criar um benchmark paralelo
Use redução de histogramas, que cria acessos concorrentes à memória sem reutilizar os exemplos anteriores.

```c
// histograma.c
#include <omp.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N (1<<22)
#define BINS 256
int main(void) {
  unsigned char *v = malloc(N);
  unsigned long hist[BINS] = {0};
  for (size_t i=0; i<N; i++) v[i] = (i * 17u + 13u) & 255;
  #pragma omp parallel
  {
    unsigned long local[BINS] = {0};
    #pragma omp for
    for (size_t i=0; i<N; i++) local[v[i]]++;
    #pragma omp critical
    for (int b=0; b<BINS; b++) hist[b] += local[b];
  }
  printf("total=%lu\n", hist[0] + hist[1]);
  free(v);
}
```

Compile para x86:

```bash
gcc -O3 -fopenmp histograma.c -o histograma
```

## Etapa 2 — Preparar a configuração Ruby
Parta do script de exemplo da sua versão, normalmente em `configs/example/garnet_synth_traffic.py` para microbenchmarks de rede ou em um script Ruby para executar aplicações. Para observar o sistema completo, adapte um script SE que aceite `--ruby`.

Exemplo de comando-base com 16 núcleos e topologia Mesh:

```bash
build/X86/gem5.opt -d out/mesh \
  configs/example/se.py --cmd=./histograma --cpu-type=TimingSimpleCPU \
  --num-cpus=16 --ruby --network=garnet --topology=Mesh_XY
```

Para tráfego sintético, que isola a rede da CPU:

```bash
build/X86/gem5.opt -d out/mesh-sintetico \
  configs/example/garnet_synth_traffic.py \
  --num-cpus=16 --num-dirs=4 --topology=Mesh_XY \
  --synthetic=uniform_random --sim-cycles=100000
```

## Etapa 3 — Executar as topologias
Execute a mesma carga e mantenha constantes frequência, número de nós, caches, protocolo e ciclos simulados.

```bash
# Substitua pelos identificadores disponíveis em sua versão.
for topo in Mesh_XY Torus Ring Crossbar; do
  build/X86/gem5.opt -d out/$topo \
    configs/example/garnet_synth_traffic.py \
    --num-cpus=16 --num-dirs=4 --topology=$topo \
    --synthetic=uniform_random --sim-cycles=100000
done
```

Se `Torus`, `Ring` ou `Crossbar` não estiverem disponíveis, implemente/adicione a topologia em `configs/topologies/` ou compare apenas as topologias expostas pelo checkout. Não altere o protocolo durante a comparação.

## Etapa 4 — Extrair métricas
Em cada `stats.txt`, procure estatísticas de rede e de execução:

```bash
grep -E "simSeconds|simTicks|average_hops|average_packet|packets_received|flits" out/Mesh_XY/stats.txt
```

Métricas úteis:

| Métrica | Interpretação |
|---|---|
| `simSeconds` | Tempo simulado da carga |
| `average_hops` | Distância média percorrida pelos pacotes |
| latência média de rede | Espera mais travessia na rede |
| pacotes/flits recebidos | Volume de tráfego transportado |
| utilização de link | Indício de gargalo e contenção |

Os nomes podem ter prefixos como `system.ruby.network`.

## Etapa 5 — Analisar
Organize os resultados em uma tabela:

| Topologia | Tempo (s) | Hops médios | Latência média | Flits recebidos |
|---|---:|---:|---:|---:|
| Mesh | | | | |
| Torus | | | | |
| Ring | | | | |
| Crossbar | | | | |

Calcule o *speedup* relativo à mesh:

\[
S_T = \frac{T_{mesh}}{T_T}
\]

Uma topologia com menos hops não é automaticamente melhor: enlaces extras, arbitragem, padrão de tráfego e carga oferecida também importam.

## Validação e cuidados
- Use sementes e duração idênticas para tráfego sintético.
- Confirme que a quantidade de nós é compatível com a topologia, por exemplo, 16 para uma mesh 4×4.
- Descarte execuções abortadas e registre a versão do gem5.
- Para aplicações reais, diferencie tempo de simulação de tempo de parede do host.

## Exercícios
1. Repita com tráfego `transpose` ou `bit_complement`.
2. Compare 4, 16 e 64 nós, quando o custo de simulação permitir.
3. Aumente a taxa de injeção até localizar o ponto de saturação de cada topologia.
4. Explique um caso em que Ring supera Mesh para uma carga pouco comunicativa.

## Conclusão
A topologia é uma decisão arquitetural: ela define caminhos, capacidade bissecional e custo de implementação. Garnet permite separar o efeito da rede com tráfego sintético e depois validá-lo com aplicações paralelas reais.