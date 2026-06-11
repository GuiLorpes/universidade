/*
UNIVERSIDADE ESTADUAL DE MARINGA
DEPARTAMENTO DE INFORMÁTICA
CIÊNCIA DA COMPUTAÇÃO
PROGRAMAÇÃO DE SISTEMAS - PROF.RONALDO

TRABALHO INDIVIDUAL DE NATUREZA PRÁTICA MONITORADO
COM RESTRIÇÃO DE TEMPO DE RESOLUÇÃO (3 HORAS)
28/05/2026

NOME DO ALUNO: Guilherme dos Santos Lira Lopes
RA: 143630

=============================
Orientacoes Preliminares:

- Responda a questão diretamente neste arquivo e entregue-o no Moodle]

- Preencha seu nome e RA nos locais especificados

- Acrescente seu nome abreviado no nome do arquivo. Salve-o frequentemente para evitar perdas.

- Não será permitido acesso a internet. Desconecte o cabo na internet quando for instruído.

- Não será permitido consulta a nenhum tipo de código.

- Quando terminar, informe o professor, reconecte a internet e envie-o arquivo texto na plataforma Moodle. Não converta o arquivo em PDF ou em outro formato que não seja texto.

- A implementacao deve ser feita em linguagem C, formatada e alinhada adequadamente. Desloque os comandos mais internos mais para a direita e alinhe as chaves correspondentes ao comando que pertencem.

- use nomes de variaveis adequadas a sua finalidade, por exemplo, "soma", "nome", "idade" etc. e nao use nomes que nada significam, tipo "w_p3", "xyz", "pa_daqui" etc.

- nao declare e nem use variaveis auxiliares/secundarias desnecessarias, que nao causam efeito relevante no programa.

ALERTA: Nao obtenha respostas de terceiros, senao sua prova sera anulada.

Boa Prova!

=============================

QUESTÃO ÚNICA (10 PONTOS): Desenvolver um programa fonte em C para gerar, 
inverter e diagonalizar uma matriz de numeros inteiros. O usuário deverá fornecer 
as dimensões da matriz e a opção de diagonalização. As matrizes original, 
invertida e diagonalizada devem ser mostradas na tela, todas tabuladas. Faça um 
loop no programa para permitir a reexecução por meio de uma pergunta. Siga as 
exigências a seguir definidas.

- crie uma função em C chamada "AlocaVetor()" que retorne no nome da função um 
vetor de inteiros, alocado dinamicamente com malloc(), a partir do tamanho 
(numero de elementos) passado com parâmetro. Os valores devem ser gerados 
aleatoriamente, podendo ser aleatoriamente negativos ou positivos.

- crie um procedimento em C chamado "CriaMatriz()" que retorne no parâmetro uma 
matriz de números inteiros, alocada dinamicamente com malloc(), a partir das 
dimensões passadas como parâmetros. A primeira dimensão da matriz deverá indexar 
as linhas e a segunda dimensão deverá indexar as colunas. Tal procedimento 
deverá criar a matriz usando a função "AlocaVetor()" para criar as linhas.

- crie uma uma função em C chamada "CopiaMatrizNoVetor()" para copiar uma matriz 
em um vetor alocado dinamicamente com malloc(). A matriz e as dimensões são 
passados por parâmetros e o vetor é retornado no nome da função. A copia deverá 
"descarregar" os elementos das linhas da matriz no vetor.

- crie um procedimento em C chamado "ExtraiSubVetor()" para criar um vetor 
dinamicamente com malloc() contendo todos os elementos equidistantes de um vetor 
maior, a partir de uma posição inicial, da distancia, o vetor maior e o tamanho 
do vetor maior passados como parâmetro. O subvetor criado deverá ser retornado 
no parâmetro.

- crie um procedimento em C chamada "InverteMatriz()" para inverter uma matriz, 
trocando as linhas pelas colunas, tipo, a coluna 0 para a ser a linha 0, a 
coluna 1 para a ser a linha 1 e assim sucessivamente, usando a função 
"CopiaMatrizNoVetor()" e o procedimento "ExtraiSubVetor()". A própria matriz 
original deve ter seus elementos modificados. A matriz e as dimensões deverão 
ser passados como parâmetros. Esse procedimento somente poderá ser utilizado se 
a matriz for quadrada, caso contrário, emitirá mensagem de impossibilidade.

- crie um procedimento em C chamada "DiagonalizaMatriz()" para transformar a 
matriz passada como parametro em matriz diagonal superior ou diagonal inferior, 
conforme opção do usuário. A própria matriz original deve ter seus elementos 
modificados. A matriz e as dimensões deverão ser passados como parâmetros.

- Implemente um procedimento chamado "MostraMatriz()" para mostrar uma matriz 
tabulada na tela.

- Faça a função principal (main) cumprir os objetivos da questão utilizando 
os procedimentos e função especificados acima.

- Nenhum outro vetor (ou matriz), estático ou dinamico, deve ser declarado ou 
alocado.

- Nenhuma variável global deve ser declarada, apenas tipo, se for o caso.

- Se for necessário, passe outros parâmetros além dos já definidos.

- Implemente seu programa a seguir. Boa sorte!

*/

#include <stdio.h>
#include <time.h>
#include <stdlib.h>


typedef int **Matriz;


int *alocaVetor(int qtdElem) {
    int *vetor = malloc(qtdElem * sizeof(int));
    for (int i = 0; i < qtdElem; i++) {
        int valor = rand() % 784;
        if (valor % 67 == 0) {
            valor *= -1;
        } 
        vetor[i] = valor;
    }
    return vetor;
}

void criaMatriz(Matriz *m, int linha, int coluna) {
    *m = malloc(linha * sizeof(int));
    for (int i = 0; i < linha; i++) {
        (*m)[i] = alocaVetor(coluna);
    }
}

void mostraMatriz(Matriz m, int linha, int coluna) {
    for (int i = 0; i < linha; i++) {
        printf("| ");
        for (int j = 0; j < coluna; j++) {
            printf("%i ", m[i][j]);
        }
        printf("|\n");
    }
}

int copiaMatrizNoVetor(Matriz matriz, int linha, int coluna) {
    int vetorCopia;
    int *ptr_vetorCopia = &vetorCopia;
    ptr_vetorCopia = malloc((linha * coluna) * sizeof(int));
    for (int k = 0; k < (linha * coluna); k++) {
        for (int i = 0; i < linha; i++) {
            for (int j = 0; j < coluna; j++) {
                (ptr_vetorCopia)[k] = matriz[i][j];
            }
        }
        
    }
    return *ptr_vetorCopia;
}

int extraiSubvetor(int vetor[], int posInicial, int distancia, int tamVetor) {
    int novoVetor;
    int *ptr_novoVetor = malloc(tamVetor * sizeof(int));
    int i = posInicial, j = 0;
    while (i < tamVetor) {
        ptr_novoVetor[j] = vetor[i];
        i += distancia;
        j++;
    }
    return *ptr_novoVetor;
}

void inverteMatriz(Matriz *m, int linha, int coluna) {
    if (linha != coluna) {
        printf("Erro! Não foi possivel inverter essa matriz (Não é quadrada)");
    }
    else {
        int vetorMatriz;
        int *ptr_vetorMatriz = &vetorMatriz;
        *ptr_vetorMatriz = copiaMatrizNoVetor(*m, linha, coluna);
        int i = 0, j = 0;
        while (i < linha) {
            int vetorLinha;
            int *ptr_vetorLinha = &vetorLinha;
            *ptr_vetorLinha = extraiSubvetor(ptr_vetorMatriz, i + coluna, coluna, (linha * coluna));
            while (j < coluna) {
                (*m)[j][i] = ptr_vetorLinha[j];
                j++;
            }
            j = 0;
            i++;
        }
    }
}


void diagonalizaMatriz(Matriz *m, int linha, int coluna) {
    if (linha != coluna) {
        printf("Erro! Não foi possivel diagonalizar essa matriz (Não é quadrada)");
    }
    else {
        int opcao;
        printf("Deseja transformar em uma matriz diagonal inferior(1) ou superior(2)?\n");
        scanf("%i", &opcao);
        switch (opcao)
        {
        case 1:
            for (int i = 0; i < linha; i++) {
                for (int j = 0; j < coluna; j++) {
                    if (i > j) {
                        (*m)[i][j] = 0;
                    }
                }
            }
            break;
        case 2:
            for (int i = 0; i < linha; i++) {
                for (int j = 0; j < coluna; j++) {
                    if (i < j) {
                        (*m)[i][j] = 0;
                    }
                }
            }
            break;
        default:
            printf("Valor inserido inválido!");
            break;
        }
    }
}


int main() {
    int caso = 0;
    printf("Bem vindo a minha prova de PS\n");
    do {
        srand(time(NULL));
        Matriz matriz = NULL;
        int linha, coluna;
        printf("Insira quantas linhas deseja ter a sua matriz: \n");
        scanf("%i", &linha);
        printf("Insira quantas colunas deseja ter a sua matriz: \n");
        scanf("%i", &coluna);
        criaMatriz(&matriz, linha, coluna);
        mostraMatriz(matriz, linha, coluna);
        inverteMatriz(&matriz, linha, coluna);
        mostraMatriz(matriz, linha, coluna);
        diagonalizaMatriz(&matriz, linha, coluna);
        mostraMatriz(matriz, linha, coluna);
        printf("Deseja realizar outra operação? 1 - Sim | 0 - Sair\n");
        scanf("%i", &caso);
    } while (caso != 0);
}