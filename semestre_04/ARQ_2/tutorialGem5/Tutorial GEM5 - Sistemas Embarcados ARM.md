# Tutorial GEM5 — Sistemas Embarcados ARM

## Introdução
Este tutorial apresenta uma campanha de simulação de uma plataforma ARM embarcada no gem5, usando **Full System (FS)**. O experimento mede o impacto de frequência e hierarquia de cache em uma carga de processamento de sensores.

## Objetivo
Inicializar Linux ARM no gem5, executar uma aplicação embarcada e coletar métricas de desempenho e memória de forma reprodutível.

## Pré-requisitos
- gem5 compilado para ARM: `scons build/ARM/gem5.opt -j$(nproc)`;
- imagem de disco ARM64/ARM fornecida ou construída para gem5;
- kernel compatível e DTB, quando exigidos pela plataforma;
- host Linux com Python 3.

> FS modela kernel, dispositivos e E/S. Portanto, é mais lento que SE, mas representa melhor um sistema embarcado real.

## Conceitos
Uma plataforma embarcada combina CPU, memória, periféricos e sistema operacional. Para uma análise arquitetural, separe sempre: (1) tempo de boot, (2) região de interesse da aplicação e (3) desligamento. As estatísticas globais incluem o boot e não devem ser usadas diretamente como resultado do programa.

## Prática

### Etapa 1 — Criar a carga de trabalho
Crie `sensor_filter.c`:

```c
#include <stdint.h>
#include <stdio.h>
#define N 1048576
static int16_t in[N], out[N];
int main(void) {
  for (int i=0;i<N;i++) in[i]=(i*17)%1024;
  for (int i=2;i<N-2;i++) out[i]=(in[i-2]+2*in[i-1]+3*in[i]+2*in[i+1]+in[i+2])/9;
  printf("checksum=%d\n", out[N-10]);
  return 0;
}
```

Compile na arquitetura-alvo, copie o binário para a imagem de disco e torne-o executável:

```bash
arm-linux-gnueabihf-gcc -O2 sensor_filter.c -o sensor_filter
sudo mount -o loop arm-disk.img /mnt
sudo cp sensor_filter /mnt/home/gem5/
sudo umount /mnt
```

### Etapa 2 — Preparar o script de comandos
Crie `run.rcS` e coloque-o na imagem ou informe-o ao script de configuração:

```sh
#!/bin/sh
cd /home/gem5
m5 resetstats
./sensor_filter
m5 dumpstats
m5 exit
```

`m5 resetstats` delimita a região de interesse; `dumpstats` grava as métricas antes da saída.

### Etapa 3 — Executar a plataforma ARM
Use um script de exemplo correspondente à versão instalada do gem5. Um padrão comum é:

```bash
build/ARM/gem5.opt configs/example/arm/fs_bigLITTLE.py \
  --kernel=vmlinux --disk=arm-disk.img --bootscript=run.rcS \
  --cpu-type=timing --num-cores=1 --cpu-clock=1GHz \
  --caches --l2cache --l1d_size=32kB --l1i_size=32kB --l2_size=512kB \
  --outdir=out/arm-1ghz
```

Os nomes de opções e scripts podem variar entre versões; confirme com `--help`. Não misture kernel, imagem e ISA incompatíveis.

### Etapa 4 — Variar a configuração
Execute, mantendo programa, imagem, kernel e comando idênticos:

| Experimento | Clock | L1D | L2 |
|---|---:|---:|---:|
| A | 1 GHz | 32 KiB | 512 KiB |
| B | 2 GHz | 32 KiB | 512 KiB |
| C | 1 GHz | 64 KiB | 1 MiB |

### Etapa 5 — Extrair resultados

```bash
grep -E 'simSeconds|simTicks|system.cpu.numCycles|dcache.overallMissRate' out/arm-*/stats.txt
```

Registre o intervalo entre `Begin Simulation Statistics` associado ao `dumpstats` da aplicação.

## Análise
Compare `system.cpu.numCycles`, taxa de faltas de L1D e acessos à memória. Aumentar o clock pode reduzir tempo simulado, mas não reduz necessariamente ciclos nem faltas. Uma cache maior pode diminuir faltas e ciclos, ao custo de área/energia que devem ser avaliadas em ferramenta complementar.

## Boas práticas
- Use checkpoints após o boot para não repeti-lo em cada experimento.
- Fixe a versão do kernel, imagem, gem5 e compilador.
- Repita testes com entradas distintas quando houver comportamento dependente dos dados.
- Documente a região de interesse e as métricas coletadas.

## Exercícios
1. Compare uma CPU `TimingSimpleCPU` e `MinorCPU`.
2. Altere o filtro para janela de 9 amostras e avalie o efeito em cache.
3. Use dois núcleos e distribua blocos do vetor entre processos.
