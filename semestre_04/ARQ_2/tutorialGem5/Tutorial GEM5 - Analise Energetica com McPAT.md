# Tutorial GEM5 — Análise Energética com gem5 e McPAT

## Introdução

O gem5 é um simulador de arquitetura orientado principalmente a desempenho e comportamento microarquitetural. Ele fornece contadores como ciclos, instruções e acessos à cache, mas não estima energia diretamente para todas as configurações. O **McPAT** é uma ferramenta de modelagem que usa parâmetros arquiteturais e estatísticas de execução para estimar potência e energia.

## Objetivo

Este tutorial apresenta uma metodologia para comparar duas configurações de CPU e cache em termos de desempenho e energia. Ao final, você deverá conseguir:

- executar um benchmark em modo SE por uma configuração Python;
- coletar os arquivos de saída do gem5;
- preparar dados de configuração e estatísticas para o McPAT;
- calcular energia, desempenho por watt e produto energia-atraso (EDP);
- identificar limitações e hipóteses do método.

> **Pré-requisitos:** gem5 para `X86`, Python 3, compilador C, instalação local do McPAT e familiaridade com o modo SE. McPAT e gem5 devem ser documentados com as versões usadas no experimento.

---

## 1. Conceitos fundamentais

### 1.1 Potência, energia e EDP

A potência média é expressa em watts (W). Para uma execução de duração $T$, a energia aproximada é:

\[
E = P_{medio} \times T
\]

O produto energia-atraso combina ambos os objetivos:

\[
EDP = E \times T
\]

Menor EDP é geralmente desejável quando desempenho e energia têm importância semelhante. Ele não substitui requisitos específicos de potência máxima ou tempo máximo.

### 1.2 Limitações do acoplamento

O McPAT produz **estimativas**, não medições físicas. Resultados dependem de tecnologia, tensão, frequência, organização da cache, atividade dinâmica e mapeamento correto dos parâmetros. Não compare valores absolutos de estudos distintos sem garantir as mesmas premissas.

---

## 2. Etapa prática 1 — Preparar o experimento

```bash
mkdir -p experiments/energia/{src,bin,configs,resultados,mcpat}
cd experiments/energia
```

O experimento compara duas configurações:

| Configuração | CPU | L1-D | Hipótese |
|---|---|---:|---|
| A | `TimingSimpleCPU` | 32 KiB | Menor estrutura e custo estimado |
| B | `O3CPU` | 64 KiB | Maior desempenho, potencialmente maior potência |

A comparação é didática. Em estudos reais, use modelos e parâmetros que correspondam adequadamente à microarquitetura simulada.

---

## 3. Etapa prática 2 — Implementar o benchmark

Crie `src/filtro.c`:

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N (1 << 20)
#define RODADAS 30

int main(void) {
    int *entrada = malloc(N * sizeof(int));
    int *saida = malloc(N * sizeof(int));
    if (!entrada || !saida) return 1;

    for (int i = 0; i < N; i++) entrada[i] = (i * 17) & 1023;

    uint64_t checksum = 0;
    for (int r = 0; r < RODADAS; r++) {
        for (int i = 1; i < N - 1; i++) {
            saida[i] = (entrada[i - 1] + 2 * entrada[i] + entrada[i + 1]) / 4;
            checksum += (unsigned)saida[i];
        }
        int *tmp = entrada; entrada = saida; saida = tmp;
    }

    printf("checksum=%llu\n", (unsigned long long)checksum);
    free(entrada);
    free(saida);
    return 0;
}
```

Compile:

```bash
gcc -O2 -static -o bin/filtro src/filtro.c
```

---

## 4. Etapa prática 3 — Criar a configuração Python

Crie `configs/energia.py`:

```python
import argparse
import m5
from m5.objects import *

parser = argparse.ArgumentParser()
parser.add_argument("--cpu", choices=["timing", "o3"], required=True)
parser.add_argument("--l1d", default="32KiB")
parser.add_argument("--cmd", required=True)
args = parser.parse_args()

cpu_cls = TimingSimpleCPU if args.cpu == "timing" else O3CPU

system = System()
system.clk_domain = SrcClockDomain(clock="2GHz",
                                   voltage_domain=VoltageDomain())
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MiB")]
system.cpu = cpu_cls(cpu_id=0)
system.membus = SystemXBar()

system.cpu.icache = Cache(size="32KiB", assoc=4, tag_latency=1,
                          data_latency=1, response_latency=1,
                          mshrs=4, tgts_per_mshr=20)
system.cpu.dcache = Cache(size=args.l1d, assoc=4, tag_latency=1,
                          data_latency=1, response_latency=1,
                          mshrs=8, tgts_per_mshr=20)
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port
system.cpu.icache.mem_side = system.membus.cpu_side_ports
system.cpu.dcache.mem_side = system.membus.cpu_side_ports

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

process = Process()
process.cmd = [args.cmd]
system.cpu.workload = process
system.cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()
event = m5.simulate()
print(event.getCause())
```

---

## 5. Etapa prática 4 — Executar as configurações

A partir da raiz do gem5:

```bash
build/X86/gem5.opt \
  --outdir=experiments/energia/resultados/A_timing_32k \
  experiments/energia/configs/energia.py \
  --cpu=timing --l1d=32KiB --cmd=experiments/energia/bin/filtro

build/X86/gem5.opt \
  --outdir=experiments/energia/resultados/B_o3_64k \
  experiments/energia/configs/energia.py \
  --cpu=o3 --l1d=64KiB --cmd=experiments/energia/bin/filtro
```

Cada diretório deve conter, no mínimo, `config.ini`, `stats.txt` e `simout`. Confirme que ambos os cenários imprimem o mesmo `checksum`.

---

## 6. Etapa prática 5 — Coletar dados do gem5

Extraia estatísticas básicas:

```bash
for d in A_timing_32k B_o3_64k; do
  echo "=== $d ==="
  grep -E '^simSeconds|^simInsts|^system.cpu.numCycles|^system.cpu.ipc|dcache.overall(Misses|MissRate)' \
    experiments/energia/resultados/$d/stats.txt
done
```

Arquivos importantes:

- `config.ini`: parâmetros efetivos dos objetos simulados;
- `stats.txt`: contadores e métricas da execução;
- `simout`: saída do programa e mensagens relevantes;
- `config.json`: alternativa estruturada para automação, se gerada pela sua versão.

---

## 7. Etapa prática 6 — Preparar o McPAT

O McPAT recebe normalmente um XML de entrada. A estrutura e os campos disponíveis variam conforme a versão. Use o XML de exemplo distribuído com sua instalação como base, em vez de criar um XML mínimo sem verificar o esquema.

Copie um modelo:

```bash
cp /caminho/para/mcpat/processor.xml mcpat/A_timing_32k.xml
cp /caminho/para/mcpat/processor.xml mcpat/B_o3_64k.xml
```

Para cada XML, ajuste de maneira consistente:

1. **Tecnologia e clock:** por exemplo, tecnologia de 45 nm e frequência de 2000 MHz, se essas forem as hipóteses do estudo.
2. **Núcleos:** um núcleo no experimento atual.
3. **Estrutura do core:** largura, filas, predição e unidades funcionais devem representar o modelo escolhido. `O3CPU` exige uma descrição diferente de `TimingSimpleCPU`.
4. **Caches:** tamanho, associatividade, tamanho de linha e número de portas devem corresponder à configuração gem5.
5. **Atividade:** substitua contadores de instruções, acessos, leituras e escritas pelos valores de `stats.txt`.

Um fragmento ilustrativo de parâmetro no XML é:

```xml
<param name="clock_rate" value="2000"/>
<param name="number_of_cores" value="1"/>
<param name="instruction_buffer_size" value="32"/>
```

Os nomes exatos e os campos obrigatórios dependem do modelo XML utilizado. Não copie valores arbitrários: a qualidade da estimativa depende dessa correspondência.

### Automação recomendada

Para campanhas maiores, escreva um conversor Python que leia `config.json` e `stats.txt`, preencha um XML-base e valide os campos antes de invocar o McPAT. Registre no relatório quais estatísticas alimentam cada contador do McPAT.

---

## 8. Etapa prática 7 — Executar o McPAT e calcular métricas

Com o executável McPAT compilado, o comando costuma seguir este padrão:

```bash
/caminho/para/mcpat/mcpat -infile mcpat/A_timing_32k.xml > mcpat/A_timing_32k.out
/caminho/para/mcpat/mcpat -infile mcpat/B_o3_64k.xml > mcpat/B_o3_64k.out
```

Localize no relatório a potência total estimada, por exemplo `Processor: Total Power`. Depois, use o valor de `simSeconds` para calcular energia:

```bash
# Exemplo de cálculo: substitua P e T pelos valores obtidos.
python3 - <<'PY'
P = 1.25      # W
T = 0.0038    # s
E = P * T
print(f"Energia: {E:.6f} J")
print(f"EDP: {E*T:.9e} J.s")
PY
```

Monte uma tabela:

| Configuração | Tempo (s) | Potência (W) | Energia (J) | EDP (J·s) |
|---|---:|---:|---:|---:|
| A |  |  |  |  |
| B |  |  |  |  |

---

## 9. Interpretação dos resultados

A configuração O3 pode reduzir o tempo de execução e, simultaneamente, elevar a potência média. A decisão depende de qual efeito predomina na energia total e no EDP. Uma cache maior também pode reduzir acessos à DRAM, mas ocupa mais área e pode aumentar a energia por acesso.

Evite afirmar que uma configuração é “mais eficiente” apenas por ter menor potência. Compare energia para concluir o mesmo trabalho e use o EDP se o atraso também for relevante.

---

## 10. Exercícios

1. Compare L1-D de 16, 32 e 64 KiB mantendo a CPU constante.
2. Varie a frequência no modelo de potência, documentando a hipótese de tensão correspondente.
3. Separe a contribuição estimada de core, caches e memória no relatório McPAT.
4. Repita com um benchmark mais computacional e compare a sensibilidade às caches.
5. Crie um script que produza um CSV com desempenho, potência, energia e EDP.

## Conclusão

Você usou o gem5 para obter comportamento de execução e o McPAT para estimar custos energéticos. A principal exigência metodológica é manter consistência entre a microarquitetura simulada, os contadores coletados e os parâmetros fornecidos ao modelo energético.
