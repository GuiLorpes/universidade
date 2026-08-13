# Tutorial GEM5: Download, Escolha de Arquitetura e Build

## Introdução

O **gem5** é um simulador modular de arquitetura de computadores utilizado para estudar processadores, memória, dispositivos e sistemas completos. Ele permite executar cargas de trabalho simuladas e coletar métricas como ciclos, instruções executadas, IPC e acessos à memória.

Um build do gem5 é produzido para uma **ISA** (*Instruction Set Architecture*, ou arquitetura do conjunto de instruções). A ISA define, entre outros aspectos, as instruções de máquina, registradores e o modo de execução que serão simulados. Portanto, a arquitetura escolhida deve ser compatível com o sistema operacional, a imagem de disco e os programas usados no experimento.

## Objetivo

Ao final deste tutorial, você será capaz de baixar o código-fonte do gem5, identificar as arquiteturas disponíveis, escolher a arquitetura adequada ao seu experimento e compilar um executável funcional do simulador.

> **Ambiente adotado:** Ubuntu ou outra distribuição Linux baseada em Debian. Adapte os comandos de instalação de pacotes caso use outra distribuição.

---

## Arquiteturas presentes no gem5

As principais ISAs disponíveis no gem5 são:

| Arquitetura | Diretório/Alvo de build | Quando escolher |
|---|---|---|
| **X86** | `build/X86/` | Para simular PCs e servidores compatíveis com Intel/AMD, normalmente com Linux x86-64. |
| **ARM** | `build/ARM/` | Para sistemas embarcados, dispositivos móveis, servidores ARM e plataformas como Armv8/AArch64. |
| **RISCV** | `build/RISCV/` | Para pesquisas, ensino e experimentos baseados em RISC-V, incluindo Linux RISC-V. |
| **MIPS** | `build/MIPS/` | Para estudos e cargas de trabalho legadas baseadas em MIPS. |
| **POWER** | `build/POWER/` | Para estudos de sistemas e software que utilizam a ISA Power/PowerPC. |
| **SPARC** | `build/SPARC/` | Para experimentos legados ligados à arquitetura SPARC. |
| **NULL** | `build/NULL/` | Para testes de infraestrutura e desenvolvimento do gem5 sem uma ISA completa. Não é a escolha usual para executar aplicações reais. |

> A disponibilidade concreta de configurações, imagens de disco e exemplos pode variar conforme a revisão do gem5. X86, ARM e RISCV são as escolhas mais comuns em novos experimentos.

### Como escolher a arquitetura

Use esta regra principal: **compile a ISA para a qual sua carga de trabalho foi construída**.

1. Se você possui um binário, uma imagem Linux ou uma aplicação compilada para **x86-64**, escolha **X86**.
2. Se a carga de trabalho usa **AArch64/ARM64**, ou se o objetivo é estudar plataformas ARM, escolha **ARM**.
3. Se o binário e a imagem do sistema são para **RISC-V**, escolha **RISCV**.
4. Escolha **MIPS**, **POWER** ou **SPARC** apenas quando sua pesquisa ou carga de trabalho exigir especificamente essas ISAs.
5. Não escolha a ISA com base no computador que hospeda o gem5. Por exemplo, é possível compilar e executar `build/RISCV/gem5.opt` em um computador hospedeiro x86-64; o que importa é a arquitetura **simulada**.

Para experimentos iniciais sem uma carga de trabalho previamente definida, recomenda-se:

- **X86**, se o objetivo for explorar cenários semelhantes a PCs e servidores convencionais;
- **ARM**, se o foco for sistemas embarcados, dispositivos móveis ou servidores ARM;
- **RISCV**, se o objetivo for aprendizagem, extensão da ISA ou pesquisa aberta em arquitetura de computadores.

---

## Pré-requisitos

Abra um terminal e instale as ferramentas de compilação e dependências mais comuns:

```bash
sudo apt update
sudo apt install -y \
  build-essential \
  git \
  python3 \
  python3-dev \
  python3-venv \
  scons \
  pkg-config \
  zlib1g-dev \
  libprotobuf-dev \
  protobuf-compiler \
  libhdf5-dev \
  libgoogle-perftools-dev \
  libboost-all-dev \
  libsqlite3-dev \
  m4
```

Verifique as ferramentas principais:

```bash
git --version
python3 --version
scons --version
g++ --version
```

---

# Prática: download e compilação

## Etapa 1 — Escolher um diretório de trabalho

Crie um diretório para seus projetos e entre nele:

```bash
mkdir -p ~/projetos
cd ~/projetos
```

Você pode usar outro local, desde que tenha permissão de escrita e espaço livre em disco.

## Etapa 2 — Baixar o código-fonte do gem5

Clone o repositório oficial:

```bash
git clone https://github.com/gem5/gem5.git
cd gem5
```

Confirme o estado e registre a revisão do código que será usada nos experimentos:

```bash
git status
git branch --show-current
git log -1 --oneline
```

> Registre o *commit* no relatório. Diferentes revisões do gem5 podem alterar opções, modelos e resultados.

## Etapa 3 — Opcional: selecionar uma versão estável

Por padrão, o clone usa a linha principal de desenvolvimento. Para listar etiquetas de versão:

```bash
git tag --list | tail
```

Para selecionar uma etiqueta específica, substitua `<tag>` pelo nome desejado:

```bash
git checkout <tag>
```

## Etapa 4 — Criar um ambiente Python isolado

Crie e ative um ambiente virtual Python:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Se o repositório possuir `requirements.txt`, instale as dependências declaradas:

```bash
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi
```

Para sair do ambiente virtual ao terminar:

```bash
deactivate
```

## Etapa 5 — Definir a arquitetura simulada

Escolha **uma** arquitetura de acordo com sua carga de trabalho. Nos comandos seguintes, `ISA` deve ser substituída por `X86`, `ARM`, `RISCV`, `MIPS`, `POWER`, `SPARC` ou `NULL`.

Exemplos de correspondência:

```text
Binário Linux x86-64             -> X86
Binário Linux AArch64/ARM64      -> ARM
Binário Linux RISC-V             -> RISCV
```

Se você ainda não possui uma carga de trabalho e deseja um caminho inicial típico, use X86:

```bash
export ISA=X86
```

Para um experimento com RISC-V, por exemplo:

```bash
export ISA=RISCV
```

Confira o valor escolhido:

```bash
echo "$ISA"
```

## Etapa 6 — Compilar o gem5

Compile a variante `opt`, recomendada para a maior parte dos experimentos:

```bash
scons build/$ISA/gem5.opt -j"$(nproc)"
```

Por exemplo, para X86, o comando efetivo será:

```bash
scons build/X86/gem5.opt -j"$(nproc)"
```

Para ARM:

```bash
scons build/ARM/gem5.opt -j"$(nproc)"
```

Para RISC-V:

```bash
scons build/RISCV/gem5.opt -j"$(nproc)"
```

Significado dos componentes do comando:

- `build/$ISA/`: diretório de saída associado à ISA simulada;
- `gem5.opt`: executável otimizado, com verificações úteis para experimentos;
- `-j"$(nproc)"`: usa os núcleos lógicos disponíveis para acelerar o build.

A primeira compilação pode levar vários minutos. Se ocorrer falta de memória, reduza o paralelismo, por exemplo:

```bash
scons build/$ISA/gem5.opt -j2
```

## Etapa 7 — Validar o executável

Verifique se o arquivo foi criado:

```bash
ls -lh build/$ISA/gem5.opt
```

Exiba parte da ajuda e a versão do simulador:

```bash
build/$ISA/gem5.opt --help | head -n 20
build/$ISA/gem5.opt --version
```

Se esses comandos exibirem informações do gem5 sem erros, o build foi concluído com sucesso.

---

## Variantes de compilação

Além de `opt`, o gem5 oferece outras variantes. Substitua `ISA` pela arquitetura escolhida:

| Variante | Comando | Uso recomendado |
|---|---|---|
| `opt` | `scons build/$ISA/gem5.opt -j"$(nproc)"` | Experimentos e uso geral. |
| `debug` | `scons build/$ISA/gem5.debug -j"$(nproc)"` | Depuração detalhada; execução mais lenta. |
| `fast` | `scons build/$ISA/gem5.fast -j"$(nproc)"` | Execução mais rápida, com menos verificações. |

Para este tutorial, use preferencialmente `gem5.opt`.

---

## Problemas frequentes

### `scons: command not found`

Instale o SCons:

```bash
sudo apt install scons
```

### Erro relacionado ao compilador C++

Instale as ferramentas de compilação:

```bash
sudo apt install build-essential g++
```

### Erro de memória durante o build

Diminua o número de tarefas simultâneas:

```bash
scons build/$ISA/gem5.opt -j2
```

### Arquitetura incompatível com a carga de trabalho

Se o simulador não consegue iniciar um binário ou imagem, confirme a ISA com que esse artefato foi compilado. Recompile o gem5 para a ISA correspondente; um binário x86-64 não deve ser usado em uma simulação RISCV ou ARM, por exemplo.

---

## Resultado esperado

Ao final, a estrutura deverá conter um executável para a arquitetura escolhida. Para uma escolha X86, por exemplo:

```text
gem5/
├── build/
│   └── X86/
│       └── gem5.opt
├── configs/
├── src/
└── tests/
```

O próximo passo é selecionar uma configuração compatível com a ISA escolhida, executar uma carga de trabalho e analisar os arquivos gerados, especialmente `stats.txt` e `config.ini`.