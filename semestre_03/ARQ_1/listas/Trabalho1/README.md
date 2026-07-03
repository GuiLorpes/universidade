# Simulador IAS - Trabalho de ARQ I

Este projeto implementa, em linguagem C, um simulador simplificado da arquitetura IAS, proposta por John von Neumann. O simulador executa programas escritos em arquivos `.txt`, carregando dados e instruções em uma memória simulada e mostrando o estado dos registradores durante o ciclo de execução.

## Arquitetura Simulada

A memória possui 1000 palavras de 40 bits:

- `M[0]` até `M[99]`: área de dados.
- `M[100]` até `M[999]`: área de instruções.

Cada palavra de instrução de 40 bits pode armazenar duas instruções de 20 bits:

```text
+--------------------+--------------------+
| instrução esquerda |  instrução direita |
|      0:19          |       20:39        |
+--------------------+--------------------+
```

Cada instrução possui:

```text
8 bits de opcode + 12 bits de endereço
```

O banco de registradores implementado possui os registradores clássicos do IAS:

- `AC`: acumulador.
- `MQ`: multiplicador/quociente.
- `PC`: contador de programa.
- `MBR`: registrador temporário para dados/instruções vindos da memória.
- `IR`: opcode da instrução atual.
- `MAR`: endereço de memória acessado.
- `IBR`: armazena temporariamente a instrução direita de uma palavra.

## Estrutura do Projeto

- `IAS.c`: ciclo de busca, decodificação, execução das instruções e interface principal.
- `Memoria.c` / `Memoria.h`: alocação e liberação da memória simulada.
- `BancoRegistradores.c` / `BancoRegistradores.h`: definição e inicialização dos registradores.
- `leituraArquivo.c` / `leituraArquivo.h`: leitura dos arquivos `.txt`, conversão de instruções para opcode e carregamento na memória.
- `*.txt`: programas e testes para o simulador.

## Compilação

Para compilar o simulador, use:

```bash
gcc -Wall -std=c99 IAS.c Memoria.c BancoRegistradores.c leituraArquivo.c -o ias
```

## Execução

Execute o simulador com:

```bash
./ias
```

O programa pedirá o nome de um arquivo `.txt` contendo dados e instruções:

```text
Insira o nome do arquivo do seu programa:
```

Exemplo:

```text
soma.txt
```

Ao final da execução, o simulador mostra uma amostra da memória de dados (`M[0]` até `M[99]`).

## Formato dos Arquivos de Entrada

Os arquivos de entrada não usam seções explícitas como `.data` ou `.text`. O leitor diferencia dados e instruções pelo formato da linha:

- Linhas contendo apenas números inteiros são carregadas como dados, a partir de `M[0]`.
- Linhas contendo mnemônicos são carregadas como instruções, a partir de `M[100]`.
- Comentários podem ser escritos com `#`.
- Linhas vazias são ignoradas.

Exemplo:

```txt
# Soma de 5 numeros
# Resultado esperado: M(6) = 16

5
3
4
1
2
6
0

LOAD M(6)
ADD M(1)
ADD M(2)
ADD M(3)
ADD M(4)
ADD M(5)
STOR M(6)
```

## Instruções Suportadas

O simulador reconhece as 21 instruções básicas do IAS usadas no trabalho. Nas instruções abaixo, `x` representa um endereço de memória.

### Transferência de Dados

```text
LOAD MQ
LOAD MQ,M(x)
STOR M(x)
LOAD M(x)
LOAD -M(x)
LOAD |M(x)|
LOAD -|M(x)|
```

### Aritmética

```text
ADD M(x)
ADD |M(x)|
SUB M(x)
SUB |M(x)|
MUL M(x)
DIV M(x)
LSH
RSH
```

### Saltos

```text
JUMP M(x, 0:19)
JUMP M(x, 20:39)
JUMP +M(x, 0:19)
JUMP +M(x, 20:39)
```

### Alteração de Endereço

```text
STOR M(x, 8:19)
STOR M(x, 28:39)
```

Essas duas instruções modificam o campo de endereço de uma instrução já armazenada na memória, permitindo comportamento de automodificação.


## Programas de Exemplo

- `soma.txt`: soma cinco números.
- `fatorial.txt`: calcula o fatorial de 5.
- `fibonacci.txt`: calcula os primeiros termos da sequência de Fibonacci.
- `maximo.txt`: encontra o maior valor de uma lista fixa.
- `selection_sort.txt`: ordena uma lista fixa usando trocas manuais.
- `multiplicacao_matriz.txt`: multiplica duas matrizes 2x2.