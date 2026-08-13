# Tutorial GEM5 — Sistemas Heterogêneos big.LITTLE

## Introdução
Um sistema heterogêneo combina núcleos de alto desempenho com núcleos mais simples e econômicos. A ideia é executar cada fase da carga no tipo de núcleo mais adequado, equilibrando desempenho e custo energético.

## Objetivo
Montar uma configuração FS ARM com dois tipos de CPU, executar uma aplicação em fases e comparar a execução em núcleo rápido e núcleo econômico.

## Pré-requisitos
- build ARM do gem5;
- kernel, disco e bootloader ARM compatíveis com a configuração;
- aplicação ARM estática ou pacote instalado na imagem;
- familiaridade com modo FS.

## Conceitos
No gem5, uma aproximação de big.LITTLE pode usar modelos distintos de CPU, como um núcleo mais detalhado para o grupo “big” e um modelo mais simples para o grupo “little”. Isso é uma abstração: os resultados dependem dos modelos e parâmetros escolhidos, não sendo uma reprodução automática de um SoC comercial.

## Prática

### Etapa 1 — Escolher os modelos
Defina, por exemplo:

| Grupo | Modelo | Papel experimental |
|---|---|---|
| big | `O3CPU` | maior capacidade de execução fora de ordem |
| little | `MinorCPU` ou `TimingSimpleCPU` | menor complexidade de modelagem |

Use o mesmo ISA, frequência explicitamente definida e hierarquia de memória documentada.

### Etapa 2 — Criar uma aplicação por fases
Crie `fases.c`:

```c
#include <stdio.h>
#include <stdint.h>
volatile uint64_t soma;
int main(void) {
  for (uint64_t i = 0; i < 200000000ULL; i++) soma += (i * 17) ^ (i >> 3);
  printf("fase computacional: %llu\n", (unsigned long long)soma);
  return 0;
}
```

Compile para ARM com o compilador cruzado apropriado:

```bash
aarch64-linux-gnu-gcc -O2 -static fases.c -o fases_arm64
```

Ajuste o triplet para sua ISA e imagem.

### Etapa 3 — Preparar a imagem FS
Copie o executável para a imagem de disco ou disponibilize-o por mecanismo já usado na sua plataforma. Crie um script de inicialização que execute a aplicação e desligue o sistema:

```sh
#!/bin/sh
/path/fases_arm64 > /tmp/resultado.txt
m5 exit
```

O mecanismo para injetar esse script depende da imagem e do exemplo ARM adotado.

### Etapa 4 — Montar o script Python
Parta de uma configuração FS ARM funcional. Crie dois conjuntos de CPUs com a mesma ISA e conecte ambos à hierarquia de memória. Para o primeiro experimento, mantenha apenas um conjunto ativo por execução: isso torna a comparação interpretável.

Parâmetros recomendados no script:

```python
parser.add_argument("--tipo-cpu", choices=["big", "little"], required=True)
parser.add_argument("--cpu-clock", default="2GHz")
```

Associe `big` e `little` ao modelo de CPU escolhido. Não faça troca dinâmica de CPU antes de validar as execuções independentes.

### Etapa 5 — Executar os cenários

```bash
for tipo in big little; do
  build/ARM/gem5.opt configs/biglittle_fs.py \
    --outdir="resultados/biglittle/${tipo}" --tipo-cpu="$tipo" \
    --disk-image=imagem-arm.img --kernel=vmlinux
 done
```

### Etapa 6 — Analisar

```bash
grep -E 'simSeconds|simTicks|system.cpu.*numCycles|ipc|cpi' \
  resultados/biglittle/big/stats.txt
```

Compare tempo, IPC, CPI e, se houver integração energética, potência estimada. Núcleos diferentes podem produzir números de IPC incomparáveis como medida isolada; priorize tempo, trabalho concluído e energia sob premissas registradas.

## Limitações
Troca de tarefas entre grupos, escalonamento do Linux e DVFS exigem modelagem adicional. O tutorial mede cenários separados, não afirma que o SO implementou automaticamente uma política big.LITTLE real.

## Exercícios
1. Compare uma carga computacional e uma carga com muitos acessos à memória.
2. Varie a frequência de cada grupo.
3. Integre a coleta energética e avalie energia por trabalho concluído.