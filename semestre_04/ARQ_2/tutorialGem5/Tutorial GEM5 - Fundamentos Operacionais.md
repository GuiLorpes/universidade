# Tutorial GEM5 — Fundamentos Operacionais

## Introdução

O gem5 é um simulador modular de arquitetura de computadores. Antes de comparar caches, processadores, redes ou protocolos de coerência, é necessário dominar seu ciclo operacional: selecionar o binário correto, descrever um sistema em Python, iniciar a simulação, localizar os resultados e interpretar as mensagens produzidas.

Este tutorial apresenta uma primeira execução completa em **modo System Emulation (SE)**. O experimento usa um programa de **histograma de caracteres**, evitando exemplos de soma de vetores, multiplicação de matrizes e busca de primos. Ao final, você terá uma base prática para executar os demais tutoriais da coleção.

## Objetivos

Ao concluir, você deverá ser capaz de:

- distinguir o binário do gem5 do script de configuração;
- identificar os componentes mínimos de uma simulação em SE;
- executar um programa de usuário no simulador;
- controlar o diretório de saída e localizar `config.ini`, `config.json` e `stats.txt`;
- reconhecer avisos comuns sem confundi-los com falhas;
- interpretar métricas iniciais de tempo simulado, instruções, ciclos e IPC;
- modificar parâmetros básicos por linha de comando e por API Python.

## Pré-requisitos

- Linux ou ambiente compatível com shell POSIX;
- gem5 compilado para a ISA escolhida; neste tutorial será utilizado `build/X86/gem5.opt`;
- compilador C, como GCC;
- conhecimentos elementares de terminal, C e Python.

> Os caminhos e os nomes de alguns parâmetros podem variar entre versões do gem5. Sempre confirme a interface local com `--help` e consulte `config.ini` após a execução.

## Conceitos fundamentais

### Binário, ISA e arquivo de configuração

O comando do gem5 tem duas partes principais:

```text
<binário-do-gem5> <script-de-configuração.py> <opções-do-script>
```

Por exemplo:

```bash
build/X86/gem5.opt configs/example/se.py --cmd=./histograma
```

- `build/X86/gem5.opt` é o **executável do simulador**, compilado com suporte à ISA x86.
- `configs/example/se.py` é um **script Python** que constrói uma plataforma simulada.
- `--cmd=./histograma` é uma opção consumida pelo script de configuração, que informa qual programa será executado pelo sistema simulado.

A ISA do binário precisa ser compatível com o executável do workload. Para usar um programa ARM, por exemplo, use um binário gem5 ARM e um programa compilado para ARM.

### Modos de execução

O gem5 é frequentemente usado em dois modos:

- **SE (System Emulation):** emula processos de usuário e as chamadas de sistema mais relevantes. É rápido para experimentos de microarquitetura e não exige imagem de disco ou kernel convidado.
- **FS (Full System):** simula uma máquina completa, incluindo kernel, dispositivos e sistema operacional convidado. É indicado quando o comportamento do SO e dos dispositivos importa.

Usaremos SE porque ele reduz a complexidade operacional inicial. Isso não significa que os resultados representem todo o comportamento de um sistema operacional real.

### Tempo do hospedeiro e tempo simulado

Há duas noções de tempo:

- **tempo do hospedeiro:** tempo real gasto pelo computador que executa o gem5;
- **tempo simulado:** tempo que transcorre na plataforma modelada.

Uma simulação pode levar minutos no hospedeiro para representar poucos milissegundos de tempo simulado. Métricas como `simSeconds` e `simTicks` descrevem o sistema modelado; não são o tempo de relógio do seu computador.

### Objetos SimObject e conexões

Internamente, CPUs, caches, barramentos, memórias e controladores são objetos chamados **SimObjects**. Um script Python cria esses objetos, define parâmetros e conecta portas. A plataforma não existe até que o script faça algo conceitualmente semelhante a:

```python
system.cpu.icache_port = system.l1i.cpu_side
system.l1i.mem_side = system.membus.cpu_side_ports
```

Ou seja: uma porta do processador é conectada ao lado da CPU de um cache; o lado de memória desse cache é conectado ao barramento de memória.

## Organização sugerida do experimento

Crie um diretório de trabalho fora da árvore de resultados padrão:

```bash
mkdir -p ~/gem5-labs/fundamentos
cd ~/gem5-labs/fundamentos
```

Defina, se desejar, o caminho da árvore-fonte do gem5:

```bash
export GEM5_ROOT="$HOME/gem5"
```

Nos comandos seguintes, substitua `"$GEM5_ROOT"` pelo diretório real caso tenha escolhido outro local.

## Etapa 1 — Verificar a instalação

Confira se o binário existe e obtenha ajuda básica:

```bash
ls "$GEM5_ROOT/build/X86/gem5.opt"
"$GEM5_ROOT/build/X86/gem5.opt" --help | head -n 25
```

Use `gem5.debug` apenas quando precisar investigar um problema específico. Ele contém verificações adicionais e costuma ser mais lento. Para campanhas de experimentos, `gem5.opt` é normalmente a melhor escolha.

Verifique também as opções do script SE disponível na sua versão:

```bash
"$GEM5_ROOT/build/X86/gem5.opt" \
  "$GEM5_ROOT/configs/example/se.py" --help | less
```

Procure opções como `--cmd`, `--options`, `--cpu-type`, `--cpu-clock`, `--caches`, `--l1d_size`, `--l1i_size`, `--l2cache` e `--mem-size`.

## Etapa 2 — Criar o workload

Crie o arquivo `histograma.c`:

```c
#include <stdio.h>
#include <string.h>

#define TAM 8192

int main(void)
{
    char dados[TAM];
    unsigned int freq[26] = {0};
    unsigned long checksum = 0;

    for (int i = 0; i < TAM - 1; i++) {
        dados[i] = 'a' + ((i * 17 + 3) % 26);
    }
    dados[TAM - 1] = '\0';

    for (int repeticao = 0; repeticao < 2000; repeticao++) {
        for (int i = 0; dados[i] != '\0'; i++) {
            unsigned int indice = (unsigned int)(dados[i] - 'a');
            freq[indice]++;
            checksum += (freq[indice] ^ (unsigned int)i);
        }
    }

    printf("checksum=%lu\n", checksum);
    printf("freq[a]=%u freq[z]=%u\n", freq[0], freq[25]);
    return 0;
}
```

Compile para x86-64:

```bash
gcc -O2 -Wall -Wextra -o histograma histograma.c
file histograma
./histograma
```

O último comando executa o programa no hospedeiro e serve como verificação funcional. O texto e os valores exatos podem mudar com alterações no código, mas o programa deve terminar com código de saída zero.

> Em SE, executáveis estáticos simplificam a portabilidade, pois reduzem a dependência de bibliotecas do sistema emulado. Caso a sua configuração suporte compilação estática, experimente `gcc -O2 -static -o histograma histograma.c`. Algumas distribuições não possuem bibliotecas estáticas instaladas; nesse caso, use o executável dinâmico normalmente ou instale o pacote apropriado.

## Etapa 3 — Executar uma configuração inicial

Execute o script pronto em modo SE, escolhendo uma CPU simples e caches privados L1:

```bash
"$GEM5_ROOT/build/X86/gem5.opt" \
  --outdir=saida-baseline \
  "$GEM5_ROOT/configs/example/se.py" \
  --cmd=./histograma \
  --cpu-type=TimingSimpleCPU \
  --cpu-clock=2GHz \
  --caches \
  --l1i_size=32KiB \
  --l1d_size=32KiB \
  --mem-size=512MiB
```

A opção `--outdir=saida-baseline` evita misturar resultados de execuções diferentes. Não reutilize o mesmo diretório para experimentos distintos sem limpá-lo conscientemente.

Durante a execução, mensagens informativas e avisos podem aparecer. O encerramento esperado normalmente inclui uma mensagem conceitualmente equivalente a:

```text
Exiting @ tick ... because exiting with last active thread context
```

Isso indica que o processo simulado encerrou. Se houver uma mensagem de `fatal`, a execução falhou e os resultados não devem ser comparados com uma campanha válida.

## Etapa 4 — Inspecionar os arquivos gerados

Liste o diretório de saída:

```bash
find saida-baseline -maxdepth 1 -type f -printf '%f\n' | sort
```

Os arquivos mais importantes são:

| Arquivo | Função |
|---|---|
| `config.ini` | configuração resolvida, em formato legível por seções |
| `config.json` | configuração resolvida em formato estruturado |
| `stats.txt` | contadores e estatísticas da execução |
| `simout` | saída padrão do programa simulado |
| `simerr` | saída de erro do programa simulado |

Confirme a saída do workload:

```bash
cat saida-baseline/simout
cat saida-baseline/simerr
```

Verifique a CPU e os caches realmente instanciados. Não presuma que uma opção foi aplicada apenas porque o comando a contém:

```bash
grep -nE '^\[system.cpu|^\[system.cpu.icache|^\[system.cpu.dcache|^clock' saida-baseline/config.ini
```

A fonte de verdade de um experimento é a configuração registrada na saída, não somente o comando digitado.

## Etapa 5 — Ler estatísticas essenciais

Extraia métricas iniciais:

```bash
grep -E '^(simSeconds|simTicks|simInsts|simOps|hostSeconds|hostInstRate|system\.cpu\.(numCycles|ipc|cpi))' \
  saida-baseline/stats.txt
```

Os nomes podem variar levemente entre modelos e versões. Interprete-os assim:

- `simTicks`: duração simulada em *ticks*;
- `simSeconds`: duração simulada em segundos;
- `simInsts`: instruções simuladas, quando o modelo fornece esse contador;
- `system.cpu.numCycles`: ciclos da CPU simulada;
- `system.cpu.ipc`: instruções por ciclo;
- `system.cpu.cpi`: ciclos por instrução;
- `hostSeconds`: custo da simulação no computador hospedeiro.

Para uma CPU com frequência fixa, uma relação útil de validação é:

\[
\text{tempo simulado} \approx \frac{\text{ciclos simulados}}{\text{frequência da CPU}}
\]

E, para os contadores medidos sobre intervalos compatíveis:

\[
IPC = \frac{\text{instruções}}{\text{ciclos}}, \qquad CPI = \frac{\text{ciclos}}{\text{instruções}}
\]

Em geral, quando ambos são calculados a partir do mesmo conjunto de instruções, vale aproximadamente \(CPI \approx 1/IPC\). Estatísticas de inicialização, drenagem ou diferentes domínios de contagem podem causar pequenas diferenças.

Para caches, procure por acessos, faltas e taxa de faltas:

```bash
grep -E 'system\.cpu\.(icache|dcache).*\.(overallAccesses|overallMisses|overallMissRate)' \
  saida-baseline/stats.txt
```

Uma taxa de faltas é definida por:

\[
\text{miss rate} = \frac{\text{número de faltas}}{\text{número de acessos}}
\]

Nunca compare apenas o valor absoluto de faltas entre workloads com números muito diferentes de acessos. Use taxas, contexto do programa e métricas de desempenho em conjunto.

## Etapa 6 — Comparar dois modelos simples de CPU

Repita o experimento com `AtomicSimpleCPU`:

```bash
"$GEM5_ROOT/build/X86/gem5.opt" \
  --outdir=saida-atomic \
  "$GEM5_ROOT/configs/example/se.py" \
  --cmd=./histograma \
  --cpu-type=AtomicSimpleCPU \
  --cpu-clock=2GHz \
  --caches \
  --l1i_size=32KiB \
  --l1d_size=32KiB \
  --mem-size=512MiB
```

Monte uma tabela mínima:

```bash
for diretorio in saida-baseline saida-atomic; do
  echo "=== $diretorio ==="
  grep -E '^(simSeconds|hostSeconds|system\.cpu\.(numCycles|ipc|cpi))' "$diretorio/stats.txt"
done
```

`AtomicSimpleCPU` faz acessos de memória de forma atômica e é útil para execução funcional e rápida. `TimingSimpleCPU` modela temporização de modo mais detalhado. Portanto, não trate o resultado da CPU atômica como uma estimativa detalhada de desempenho de memória; ela é uma referência operacional, não uma substituta para um modelo temporal.

## Etapa 7 — Criar uma configuração mínima pela API Python

Scripts prontos aceleram os primeiros testes, mas a API Python oferece controle explícito. Crie `fundamentos_se.py`:

```python
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy,
)
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator

cache_hierarchy = PrivateL1PrivateL2CacheHierarchy(
    l1d_size="32KiB",
    l1i_size="32KiB",
    l2_size="256KiB",
)

memory = SingleChannelDDR3_1600(size="512MiB")
processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING,
    isa=ISA.X86,
    num_cores=1,
)

board = SimpleBoard(
    clk_freq="2GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

board.set_se_binary_workload(BinaryResource("./histograma"))

simulator = Simulator(board=board)
simulator.run()

print("Causa de saída:", simulator.get_last_exit_event_cause())
```

Execute-o:

```bash
"$GEM5_ROOT/build/X86/gem5.opt" \
  --outdir=saida-python \
  fundamentos_se.py
```

Esse exemplo utiliza a biblioteca padrão de componentes do gem5. Em versões antigas, os módulos podem ter nomes diferentes; nesse caso, use o estilo de configuração clássico compatível com a árvore-fonte instalada ou atualize o gem5. A ideia central permanece: instanciar processador, memória, caches e placa, associar um workload e iniciar `Simulator.run()`.

Inspecione a configuração e as estatísticas exatamente como na execução anterior:

```bash
head -n 30 saida-python/config.ini
grep -E '^(simSeconds|simInsts|system\.processor|system\.board)' saida-python/stats.txt | head -n 30
```

Os caminhos das estatísticas variam conforme a hierarquia de objetos criada pela API. Use buscas amplas antes de fixar scripts de coleta.

## Etapa 8 — Alterar uma hipótese por vez

Faça uma pequena campanha variando somente o tamanho da L1 de dados. Com o script `se.py`:

```bash
for tamanho in 8KiB 32KiB 128KiB; do
  nome="saida-l1d-${tamanho}"
  "$GEM5_ROOT/build/X86/gem5.opt" \
    --outdir="$nome" \
    "$GEM5_ROOT/configs/example/se.py" \
    --cmd=./histograma \
    --cpu-type=TimingSimpleCPU \
    --cpu-clock=2GHz \
    --caches \
    --l1i_size=32KiB \
    --l1d_size="$tamanho" \
    --mem-size=512MiB
done
```

Colete os resultados:

```bash
for diretorio in saida-l1d-*; do
  echo "=== $diretorio ==="
  grep -E '^(simSeconds|system\.cpu\.(numCycles|ipc))' "$diretorio/stats.txt"
  grep -E 'system\.cpu\.dcache.*overallMissRate' "$diretorio/stats.txt"
done
```

Mantenha constantes o binário do workload, a frequência, o modelo de CPU, a memória e as demais caches. Se vários fatores mudarem ao mesmo tempo, não será possível atribuir a causa de uma diferença observada.

## Boas práticas experimentais

1. **Registre o comando completo**, a revisão do gem5 e o compilador do workload.
2. **Use um diretório de saída exclusivo por configuração**.
3. **Valide funcionalmente o programa** observando `simout` e o motivo de saída.
4. **Confirme parâmetros em `config.ini`**, sobretudo em campanhas automatizadas.
5. **Aqueça e delimite regiões de interesse** em estudos avançados; inicialização pode distorcer métricas de programas curtos.
6. **Não compare `hostSeconds` como desempenho da arquitetura simulada**; ele mede o custo da ferramenta no hospedeiro.
7. **Mude uma variável independente por experimento**, salvo quando estiver usando um planejamento fatorial explícito.
8. **Guarde resultados brutos**. Tabelas derivadas não substituem `stats.txt` e `config.ini`.

## Problemas frequentes

### `fatal: ...` ao iniciar

Verifique se o binário do gem5 corresponde à ISA e se o script recebeu todos os parâmetros necessários. Leia as linhas imediatamente anteriores ao erro: elas geralmente identificam o objeto ou a conexão ausente.

### O programa não é encontrado

O caminho em `--cmd` ou em `BinaryResource` é resolvido a partir do diretório em que o gem5 foi iniciado. Use caminho absoluto para eliminar ambiguidade:

```bash
--cmd="$PWD/histograma"
```

### O programa termina, mas `simout` está vazio

Algumas saídas podem ser afetadas por *buffering*, falha do programa ou configuração do workload. Execute o binário no hospedeiro, verifique `simerr` e confirme o motivo de saída no log do gem5.

### Não encontro uma estatística mencionada

Nomes e hierarquias mudam com o modelo de CPU, a configuração e a versão. Faça uma busca aproximada:

```bash
grep -iE 'cache|miss|ipc|cycle|inst' saida-baseline/stats.txt | head -n 80
```

Depois adapte o coletor à nomenclatura efetivamente produzida.

### Há avisos sobre componentes não configurados

Nem todo aviso invalida a simulação. Porém, avisos sobre memória, portas desconectadas, ISA incompatível ou valores padrão inesperados devem ser investigados antes de aceitar resultados. Diferencie claramente `warn` de `fatal`, mas não ignore avisos sem entendê-los.

## Exercícios

1. Compile o workload com `-O0`, `-O2` e `-O3`. Compare instruções simuladas, ciclos e IPC. Explique por que o compilador altera o perfil microarquitetural.
2. Varie `--cpu-clock` entre `1GHz`, `2GHz` e `4GHz`. Quais métricas em segundos e em ciclos devem mudar? Quais deveriam permanecer próximas para a mesma configuração lógica?
3. Remova `--caches` e compare a configuração final com a versão que possui L1. Confirme as diferenças em `config.ini` antes de interpretar `stats.txt`.
4. Modifique `histograma.c` para usar um alfabeto de 256 símbolos. Discuta o efeito esperado sobre localidade e cache de dados.
5. Recrie a campanha de tamanhos de L1 usando o script Python e registre os resultados em CSV.

## Conclusão

O fluxo operacional do gem5 é: **construir ou selecionar a plataforma, associar um workload compatível, executar em um diretório de saída isolado, validar a configuração resolvida e analisar as estatísticas no contexto do modelo escolhido**. Dominar esse fluxo evita interpretações incorretas e fornece a base necessária para os tutoriais de hierarquia de memória, modelos de CPU, multicore, NoC e coerência de cache.
