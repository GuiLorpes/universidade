# Tutorial GEM5 — Aceleradores Personalizados

## Introdução
O gem5 permite modelar componentes arquiteturais e conectar objetos SimObject ao sistema. Este tutorial propõe um acelerador de soma de blocos (block reduction), comparando uma versão executada pela CPU com uma versão que usa um dispositivo modelado.

## Objetivo
Definir o escopo de um acelerador, criar um modelo inicial simples, conectá-lo a um sistema SE e estabelecer métricas corretas para a comparação.

## Pré-requisitos
- gem5 compilado para X86 ou outra ISA-alvo;
- familiaridade com C++, Python e processo de build do gem5;
- uma cópia do código-fonte do gem5.

## Conceitos
Um acelerador útil precisa de interface, modelo temporal e acesso à memória. Um modelo funcional que retorna resultados instantaneamente **não** é uma avaliação de desempenho válida. Comece com um modelo de latência fixa e evolua para portas, filas, DMA e contenção de memória.

## Prática

### Etapa 1 — Definir o caso de uso
A operação é:

\[
S = \sum_{i=0}^{N-1} x_i
\]

A CPU executará uma redução escalar. O acelerador receberá endereço base, tamanho e endereço de resultado. Para uma primeira versão, use uma latência configurável proporcional ao número de elementos.

### Etapa 2 — Criar a interface SimObject
Em `src/dev/BlockReducer.py`:

```python
from m5.params import Param, Addr
from m5.SimObject import SimObject
class BlockReducer(SimObject):
    type = 'BlockReducer'
    cxx_header = 'dev/block_reducer.hh'
    cxx_class = 'gem5::BlockReducer'
    base_latency = Param.Latency('20ns', 'Latência de partida')
    cycles_per_element = Param.Unsigned(1, 'Ciclos por elemento')
    result_addr = Param.Addr(0, 'Endereço do resultado')
```

Inclua o objeto no `SConscript` do diretório. Crie a implementação C++ correspondente, derivada de uma classe apropriada ao tipo de interface escolhido. Para um dispositivo conectado a memória, implemente portas de requisição/resposta e não ignore retornos de memória.

### Etapa 3 — Implementar um modelo mínimo
O modelo deve:

1. receber uma solicitação de início;
2. calcular o instante de conclusão a partir de `base_latency` e `cycles_per_element`;
3. emitir leituras dos blocos de entrada;
4. acumular os dados recebidos;
5. escrever o resultado e sinalizar conclusão.

Compile novamente:

```bash
scons build/X86/gem5.opt -j$(nproc)
```

### Etapa 4 — Implementar o programa de referência
Crie `reduce_cpu.c`:

```c
#include <stdio.h>
#define N (1<<20)
static int x[N];
int main(void) {
  long long s=0;
  for (int i=0;i<N;i++) { x[i]=i&255; s+=x[i]; }
  printf("soma=%lld\n", s);
  return 0;
}
```

Para acionar um dispositivo real, a aplicação precisa de um driver, região MMIO ou interface de syscall definida pelo seu modelo. Não substitua essa interface por uma chamada C comum se o objetivo for medir o dispositivo.

### Etapa 5 — Instanciar no script Python
No script SE, importe e conecte o objeto à interconexão usada pelo sistema. Exemplo conceitual:

```python
from m5.objects import BlockReducer
board.block_reducer = BlockReducer(base_latency="20ns", cycles_per_element=1)
# Conecte a porta do dispositivo ao barramento/coherent I/O conforme seu modelo.
```

A ligação exata depende das portas declaradas no SimObject. Verifique `config.ini` para confirmar que o objeto foi instanciado e conectado.

### Etapa 6 — Campanha experimental
Compare:

| Caso | Execução | Parâmetro |
|---|---|---|
| CPU | redução escalar | — |
| ACC-1 | acelerador | 1 ciclo/elemento |
| ACC-4 | acelerador | 4 ciclos/elemento |

Use a mesma entrada, CPU, memória e caches. Colete ciclos, acessos de memória, latência média e estatísticas específicas do acelerador.

## Análise
O speedup é `ciclos_CPU / ciclos_ACEL`. Porém, reporte também tráfego de memória e ocupação do barramento: um acelerador pode reduzir tempo de CPU e aumentar pressão sobre DRAM. Valide o valor final da soma em todos os casos.

## Exercícios
1. Adicione uma FIFO de comandos e avalie filas de espera.
2. Modele transferências DMA em blocos de 64 B.
3. Compare dois aceleradores concorrentes acessando a mesma memória.
