# Tutorial GEM5 — Checkpoints e Restauração

## Introdução
Checkpoints salvam o estado de uma simulação para que ela seja retomada posteriormente. Eles são especialmente úteis em Full System, onde o boot do sistema operacional pode representar grande parte do tempo de uma campanha.

## Objetivo
Criar um checkpoint após o boot, restaurá-lo em execuções posteriores e usar esse mecanismo corretamente em uma campanha comparativa.

## Pré-requisitos
- gem5 e recursos compatíveis de kernel/imagem para FS;
- espaço em disco suficiente;
- uma carga executável dentro da imagem convidada.

## Conceitos
Um checkpoint contém estado de CPU, memória e objetos simulados. Ele é vinculado à ISA, versão/configuração e, frequentemente, à estrutura de objetos usada para criá-lo. Restaurar um checkpoint em uma configuração incompatível pode falhar ou, pior, produzir resultados inválidos.

## Prática

### Etapa 1 — Preparar a execução de boot
Crie um script de inicialização do sistema convidado que apenas indique que o boot terminou e aguarde. Em uma campanha real, use um script `rcS` para chegar a um estado conhecido.

```sh
#!/bin/sh
echo "Sistema pronto para checkpoint"
m5 checkpoint
m5 exit
```

A disponibilidade do utilitário `m5` depende da imagem. Inclua os binários `m5` adequados à ISA.

### Etapa 2 — Criar o checkpoint
Execute a configuração FS com kernel, disco e script:

```bash
build/ARM/gem5.opt --outdir=out/boot \
  configs/example/arm/fs_bigLITTLE.py \
  --kernel=vmlinux --disk=arm-disk.img --bootscript=checkpoint.rcS
```

Localize o diretório criado, normalmente semelhante a:

```text
out/boot/cpt.<tick>/
```

Guarde junto dele `config.ini`, `config.json`, `stats.txt`, hash do gem5 e identificação da imagem.

### Etapa 3 — Restaurar o checkpoint
A sintaxe varia entre scripts. Em muitos scripts legados, use uma opção semelhante a:

```bash
build/ARM/gem5.opt --outdir=out/restored \
  configs/example/arm/fs_bigLITTLE.py \
  --kernel=vmlinux --disk=arm-disk.img \
  --restore-with-cpu=TimingSimpleCPU \
  --checkpoint-dir=out/boot/cpt.<tick>
```

Consulte `--help` do script. Nas APIs modernas, a restauração é configurada no objeto `Simulator` ou no board. Não assuma que todas as versões aceitam os mesmos argumentos.

### Etapa 4 — Delimitar a região de interesse
No convidado, execute:

```sh
m5 resetstats
/home/gem5/workload
m5 dumpstats
m5 exit
```

O checkpoint reduz tempo de preparação; `resetstats` impede que o boot contamine as métricas do workload.

### Etapa 5 — Usar checkpoints em campanhas
Fluxo recomendado:

1. inicialize o SO uma vez e crie o checkpoint;
2. restaure a mesma base para cada configuração experimental;
3. execute a mesma carga e entrada;
4. colete apenas estatísticas da região de interesse;
5. valide se os `config.ini` diferem apenas nos parâmetros planejados.

## Análise
Compare o tempo de parede das campanhas com e sem checkpoint, mas não misture esse tempo com `simSeconds` do workload. O benefício principal é reduzir a simulação de fases repetidas; ele não torna comparáveis configurações estruturalmente incompatíveis.

## Problemas comuns
- **Falha ao restaurar:** confirme ISA, build, kernel, imagem e topologia compatíveis.
- **Resultados diferentes entre execuções:** verifique seed, dados de entrada, script de boot e sincronização.
- **Checkpoint grande:** reduza memória modelada apenas se isso não alterar o experimento.

## Exercícios
1. Crie checkpoints antes e depois de iniciar um serviço do SO.
2. Compare a duração de três configurações usando uma única base restaurada.
3. Documente um manifesto de reprodutibilidade para cada checkpoint.
