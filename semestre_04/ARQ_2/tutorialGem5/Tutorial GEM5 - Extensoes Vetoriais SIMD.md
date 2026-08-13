# Tutorial GEM5 — Extensões Vetoriais SIMD

## Introdução
Este tutorial compara uma implementação escalar e uma implementação vetorizada de multiplicação elemento a elemento. O foco é observar como instruções SIMD alteram instruções, ciclos e comportamento de memória no gem5.

## Objetivo
Compilar código para uma ISA com suporte vetorial, executar em **SE** via API Python e avaliar se a vetorização produz ganho mensurável.

## Pré-requisitos
- gem5 construído para a ISA escolhida, por exemplo `build/ARM/gem5.opt`;
- compilador cruzado ARM com suporte a NEON, ou ambiente RISC-V com extensão vetorial compatível;
- conhecimento básico de SE e arquivos de configuração Python.

> A ISA, as opções de compilação e o modelo de CPU devem representar extensões realmente suportadas pela build e pela configuração do gem5.

## Prática

### Etapa 1 — Implementar as duas versões
Crie `simd_mul.c`:

```c
#include <stdio.h>
#include <stdlib.h>
#ifdef NEON
#include <arm_neon.h>
#endif
#define N (1<<20)
static float a[N], b[N], c[N];
int main(void) {
  for (int i=0;i<N;i++) { a[i]=i*0.001f; b[i]=1.0f+i*0.0001f; }
#ifdef NEON
  for (int i=0;i<N;i+=4) {
    float32x4_t x=vld1q_f32(&a[i]), y=vld1q_f32(&b[i]);
    vst1q_f32(&c[i], vmulq_f32(x,y));
  }
#else
  for (int i=0;i<N;i++) c[i]=a[i]*b[i];
#endif
  printf("resultado=%f\n", c[N-1]);
  return 0;
}
```

### Etapa 2 — Compilar
Exemplo ARM AArch64:

```bash
aarch64-linux-gnu-gcc -O3 simd_mul.c -o simd_scalar
aarch64-linux-gnu-gcc -O3 -DNEON -march=armv8-a+simd simd_mul.c -o simd_neon
```

Verifique que a segunda versão contém instruções vetoriais:

```bash
aarch64-linux-gnu-objdump -d simd_neon | grep -E 'ld1|fmul|st1'
```

### Etapa 3 — Criar configuração Python SE
Crie `configs/tutorial/simd_se.py`:

```python
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import PrivateL1PrivateL2CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator

cache = PrivateL1PrivateL2CacheHierarchy(l1d_size="32KiB", l1i_size="32KiB", l2_size="512KiB")
processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, isa=ISA.ARM, num_cores=1)
board = SimpleBoard(clk_freq="2GHz", processor=processor, memory=SingleChannelDDR3_1600(), cache_hierarchy=cache)
board.set_se_binary_workload(BinaryResource("/caminho/para/simd_neon"))
Simulator(board=board).run()
```

A API muda entre versões; adapte importações conforme a documentação da sua versão.

### Etapa 4 — Executar ambas as versões

```bash
build/ARM/gem5.opt --outdir=out/scalar configs/tutorial/simd_se.py
sed 's#simd_neon#simd_scalar#' configs/tutorial/simd_se.py > configs/tutorial/scalar_se.py
build/ARM/gem5.opt --outdir=out/neon configs/tutorial/scalar_se.py
```

### Etapa 5 — Coletar métricas

```bash
for d in out/scalar out/neon; do
  echo "$d"
  grep -E 'simTicks|numCycles|committedInsts|overallMissRate' "$d/stats.txt"
done
```

## Análise
Calcule IPC como instruções comprometidas divididas por ciclos. A versão SIMD pode reduzir o número de instruções, mas seu ganho depende de suporte funcional, largura do pipeline, latência de operações vetoriais e gargalos de memória. Valide sempre que os resultados numéricos impressos sejam equivalentes.

## Cuidados
- Não compare binários compilados para ISAs distintas.
- Não atribua ganho exclusivamente ao SIMD se `-O3` mudou outras otimizações.
- Faça uma versão escalar com as mesmas opções de otimização, removendo apenas a vetorização explícita.

## Exercícios
1. Varie L1D entre 16 e 64 KiB.
2. Compare `TimingSimpleCPU` e `O3CPU`, se disponível.
3. Use vetores de tamanhos que caibam e não caibam em L2.
