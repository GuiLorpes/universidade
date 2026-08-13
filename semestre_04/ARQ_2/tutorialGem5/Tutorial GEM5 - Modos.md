# Tutorial gem5: modos de execução, linha de comando e API Python

## Introdução

O **gem5** é um simulador de arquitetura de computadores. Antes de executar um experimento, é necessário tomar duas decisões independentes:

1. qual **ISA** será simulada, como X86, ARM ou RISCV;
2. qual **modo de execução** será usado: *System-call Emulation* (SE) ou *Full System* (FS).

A ISA deve ser compatível com a carga de trabalho. Um binário x86-64 requer um build `X86`; um binário AArch64, `ARM`; e um binário RISC-V, `RISCV`. O computador hospedeiro não precisa ter a mesma arquitetura simulada.

## Objetivo

Ao final, você saberá distinguir os modos SE e FS, iniciar simulações pela linha de comando e criar uma simulação simples usando a API Python (biblioteca padrão) do gem5.

> **Pré-requisito:** tenha o gem5 compilado, preferencialmente como `build/<ISA>/gem5.opt`. Para os exemplos em SE, será usada a ISA X86.

---

## 1. Modos de execução

### 1.1 System-call Emulation (SE)

No modo **SE**, o gem5 simula o processador, a memória e os componentes definidos na configuração, mas **não inicializa um sistema operacional completo**. A aplicação é carregada diretamente; chamadas de sistema feitas pelo programa são atendidas por uma camada de emulação do gem5.

Use SE quando o foco for uma aplicação de espaço de usuário e métricas de arquitetura, como ciclos, instruções, IPC, cache e memória.

**Vantagens**

- configuração e inicialização mais simples;
- normalmente mais rápido que FS;
- não exige kernel nem imagem de disco;
- adequado para microbenchmarks e programas compilados estaticamente.

**Limitações**

- não simula a inicialização de um sistema operacional;
- suporte a chamadas de sistema e a comportamentos dependentes do SO pode ser incompleto;
- não é apropriado para estudar escalonador, drivers, interrupções ou boot.

### 1.2 Full System (FS)

No modo **FS**, o gem5 simula uma plataforma completa: processador, memória, dispositivos, firmware quando necessário, kernel e sistema operacional convidado. O sistema simulado faz o boot e executa a carga de trabalho como em uma máquina real.

Use FS quando o experimento envolver o kernel, sistema operacional, dispositivos, virtualização, inicialização do sistema ou interações completas entre software e hardware.

**Vantagens**

- maior fidelidade ao funcionamento de uma máquina completa;
- permite executar um kernel e uma imagem de disco reais para a ISA simulada;
- adequado para estudos de SO, drivers e workloads complexos.

**Limitações**

- requer mais artefatos: configuração de plataforma, kernel, imagem de disco e, em alguns casos, firmware;
- é mais demorado e consome mais recursos;
- a configuração é mais sensível à compatibilidade entre ISA, placa, kernel e disco.

### 1.3 Como escolher entre SE e FS

| Necessidade do experimento | Modo recomendado |
|---|---|
| Executar um programa simples e medir IPC, ciclos ou caches | **SE** |
| Validar um binário de usuário para uma ISA | **SE** |
| Estudar boot, kernel, escalonamento ou drivers | **FS** |
| Executar Linux convidado e aplicações que dependem do SO completo | **FS** |
| Fazer um primeiro experimento no gem5 | **SE** |

> Comece com **SE** sempre que ele responder à pergunta de pesquisa. Migre para **FS** apenas quando o sistema operacional completo for parte do fenômeno que deseja observar.

---

# Prática

## Etapa 1 — Preparar o ambiente

No diretório raiz do repositório, defina a ISA e o executável. Para este tutorial:

```bash
cd ~/projetos/gem5
export ISA=X86
export GEM5=build/$ISA/gem5.opt
```

Verifique o build:

```bash
$GEM5 --version
```

Se o executável ainda não existir, compile-o:

```bash
scons build/$ISA/gem5.opt -j"$(nproc)"
```

## Etapa 2 — Entender a execução pela linha de comando

A forma geral de invocar o simulador é:

```bash
build/<ISA>/gem5.opt [opções-do-gem5] script_de_configuração.py [opções-do-script]
```

Há duas camadas de argumentos:

- opções **antes** do script são interpretadas pelo gem5, por exemplo `--outdir`;
- opções **depois** do script pertencem ao próprio script de configuração.

Defina um diretório de saída para cada execução. Isso evita sobrescrever resultados anteriores:

```bash
mkdir -p resultados/se-basico
```

Os arquivos mais importantes gerados ao final são normalmente:

- `stats.txt`: estatísticas, como `simTicks`, instruções e IPC;
- `config.ini`: configuração final em formato legível;
- `config.json`: configuração final em JSON.

## Etapa 3 — Executar uma simulação SE pela linha de comando

O repositório inclui scripts legados de exemplo, entre eles `configs/example/se.py`. Execute um binário **compatível com a ISA simulada**:

```bash
$GEM5 --outdir=resultados/se-basico \
  configs/example/se.py \
  --cmd=/caminho/para/programa-x86
```

Para X86, `/caminho/para/programa-x86` deve apontar para um executável x86 compatível. Para simulações mais simples, programas compilados estaticamente tendem a exigir menos dependências de bibliotecas no ambiente simulado.

Argumentos para o programa podem ser fornecidos com `--options`:

```bash
$GEM5 --outdir=resultados/se-com-args \
  configs/example/se.py \
  --cmd=/caminho/para/programa-x86 \
  --options="--tamanho 1000"
```

Para listar as opções disponíveis no script instalado na sua revisão do gem5:

```bash
$GEM5 configs/example/se.py --help
```

> Scripts em `configs/example` são exemplos legados úteis para exploração. Para experimentos novos e reprodutíveis, prefira manter um script Python próprio, versionado junto com o experimento.

## Etapa 4 — Executar um experimento FS pela linha de comando

Uma execução FS usa o mesmo padrão de comando, mas o script precisa configurar uma placa compatível e informar recursos para o sistema convidado, tais como kernel e imagem de disco:

```bash
$GEM5 --outdir=resultados/fs \
  caminho/para/full_system.py \
  --kernel caminho/para/vmlinux \
  --disk-image caminho/para/disco.img
```

Os nomes exatos das opções dependem do script `full_system.py`. Consulte sempre a ajuda dele:

```bash
$GEM5 caminho/para/full_system.py --help
```

Em FS, mantenha todos os artefatos coerentes: um build `X86` deve receber uma plataforma X86, kernel X86 e imagem de disco X86; um build `RISCV` exige os equivalentes RISC-V.

O boot pode levar bastante tempo em simulação. Para automatizar uma ação no sistema convidado, configurações FS podem fornecer comandos de *readfile* ou mecanismos específicos da placa e da imagem utilizada.

---

## Etapa 5 — Criar uma configuração SE com a API Python

O gem5 usa Python para descrever sistemas simulados. A **biblioteca padrão do gem5** oferece componentes de alto nível para montar placas, processadores, memória, hierarquias de cache e workloads de forma mais clara do que alterar scripts genéricos.

Crie o arquivo `se_api.py` na raiz do repositório:

```python
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires

# Esta configuração foi escrita para o executável build/X86/gem5.opt.
requires(isa_required=ISA.X86)

processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING,
    isa=ISA.X86,
    num_cores=1,
)

board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=SingleChannelDDR3_1600(size="1GiB"),
    cache_hierarchy=NoCache(),
)

# Recurso de exemplo disponibilizado pelo sistema de recursos do gem5.
binary = obtain_resource("x86-hello64-static")
board.set_se_binary_workload(binary)

simulator = Simulator(board=board)
simulator.run()
```

Essa configuração cria um sistema SE de um núcleo, CPU de temporização, 1 GiB de DDR3 e sem caches. A ausência de cache é intencional para manter o primeiro exemplo pequeno; ela não representa uma configuração realista de processador.

Execute o script:

```bash
mkdir -p resultados/se-api
$GEM5 --outdir=resultados/se-api se_api.py
```

Na primeira execução, o gem5 pode baixar o recurso declarado por `obtain_resource`. Se o ambiente não tiver acesso à internet, obtenha previamente os recursos necessários ou adapte o script para usar um binário local compatível.

## Etapa 6 — Usar um binário local na API Python

Para definir explicitamente o executável e seus argumentos, substitua as três linhas que definem `binary` e o workload por:

```python
from gem5.components.boards.se_binary_workload import SEBinaryWorkload
from gem5.resources.resource import BinaryResource

board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=SingleChannelDDR3_1600(size="1GiB"),
    cache_hierarchy=NoCache(),
)
board.set_se_binary_workload(
    BinaryResource(local_path="/caminho/para/programa-x86"),
    arguments=["--tamanho", "1000"],
)
```

O caminho deve indicar um binário para a mesma ISA declarada em `isa=ISA.X86`. Caso use outra ISA, altere **o build**, o valor de `ISA`, o binário e, quando necessário, o tipo de placa e os recursos selecionados.

## Etapa 7 — Interpretar o resultado inicial

Abra as estatísticas produzidas pela execução:

```bash
grep -E "^(simTicks|simInsts|hostSeconds|system\.cpu\.ipc)" \
  resultados/se-api/stats.txt
```

Os nomes podem mudar conforme o modelo de CPU e a configuração. Uma leitura inicial é:

- `simTicks`: tempo simulado em *ticks*;
- `simInsts`: número de instruções simuladas, quando disponível;
- `system.cpu.ipc`: instruções por ciclo, quando exposta pelo modelo;
- `hostSeconds`: tempo de execução no computador hospedeiro.

Não compare resultados de configurações diferentes apenas pelo tempo de parede (`hostSeconds`). Para análise arquitetural, registre a configuração, a revisão do gem5, a ISA, a carga de trabalho, o modelo de CPU e as métricas simuladas em `stats.txt`.

---

## Problemas frequentes

### O binário não executa em SE

Confirme se o binário pertence à ISA do build. Um programa x86 não pode executar em `build/ARM/gem5.opt`. Verifique também se ele depende de bibliotecas dinâmicas ausentes; nesse caso, use um binário estático ou um ambiente FS apropriado.

### O script não reconhece uma opção

Execute `--help` **depois** do nome do script, pois a opção é dele:

```bash
$GEM5 caminho/para/script.py --help
```

### O resultado foi sobrescrito

Use sempre um novo valor para `--outdir` em cada execução. Assim, cada experimento preserva seu próprio `stats.txt` e sua própria configuração.

## Próximos passos

Depois de validar uma execução SE simples, adicione uma hierarquia de cache, altere o tipo de CPU e compare as estatísticas em diretórios de saída distintos. Quando a pergunta de pesquisa envolver o sistema operacional ou dispositivos, construa uma configuração FS compatível com a mesma ISA.