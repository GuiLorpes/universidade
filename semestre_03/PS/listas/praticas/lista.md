# Trilha de Mini Projetos em C

Esta trilha segue a ordem sugerida para praticar C com foco em ponteiros, alocacao dinamica, structs, arquivos e organizacao de codigo.

Ordem recomendada:

```txt
2 -> 3 -> 4 -> 5 -> 7 -> 10 -> 12 -> 13
```

## 1. Manipulador de Strings

Projeto original: **2**

### Objetivo

Reimplementar algumas funcoes basicas da biblioteca `string.h`, usando ponteiros diretamente.

### Funcoes sugeridas

```c
int minha_strlen(char *s);
void minha_strcpy(char *destino, char *origem);
int minha_strcmp(char *a, char *b);
void minha_strcat(char *destino, char *origem);
```

### Conceitos praticados

- Ponteiros para `char`
- Strings terminadas em `\0`
- Aritmetica de ponteiros
- Passagem de parametros por ponteiro
- Manipulacao manual de memoria ja alocada

### Checklist

- Ler duas strings do usuario
- Calcular o tamanho de uma string
- Copiar uma string para outra
- Comparar duas strings
- Concatenar duas strings
- Testar casos com string vazia

### Desafio extra

Criar versoes das funcoes sem usar indice, apenas incrementando ponteiros:

```c
while (*s != '\0') {
    s++;
}
```

---

## 2. Vetor Dinamico com Estatisticas

Projeto original: **3**

### Objetivo

Criar um vetor de inteiros com tamanho informado pelo usuario e calcular estatisticas basicas.

### Funcionalidades

- Ler o tamanho `n` do vetor
- Alocar o vetor dinamicamente com `malloc`
- Ler os valores do vetor
- Calcular maior valor
- Calcular menor valor
- Calcular media
- Contar numeros pares
- Contar numeros impares
- Liberar memoria com `free`

### Conceitos praticados

- `malloc`
- `free`
- Vetores dinamicos
- Ponteiros para arrays
- Funcoes recebendo ponteiros
- Validacao basica de entrada

### Funcoes sugeridas

```c
int maior_valor(int *vetor, int tamanho);
int menor_valor(int *vetor, int tamanho);
float calcular_media(int *vetor, int tamanho);
int contar_pares(int *vetor, int tamanho);
int contar_impares(int *vetor, int tamanho);
```

### Desafio extra

Criar uma funcao que recebe `int **vetor` e realoca o vetor para um novo tamanho.

---

## 3. Cadastro de Alunos

Projeto original: **4**

### Objetivo

Criar um sistema simples de cadastro de alunos usando `struct`.

### Struct sugerida

```c
typedef struct {
    char nome[100];
    int ra;
    float nota1;
    float nota2;
} Aluno;
```

### Funcionalidades

- Cadastrar alunos
- Listar alunos
- Buscar aluno por RA
- Calcular media de um aluno
- Mostrar se o aluno esta aprovado ou reprovado
- Mostrar todos os aprovados
- Mostrar todos os reprovados

### Conceitos praticados

- `struct`
- `typedef`
- Vetor de structs
- Ponteiro para struct
- Funcoes recebendo `Aluno *`
- Separacao de responsabilidades em funcoes

### Funcoes sugeridas

```c
void cadastrar_aluno(Aluno *aluno);
void listar_alunos(Aluno *alunos, int quantidade);
int buscar_por_ra(Aluno *alunos, int quantidade, int ra);
float calcular_media(Aluno aluno);
int esta_aprovado(Aluno aluno);
```

### Desafio extra

Trocar o vetor fixo de alunos por um vetor dinamico usando `malloc` e `realloc`.

---

## 4. Agenda de Contatos

Projeto original: **5**

### Objetivo

Criar uma agenda que permite cadastrar, buscar, editar e remover contatos.

### Struct sugerida

```c
typedef struct {
    char nome[100];
    char telefone[20];
    char email[100];
} Contato;
```

### Funcionalidades

- Adicionar contato
- Listar contatos
- Buscar contato por nome
- Editar contato
- Remover contato
- Crescer a lista conforme necessario

### Conceitos praticados

- `malloc`
- `realloc`
- `free`
- Array dinamico de structs
- Ponteiros para structs
- Manipulacao de strings dentro de structs

### Funcoes sugeridas

```c
void adicionar_contato(Contato **contatos, int *quantidade, int *capacidade);
void listar_contatos(Contato *contatos, int quantidade);
int buscar_contato(Contato *contatos, int quantidade, char *nome);
void editar_contato(Contato *contato);
void remover_contato(Contato *contatos, int *quantidade, int indice);
```

### Desafio extra

Ordenar os contatos por nome usando `strcmp`.

---

## 5. Agenda Salva em Arquivo

Projeto original: **7**

### Objetivo

Evoluir a agenda de contatos para salvar e carregar os dados usando arquivos.

### Funcionalidades

- Carregar contatos ao iniciar o programa
- Salvar contatos antes de sair
- Manter as funcionalidades da agenda anterior
- Permitir que os dados continuem existindo depois que o programa fechar

### Conceitos praticados

- `FILE *`
- `fopen`
- `fclose`
- `fprintf`
- `fscanf`
- `fread`
- `fwrite`
- Arquivos texto ou binarios

### Funcoes sugeridas

```c
int carregar_contatos(Contato **contatos, int *quantidade, int *capacidade, char *nome_arquivo);
int salvar_contatos(Contato *contatos, int quantidade, char *nome_arquivo);
```

### Caminho recomendado

Primeiro faca com arquivo texto, usando `fprintf` e `fscanf`.

Depois tente fazer com arquivo binario, usando `fwrite` e `fread`.

### Desafio extra

Salvar tambem a quantidade de contatos no inicio do arquivo binario.

---

## 6. Lista Encadeada de Inteiros

Projeto original: **10**

### Objetivo

Implementar uma lista encadeada do zero.

### Struct sugerida

```c
typedef struct No {
    int valor;
    struct No *proximo;
} No;
```

### Funcionalidades

- Inserir no inicio
- Inserir no fim
- Buscar valor
- Remover valor
- Imprimir lista
- Liberar toda a lista

### Conceitos praticados

- Ponteiro para struct
- Struct autorreferencial
- Alocacao de memoria no por no
- Manipulacao de ponteiros
- Casos especiais de remocao
- Liberacao correta de memoria

### Funcoes sugeridas

```c
No *criar_no(int valor);
void inserir_inicio(No **lista, int valor);
void inserir_fim(No **lista, int valor);
int buscar_valor(No *lista, int valor);
int remover_valor(No **lista, int valor);
void imprimir_lista(No *lista);
void liberar_lista(No **lista);
```

### Desafio extra

Criar uma funcao que inverte a lista encadeada.

---

## 7. Pilha e Fila

Projeto original: **12**

### Objetivo

Implementar estruturas de dados basicas: pilha e fila.

### Parte 1: Pilha

Uma pilha segue a regra LIFO: o ultimo que entra e o primeiro que sai.

Funcionalidades:

- `push`
- `pop`
- `top`
- verificar se esta vazia
- liberar memoria

### Parte 2: Fila

Uma fila segue a regra FIFO: o primeiro que entra e o primeiro que sai.

Funcionalidades:

- `enqueue`
- `dequeue`
- consultar primeiro elemento
- verificar se esta vazia
- liberar memoria

### Conceitos praticados

- TADs
- Ponteiros
- Lista encadeada
- Vetor dinamico
- Organizacao de codigo
- Separacao entre interface e implementacao

### Structs sugeridas

Pilha com lista:

```c
typedef struct No {
    int valor;
    struct No *proximo;
} No;

typedef struct {
    No *topo;
} Pilha;
```

Fila com lista:

```c
typedef struct {
    No *inicio;
    No *fim;
} Fila;
```

### Desafio extra

Separar o projeto em arquivos:

```txt
pilha.h
pilha.c
fila.h
fila.c
main.c
```

---

## 8. Mini Shell

Projeto original: **13**

### Objetivo

Criar um programa interativo que le comandos digitados pelo usuario.

Exemplo:

```txt
> help
> soma 2 3
> media 8 7
> sair
```

### Funcionalidades

- Ler uma linha completa do usuario
- Separar o comando dos argumentos
- Executar comandos diferentes
- Criar comando `help`
- Criar comando `sair`
- Criar comandos matematicos simples

### Conceitos praticados

- Strings
- `fgets`
- `strtok`
- Parsing de comandos
- Funcoes
- Menus interativos
- Ponteiros para funcao, se quiser avancar

### Comandos sugeridos

```txt
help
sair
soma 2 3
sub 10 4
mult 3 5
div 8 2
maior 10 3
strlen palavra
```

### Desafio extra

Criar uma tabela de comandos usando ponteiros para funcao.

Exemplo:

```c
typedef struct {
    char nome[20];
    void (*executar)(char **args);
} Comando;
```

---

## Dicas Gerais

Compile com warnings ligados:

```bash
gcc -Wall -Wextra -Wpedantic -g arquivo.c -o programa
```

Use `valgrind` quando trabalhar com `malloc`, `realloc` e `free`:

```bash
valgrind --leak-check=full ./programa
```

Sempre confira:

- Todo `malloc` foi testado?
- Todo `malloc` tem um `free` correspondente?
- Algum ponteiro pode estar apontando para memoria invalida?
- Alguma string pode estourar o tamanho do vetor?
- O programa trata entrada invalida?

## Ordem de Estudo Sugerida

1. Manipulador de Strings
2. Vetor Dinamico com Estatisticas
3. Cadastro de Alunos
4. Agenda de Contatos
5. Agenda Salva em Arquivo
6. Lista Encadeada de Inteiros
7. Pilha e Fila
8. Mini Shell
