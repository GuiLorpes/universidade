/*
UNIVERSIDADE ESTADUAL DE MARINGA
DEPARTAMENTO DE INFORM�TICA
CI�NCIA DA COMPUTA��O
PROGRAMA��O DE SISTEMAS - PROF.RONALDO

TRABALHO INDIVIDUAL DE NATUREZA PR�TICA MONITORADO
COM RESTRI��O DE TEMPO DE RESOLU��O (3 HORAS)
28/05/2026

NOME DO ALUNO:
RA:

=============================
Orientacoes Preliminares:

- Responda a quest�o diretamente neste arquivo e entregue-o no Moodle]

- Preencha seu nome e RA nos locais especificados

- Acrescente seu nome abreviado no nome do arquivo. Salve-o frequentemente para evitar perdas.

- N�o ser� permitido acesso a internet. Desconecte o cabo na internet quando for instru�do.

- N�o ser� permitido consulta a nenhum tipo de c�digo.

- Quando terminar, informe o professor, reconecte a internet e envie-o arquivo texto na plataforma Moodle. N�o converta o arquivo em PDF ou em outro formato que n�o seja texto.

- A implementacao deve ser feita em linguagem C, formatada e alinhada adequadamente. Desloque os comandos mais internos mais para a direita e alinhe as chaves correspondentes ao comando que pertencem.

- use nomes de variaveis adequadas a sua finalidade, por exemplo, "soma", "nome", "idade" etc. e nao use nomes que nada significam, tipo "w_p3", "xyz", "pa_daqui" etc.

- nao declare e nem use variaveis auxiliares/secundarias desnecessarias, que nao causam efeito relevante no programa.

ALERTA: Nao obtenha respostas de terceiros, senao sua prova sera anulada.

Boa Prova!

=============================

QUEST�O �NICA (10 PONTOS): Desenvolver um programa fonte em C para gerar, inverter e diagonalizar uma matriz de numeros inteiros. O usu�rio dever� fornecer as dimens�es da matriz e a op��o de diagonaliza��o. As matrizes original, invertida e diagonalizada devem ser mostradas na tela, todas tabuladas. Fa�a um loop no programa para permitir a reexecu��o por meio de uma pergunta. Siga as exig�ncias a seguir definidas.

- crie uma fun��o em C chamada "AlocaVetor()" que retorne no nome da fun��o um vetor de inteiros, alocado dinamicamente com malloc(), a partir do tamanho (numero de elementos) passado com par�metro. Os valores devem ser gerados aleatoriamente, podendo ser aleatoriamente negativos ou positivos.

- crie um procedimento em C chamado "CriaMatriz()" que retorne no par�metro uma matriz de n�meros inteiros, alocada dinamicamente com malloc(), a partir das dimens�es passadas como par�metros. A primeira dimens�o da matriz dever� indexar as linhas e a segunda dimens�o dever� indexar as colunas. Tal procedimento dever� criar a matriz usando a fun��o "AlocaVetor()" para criar as linhas.

- crie uma uma fun��o em C chamada "CopiaMatrizNoVetor()" para copiar uma matriz em um vetor alocado dinamicamente com malloc(). A matriz e as dimens�es s�o passados por par�metros e o vetor � retornado no nome da fun��o. A copia dever� "descarregar" os elementos das linhas da matriz no vetor.

- crie um procedimento em C chamado "ExtraiSubVetor()" para criar um vetor dinamicamente com malloc() contendo todos os elementos equidistantes de um vetor maior, a partir de uma posi��o inicial, da distancia, o vetor maior e o tamanho do vetor maior passados como par�metro. O subvetor criado dever� ser retornado no par�metro.

- crie um procedimento em C chamada "InverteMatriz()" para inverter uma matriz, trocando as linhas pelas colunas, tipo, a coluna 0 para a ser a linha 0, a coluna 1 para a ser a linha 1 e assim sucessivamente, usando a fun��o "CopiaMatrizNoVetor()" e o procedimento "ExtraiSubVetor()". A pr�pria matriz original deve ter seus elementos modificados. A matriz e as dimens�es dever�o ser passados como par�metros. Esse procedimento somente poder� ser utilizado se a matriz for quadrada, caso contr�rio, emitir� mensagem de impossibilidade.

- crie um procedimento em C chamada "DiagonalizaMatriz()" para transformar a matriz passada como parametro em matriz diagonal superior ou diagonal inferior, conforme op��o do usu�rio. A pr�pria matriz original deve ter seus elementos modificados. A matriz e as dimens�es dever�o ser passados como par�metros.

- Implemente um procedimento chamado "MostraMatriz()" para mostrar uma matriz tabulada na tela.

- Fa�a a fun��o principal (main) cumprir os objetivos da quest�o utilizando os procedimentos e fun��o especificados acima.

- Nenhum outro vetor (ou matriz), est�tico ou dinamico, deve ser declarado ou alocado.

- Nenhuma vari�vel global deve ser declarada, apenas tipo, se for o caso.

- Se for necess�rio, passe outros par�metros al�m dos j� definidos.

- Implemente seu programa a seguir. Boa sorte!

*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define maxValor 100

typedef int *tipoVetor;
typedef tipoVetor *tipoMatriz;  //ou typedef int **tipoMatriz;

void AlocaVetor(int tam, tipoVetor *v){

    int i,sinal;

    printf("\nAlocacao do Vetor:");

    *v = malloc(tam*sizeof(int));

    for (i=0; i<tam; i++){
        (*v)[i] = rand()%maxValor;
        sinal = 2 * (rand()%2)-1;
        (*v)[i] *= sinal;
    }
}

tipoMatriz CriaMatriz(int nlin, int ncol){
    int i;
    tipoMatriz m;
    printf("\nCriacao da Matriz:\n");

    m = malloc(nlin*sizeof(tipoVetor));

    for (i=0; i<nlin; i++){
        AlocaVetor(ncol, &m[i]);
    }
    return m;
}

void CopiaMatrizNoVetor(tipoMatriz M, tipoVetor *v, int nlin, int ncol){
    int i,j,k;

    printf("\nCopia da Matriz no Vetor:\n");

    *v=malloc(nlin*ncol*sizeof(int));

    k=0;
    for (i=0;i<nlin; i++){
        for (j=0; j<ncol; j++){
            (*v)[k]=M[i][j];
            k++;
        }
    }
}

tipoVetor ExtraiSubVetor(tipoVetor VMaior,int tamMaior,int ini,int salto){
    int i,k,tamMenor;
    tipoVetor vMenor;

    printf("\nExtracao do Subvetor:\n");

    tamMenor = 1 + ((tamMaior - ini) / salto);

    printf("\ntamMaior = %d tamMenor = %d salto = %d\n",tamMaior, tamMenor, salto);

    vMenor = malloc(tamMenor*sizeof(int));

    k=0;
    for (i=ini; i<tamMaior; i=i+salto){
        vMenor[k]=VMaior[i];
        k++;
    }
    return vMenor;
}

tipoMatriz InverteMatriz(tipoMatriz M, int nlin, int ncol){
    tipoMatriz novaMatriz = M;
    tipoVetor VMaior, VMenor;
    int tamMaior,tamMenor,i,j;

    printf("\nInversao da Matriz:\n");

    CopiaMatrizNoVetor(M, &VMaior,nlin,ncol);
    tamMaior = nlin * ncol;
    for (i=0;i<nlin;i++){
        VMenor = ExtraiSubVetor(VMaior,tamMaior,i,ncol);
        for (j=0;j<ncol;j++)
            novaMatriz[i][j]=VMenor[j];
        free(VMenor);
    }
    return novaMatriz;
}

tipoMatriz DiagonalizaMatriz(tipoMatriz M, int nlin, int ncol){
    tipoMatriz novaMatriz = M;
    int i,j,tipo;

    printf("\nDiagonalizacao da Matriz:\n");

    printf("\nDeseja Qual Diagonal: <0>Inferior ou <1>Superior? => ");
    scanf("%d",&tipo);

    if (tipo==0){
        for (i=0;i<nlin;i++){
            for (j=i+1;j<ncol;j++) {
                novaMatriz[i][j]=0;
            }
        }
    }
    else {
        for (i=1;i<nlin;i++){
            for (j=0;j<i;j++) {
                novaMatriz[i][j]=0;
            }
        }
    }
    return novaMatriz;
}

void MostraMatriz(tipoMatriz M, char *titulo, int nlin, int ncol){
    int i, j;

    printf("\nImpressao da Matriz:\n");
    printf("%s",titulo);

    for (i=0; i<nlin; i++){
        for (j=0;j<ncol;j++){
            printf("%5d",M[i][j]);
        }
        printf("\n");
    }

}

int main(void){
    int resp, nlin, ncol;
    tipoMatriz M;

    srand(time(NULL));

    do {

        printf("\nProgram Prova Pratica\n");
        printf("\nDigite o numero de linhas > ");
        scanf("%d",&nlin);

        printf("\nDigite o numero de colunas > ");
        scanf("%d",&ncol);

        M = CriaMatriz(nlin,ncol);

        MostraMatriz(M,"\nMatriz Original Aleatoria:\n",nlin,ncol);

        if (nlin==ncol) {
        M = InverteMatriz(M,nlin,ncol);
        MostraMatriz(M,"\nMatriz Invertida:\n",nlin,ncol);

        M = DiagonalizaMatriz(M,nlin,ncol);
        MostraMatriz(M,"\nMatriz Diagonalizada:\n",nlin,ncol);
        }
        else printf("\nProblema Aqui! A matriz nao eh quadrada\n");

        printf("\nDeseja Nova Execucao <0>SIM ou <1>Nao? => ");
        scanf("%d",&resp);
    } while (resp==0);
    return 0;
}

