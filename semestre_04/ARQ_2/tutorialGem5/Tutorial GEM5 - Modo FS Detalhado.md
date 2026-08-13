# Tutorial gem5: modo Full System (FS) detalhado

## Introdução

O modo **Full System (FS)** do gem5 simula uma máquina completa: processador, hierarquia de memória, dispositivos de E/S, firmware, kernel e um sistema operacional convidado. Diferentemente do modo **System-call Emulation (SE)**, o programa não é iniciado diretamente pelo simulador. Ele é executado _dentro_ do sistema operacional que inicializa na máquina simulada.

Este tutorial apresenta um fluxo completo para executar e analisar um programa em FS. O programa exemplo será uma **busca de números primos por divisão de intervalos**, escolhida para evitar os exemplos de soma de vetores e multiplicação de matrizes. Ele permite observar a diferença entre uma carga predominantemente de cálculo inteiro e uma carga com acessos à memória previsíveis.

> Os caminhos exatos de imagens, kernels e scripts podem variar entre versões e distribuições de recursos do gem5. Antes de executar um comando, confirme os nomes disponíveis no seu clone e no repositório de recursos.

## Objetivos

Ao final, você deverá conseguir:

1. Diferenciar FS de SE e decidir quando FS é necessário;
2. Preparar os artefatos de boot: binário gem5, kernel e imagem de disco;
3. Implementar e compilar um programa para a arquitetura convidada;
4. Colocar o executável e um script de execução na imagem de disco;
5. Executar FS pela linha de comando;
6. Executar FS por uma configuração baseada na API Python do gem5;
7. Localizar e interpretar `stats.txt`, `config.ini` e `system.terminal`.

---

# 1. O que é o modo Full System

No FS, o gem5 modela a plataforma necessária para inicializar um SO real. Para uma plataforma x86 típica, isso inclui CPUs simuladas, RAM, controladores, dispositivos de armazenamento, console serial, kernel Linux e uma imagem de disco com sistema de arquivos raiz.

O fluxo é:

```text
host → gem5 → firmware/boot → kernel Linux convidado → init → script na imagem → programa
```

Assim, chamadas de sistema, criação de processos, carregamento de bibliotecas, paginação, interrupções, E/S e escalonamento são tratados pelo kernel convidado, e não emulados diretamente pelo gem5.

## 1.1 Quando usar FS

Use FS quando o experimento depender do comportamento do sistema operacional ou de dispositivos. Exemplos: estudo de boot, drivers, sistema de arquivos, rede, multiprocessamento com processos/threads, interrupções, virtualização ou políticas de memória do kernel.

Para apenas executar um binário simples e medir CPU/cache, SE é normalmente mais rápido e mais simples. FS tem maior fidelidade de sistema, mas também maior custo, tempo de inicialização e complexidade de preparação.

## 1.2 O que é simulado e o que permanece no host

O gem5 é executado no host, mas o Linux inicializado na simulação é um **convidado**. Os comandos digitados no terminal serial pertencem ao convidado. Já comandos como `scons`, `gem5.opt` e a leitura do diretório `m5out/` são feitos no host.

---

# 2. Pré-requisitos

Este tutorial usa a ISA x86 e Linux no host. Adapte `X86` e os recursos caso escolha outra arquitetura.

Você precisa de:

- um clone do gem5 compilado para x86;
- Python 3 e dependências de build do gem5;
- `gcc` ou `clang` no host para gerar o programa x86-64;
- um kernel compatível com a plataforma x86 do gem5;
- uma imagem de disco Linux compatível;
- os recursos do gem5 baixados ou disponíveis localmente.

## Etapa 2.1 — Compilar o gem5

No diretório raiz do projeto:

```bash
scons build/X86/gem5.opt -j"$(nproc)"
```

Verifique o executável:

```bash
build/X86/gem5.opt --version
```

Para depuração, substitua `gem5.opt` por `gem5.debug`. Para experimentos de desempenho, use `gem5.opt`.

## Etapa 2.2 — Obter recursos

O projeto mantém recursos versionados e descritos por meio do gem5 Resources. Consulte os recursos disponíveis no seu checkout:

```bash
python3 -m gem5.resources.downloader --list | grep -i x86
```

Em versões que oferecem o utilitário, um recurso pode ser obtido assim:

```bash
python3 -m gem5.resources.downloader --get-resource <nome-do-recurso>
```

Alternativamente, use os caminhos locais de um kernel e de uma imagem fornecidos pelo ambiente da disciplina/laboratório. Neste tutorial, defina:

```bash
export GEM5_ROOT="$HOME/gem5"
export KERNEL="/caminho/para/vmlinux"
export DISK_IMAGE="/caminho/para/disco.img"
```

O kernel costuma ser um arquivo `vmlinux` sem compressão. A imagem de disco é comumente um arquivo `.img`, por exemplo contendo Ubuntu ou outra distribuição preparada para gem5.

---

# 3. Programa exemplo: busca de números primos

O programa calcula quantos números primos existem entre 2 e um limite informado na linha de comando. Um número é classificado por divisão por possíveis fatores até sua raiz quadrada.

O algoritmo não é o método mais eficiente para primos; isso é intencional: ele fornece uma carga determinística, fácil de validar e com trabalho computacional suficiente para gerar estatísticas observáveis.

## Etapa 3.1 — Criar o código fonte

No host, crie `conta_primos.c`:

```c
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int eh_primo(uint64_t n)
{
    if (n < 2)
        return 0;
    if (n == 2)
        return 1;
    if ((n % 2) == 0)
        return 0;

    for (uint64_t d = 3; d <= n / d; d += 2) {
        if ((n % d) == 0)
            return 0;
    }
    return 1;
}

int main(int argc, char **argv)
{
    uint64_t limite = 200000;
    uint64_t quantidade = 0;
    uint64_t ultimo = 0;

    if (argc == 2) {
        char *fim = NULL;
        limite = strtoull(argv[1], &fim, 10);
        if (*argv[1] == '\0' || *fim != '\0' || limite < 2) {
            fprintf(stderr, "Uso: %s [limite >= 2]\n", argv[0]);
            return 1;
        }
    }

    for (uint64_t n = 2; n <= limite; ++n) {
        if (eh_primo(n)) {
            ++quantidade;
            ultimo = n;
        }
    }

    printf("limite=%" PRIu64 " primos=%" PRIu64 " ultimo=%" PRIu64 "\n",
           limite, quantidade, ultimo);
    return 0;
}
```

A expressão `d <= n / d` evita estouro que poderia ocorrer em `d * d <= n` para valores muito grandes.

## Etapa 3.2 — Compilar para o convidado

Se host e convidado são ambos x86-64, uma compilação nativa normalmente é suficiente:

```bash
gcc -O2 -Wall -Wextra -o conta_primos conta_primos.c
```

Com Clang:

```bash
clang -O2 -Wall -Wextra -o conta_primos conta_primos.c
```

Verifique a arquitetura gerada:

```bash
file conta_primos
```

A saída deve indicar `ELF 64-bit ... x86-64`. Se o host tiver outra ISA ou o convidado for ARM/RISC-V, use um compilador cruzado e confirme que o ELF corresponde à arquitetura do convidado, por exemplo:

```bash
aarch64-linux-gnu-gcc -O2 -o conta_primos conta_primos.c
file conta_primos
```

Evite opções como `-march=native`: elas podem produzir instruções não modeladas ou não suportadas pela CPU configurada no gem5. Prefira uma base conservadora, como `-O2`.

Teste no host apenas como validação lógica:

```bash
./conta_primos 100
# Resultado esperado: limite=100 primos=25 ultimo=97
```

---

# 4. Preparar a imagem de disco

O programa precisa estar acessível ao Linux convidado. Há duas abordagens: modificar a imagem de disco ou transferir o binário após o boot. Para experimentos repetíveis, modificar ou criar uma imagem de trabalho é a opção mais robusta.

## Etapa 4.1 — Nunca modificar a imagem-base

Crie uma cópia para o experimento:

```bash
cp "$DISK_IMAGE" disco-primos.img
export DISK_IMAGE="$PWD/disco-primos.img"
```

Isso protege o recurso original e permite reiniciar o experimento do mesmo estado.

## Etapa 4.2 — Montar e inserir arquivos

Imagens podem ter partições. Primeiro inspecione-as:

```bash
fdisk -l "$DISK_IMAGE"
```

Em Linux, `guestmount` costuma ser mais seguro e prático que montar dispositivos de loop manualmente:

```bash
sudo mkdir -p /mnt/gem5-disco
sudo guestmount -a "$DISK_IMAGE" -i /mnt/gem5-disco
```

Copie o programa e crie o script `run-primos.sh`:

```bash
sudo mkdir -p /mnt/gem5-disco/opt/gem5
sudo cp conta_primos /mnt/gem5-disco/opt/gem5/
sudo tee /mnt/gem5-disco/opt/gem5/run-primos.sh >/dev/null <<'EOF'
#!/bin/sh
set -eu

m5 resetstats
/opt/gem5/conta_primos 200000
m5 dumpstats
m5 exit
EOF
sudo chmod +x /mnt/gem5-disco/opt/gem5/conta_primos
sudo chmod +x /mnt/gem5-disco/opt/gem5/run-primos.sh
sync
sudo guestunmount /mnt/gem5-disco
```

O script usa a pseudo-instrução `m5` para delimitar a região de interesse:

- `m5 resetstats`: zera os contadores antes do programa;
- `m5 dumpstats`: grava as estatísticas ao final do programa;
- `m5 exit`: pede ao gem5 que encerre a simulação.

A imagem convidada deve conter o utilitário `m5`. Imagens preparadas para gem5 normalmente o oferecem. Caso não esteja no `PATH`, instale-o na imagem ou informe o caminho absoluto, como `/sbin/m5`.

> Se `guestmount` não estiver disponível, monte a imagem com `qemu-nbd` ou `losetup -P` conforme a política do seu sistema. Desmonte tudo corretamente antes de iniciar o gem5, pois executar com a imagem ainda montada pode corrompê-la.

---

# 5. Linha de comando: execução FS

Configurações legadas, frequentemente presentes em `configs/deprecated/example/`, oferecem uma forma direta de iniciar FS. Os nomes e parâmetros variam por versão; execute `--help` para confirmar os argumentos no seu checkout.

## Etapa 5.1 — Inspecionar opções da configuração

```bash
cd "$GEM5_ROOT"
build/X86/gem5.opt configs/deprecated/example/fs.py --help
```

Procure argumentos para kernel, imagem de disco, tipo de CPU, memória, caches e script de inicialização.

## Etapa 5.2 — Criar um script de boot

Crie `boot-primos.rcS` no host:

```sh
#!/bin/sh
# Executado pelo sistema convidado após o boot, quando suportado pela imagem/configuração.
/opt/gem5/run-primos.sh
```

## Etapa 5.3 — Executar

Um formato comum de comando é:

```bash
build/X86/gem5.opt \
  --outdir=m5out/fs-primos-cli \
  configs/deprecated/example/fs.py \
  --kernel="$KERNEL" \
  --disk-image="$DISK_IMAGE" \
  --script="$PWD/boot-primos.rcS" \
  --cpu-type=TimingSimpleCPU \
  --caches \
  --l2cache \
  --mem-size=2GB
```

Se a configuração usada não reconhecer algum argumento, não tente adivinhar o nome: consulte o `--help` dela. Em algumas versões, a imagem é passada como `--disk-image`, em outras por um argumento ou configuração diferente.

O diretório `m5out/fs-primos-cli/` deverá conter, entre outros:

```text
config.ini
config.json
stats.txt
system.terminal
simout
simerr
```

O arquivo `system.terminal` registra o console serial do convidado. Ao fim, procure nele a linha produzida pelo programa:

```bash
grep 'limite=' m5out/fs-primos-cli/system.terminal
```

Também confirme que o guest solicitou a saída do simulador:

```bash
tail -n 30 m5out/fs-primos-cli/simout
```

## Etapa 5.4 — Se o boot parar no console

Se o script de boot não for aplicado pela imagem, use o console interativo. Inicie a simulação e, após o login do Linux convidado, execute:

```sh
/opt/gem5/run-primos.sh
```

O comando é digitado no terminal associado ao console serial, mas pertence ao SO convidado. Após `m5 exit`, o gem5 termina e grava os arquivos no `--outdir` do host.

---

# 6. Execução FS com a API Python do gem5

A API Python moderna permite descrever explicitamente placa, processador, memória, caches, disco e workload. A disponibilidade e a assinatura exata de algumas classes depende da versão; o exemplo abaixo segue a organização das versões recentes do gem5 e deve ser ajustado caso a sua árvore use nomes diferentes.

## Etapa 6.1 — Criar `fs_primos.py`

```python
from gem5.components.boards.x86_board import X86Board
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import DiskImageResource, KernelResource
from gem5.simulate.simulator import Simulator

KERNEL = "/caminho/para/vmlinux"
DISK_IMAGE = "/caminho/para/disco-primos.img"

cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1d_size="32KiB",
    l1i_size="32KiB",
    l2_size="256KiB",
)

memory = SingleChannelDDR4_2400(size="2GiB")
processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING,
    isa=ISA.X86,
    num_cores=1,
)

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# O readfile é copiado para o convidado e executado pelo mecanismo de boot
# suportado pela imagem/configuração x86.
board.set_kernel_disk_workload(
    kernel=KernelResource(local_path=KERNEL),
    disk_image=DiskImageResource(local_path=DISK_IMAGE, root_partition="1"),
    readfile_contents="/opt/gem5/run-primos.sh\n",
)

simulator = Simulator(board=board)
simulator.run()
```

Atualize `KERNEL`, `DISK_IMAGE` e `root_partition`. O valor de `root_partition` deve coincidir com a partição raiz da imagem; use `fdisk -l` ou `guestfish` para identificá-la. O método `set_kernel_disk_workload` configura o boot e disponibiliza o conteúdo de `readfile` para execução no convidado, conforme o fluxo adotado pelas imagens x86 preparadas para gem5.

## Etapa 6.2 — Executar a configuração

```bash
cd "$GEM5_ROOT"
build/X86/gem5.opt --outdir=m5out/fs-primos-python fs_primos.py
```

Valide a saída serial:

```bash
grep 'limite=' m5out/fs-primos-python/system.terminal
```

### Ajuste para versões diferentes

A API do gem5 evolui. Se o import ou o método de workload falhar, use exemplos fornecidos pela **mesma revisão** do seu gem5 como referência:

```bash
find configs -type f \( -name '*x86*' -o -name '*ubuntu*' \) | head -n 20
grep -R "set_kernel_disk_workload" -n configs tests 2>/dev/null | head
```

Preserve a ideia do experimento: `X86Board`, processador timing, hierarquia de cache, memória, kernel, imagem de disco e comando convidado que chama `m5 resetstats`, programa, `m5 dumpstats` e `m5 exit`.

---

# 7. Delimitar corretamente a região medida

Um experimento FS pode incluir bilhões de ticks de boot do Linux, serviços de inicialização e E/S. Se as estatísticas não forem reiniciadas, os números incluem o boot e deixam de representar apenas o programa.

O script do convidado resolve isso:

```sh
m5 resetstats
/opt/gem5/conta_primos 200000
m5 dumpstats
m5 exit
```

Em `stats.txt`, o gem5 pode registrar blocos separados por marcadores de estatística. A região desejada é a posterior a `resetstats` e anterior a `dumpstats`. Confirme a presença de múltiplos blocos:

```bash
grep -n "Begin Simulation Statistics\|End Simulation Statistics" \
  m5out/fs-primos-python/stats.txt
```

Para automatizar coleta em múltiplas fases, o programa ou script pode emitir vários `dumpstats`; documente sempre qual bloco foi usado na análise.

---

# 8. Interpretar `stats.txt`

Abra o arquivo gerado no diretório de saída:

```bash
less m5out/fs-primos-python/stats.txt
```

Os nomes exatos dependem dos componentes configurados. Comece confirmando o modelo efetivamente instanciado em `config.ini`:

```bash
grep -E "^type=|^clock=|^size=" m5out/fs-primos-python/config.ini | head -n 40
```

## 8.1 Métricas essenciais

| Métrica | Significado | Como usar |
|---|---|---|
| `simTicks` | Tempo simulado em ticks | Compare apenas a região delimitada e configurações equivalentes. |
| `simSeconds` | Tempo simulado convertido para segundos | Útil como duração da simulação modelada, não como tempo gasto pelo host. |
| `hostSeconds` | Tempo de parede no host | Mede custo de simulação, não desempenho da máquina simulada. |
| `system.cpu.numCycles` | Ciclos da CPU | Base para calcular CPI. |
| `system.cpu.committedInsts` ou `numInsts` | Instruções comprometidas/executadas | Use com ciclos para CPI; o nome varia por CPU. |
| estatísticas de `dcache`/`l1d` | Acessos, misses e taxa de miss da cache L1 de dados | Caracterizam o comportamento de dados. |
| estatísticas de `icache`/`l1i` | Acessos e misses da cache L1 de instruções | Normalmente baixas após aquecimento para este programa. |
| estatísticas de `l2` | Acessos e misses da L2 | Mostram faltas que escapam da L1. |

Localize itens sem presumir o caminho completo:

```bash
grep -E "simTicks|simSeconds|hostSeconds|numCycles|committedInsts|numInsts" \
  m5out/fs-primos-python/stats.txt

grep -Ei "(l1d|dcache|l2).*miss" m5out/fs-primos-python/stats.txt | head -n 30
```

## 8.2 Cálculos derivados

Para uma CPU que exponha ciclos e instruções comprometidas, o CPI é:

\[
\mathrm{CPI} = \frac{\text{numCycles}}{\text{committedInsts}}
\]

O IPC é:

\[
\mathrm{IPC} = \frac{\text{committedInsts}}{\text{numCycles}}
\]

Se houver contadores de acessos e faltas da cache, a taxa de faltas é:

\[
\mathrm{miss\ rate} = \frac{\text{misses}}{\text{acessos}}
\]

Não calcule CPI misturando ciclos de um bloco de estatísticas com instruções de outro. Para FS, essa precaução é especialmente importante por causa do boot.

## 8.3 O que esperar do programa de primos

A busca de primos usa variáveis escalares e possui pouca estrutura de dados grande. Em geral, depois do carregamento inicial do código, ela tende a apresentar poucos misses de dados quando comparada a algoritmos que percorrem vetores ou matrizes extensas. O custo principal está em divisões, desvios condicionais e execução de instruções inteiras.

Isso não é uma garantia universal: a CPU escolhida, compilador, otimizações, tamanho do problema, bibliotecas e ruído do SO podem alterar os resultados. Trate a hipótese como algo a testar, não como uma conclusão prévia.

---

# 9. Experimento controlado: tamanho de L1 de dados

Modifique apenas o tamanho da L1 de dados no script Python:

```python
l1d_size="16KiB"
```

Depois execute uma segunda vez com:

```python
l1d_size="64KiB"
```

Use diretórios de saída separados:

```bash
build/X86/gem5.opt --outdir=m5out/primos-l1-16k fs_primos.py
# edite l1d_size para 64KiB
build/X86/gem5.opt --outdir=m5out/primos-l1-64k fs_primos.py
```

Registre, para a região delimitada, `committedInsts`, `numCycles`, CPI e misses L1/L2. Como a carga possui pequeno conjunto de dados, uma mudança grande de L1 pode ter efeito limitado. Esse resultado também é válido: significa que, para essa carga e modelo, a L1 não era o gargalo dominante.

Mantenha constantes kernel, imagem, entrada (`200000`), tipo de CPU, frequência, memória, demais caches e número de núcleos. Mudar vários fatores de uma vez impede atribuir a causa de uma diferença.

---

# 10. Diagnóstico de problemas comuns

## O kernel não inicia

Confirme compatibilidade entre ISA, plataforma, kernel e imagem. Um kernel x86 deve ser usado com `build/X86/gem5.opt` e configuração x86. Consulte `system.terminal`, `simout` e `simerr`.

## O programa não é encontrado no convidado

No console do guest, verifique:

```sh
ls -l /opt/gem5
file /opt/gem5/conta_primos
```

Se os arquivos não existem, a cópia para a imagem não foi persistida, a imagem errada foi passada ao gem5 ou a partição montada não era a raiz usada no boot.

## `Exec format error`

O binário foi compilado para a ISA/ABI errada. Verifique `file conta_primos` no host e `file /opt/gem5/conta_primos` no guest.

## `m5: not found`

A imagem não contém o utilitário de pseudo-instruções no `PATH`. Localize-o com `find / -name m5 2>/dev/null` e use o caminho encontrado, ou instale/compile o utilitário na imagem de trabalho.

## A simulação não encerra

Garanta que o script chega a `m5 exit`. Se o programa falhar antes disso, veja o console serial e acrescente `set -x` ao script para depuração. Durante desenvolvimento, é aceitável encerrar manualmente; para medições reproduzíveis, a saída deve ser programática.

## `stats.txt` inclui o boot

Verifique se `m5 resetstats` foi executado antes do programa e selecione o bloco delimitado por `dumpstats`. Veja o console serial para confirmar a ordem dos comandos.

---

# 11. Checklist de reprodutibilidade

Antes de comparar resultados, registre:

- hash ou versão do gem5;
- binário usado (`gem5.opt` ou `gem5.debug`);
- ISA, modelo de CPU, frequência e número de núcleos;
- tamanhos/latências das caches e modelo/tamanho de memória;
- versão/origem do kernel e da imagem de disco;
- compilador, versão e flags do programa;
- limite usado pelo programa;
- conteúdo do script de boot;
- bloco específico de `stats.txt` analisado.

Arquive `config.ini`, `config.json`, `stats.txt`, `system.terminal`, o fonte C e o script Python junto com a tabela de resultados.

---

# Conclusão

No modo FS, o programa é executado dentro de um Linux convidado e, por isso, a configuração envolve boot, kernel e imagem de disco além do modelo de hardware. A preparação demanda mais trabalho que SE, mas permite analisar efeitos reais do sistema operacional e da plataforma.

Para medir corretamente o programa de busca de primos, use `m5 resetstats` imediatamente antes da execução e `m5 dumpstats` logo após. Em seguida, interprete o bloco correspondente de `stats.txt`, valide a saída do programa em `system.terminal` e compare apenas experimentos com condições controladas.