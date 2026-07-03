#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define maxDim 50

typedef double tipoMatriz[maxDim][maxDim];


void leDimensoes(int *nlA, int *ncA, int *ncB){

    printf("\nLeitura das Dimensoes:");

    printf("\nDigite o numero de linhas de A: ");
    scanf("%d",nlA);

    printf("\nDigite o numero de colunas de A: ");
    scanf("%d",ncA);

    printf("\nDigite o numero de colunas de B: ");
    scanf("%d",ncB);

    printf("obs: linhas de B = colunas de A\n\n");
}


tipoMatriz *geraMatriz(int nlin, int ncol){
    int i,j;
    tipoMatriz *M;

    M=malloc(sizeof(tipoMatriz));

    for (i=0; i<nlin; i++){
        for (j=0; j<ncol; j++){
            (*M)[i][j]=rand()%10;
        }
    }

    return M;
}

void mostraMatriz(char *nome, tipoMatriz M, int nlin, int ncol){
    int i,j;

    printf("\n%s:\n",nome);

    for (i=0; i<nlin; i++){
        for (j=0; j<ncol; j++){
            printf("%6.2lf  ",M[i][j]);
        }
        printf("\n");
        }
}


double multiplicaLinhaColuna(tipoMatriz A, int linA, tipoMatriz B, int colB, int nElem){
    double res;
    int i;

    res=0;

    for (i=0;i<nElem; i++)
        res=res+A[linA][i]*B[i][colB];

    return res;
    }

    void multiplicaMatriz(tipoMatriz A, int nlinA, int ncolA, tipoMatriz B, int ncolB, tipoMatriz **M){
    int i,j;


    *M=malloc(sizeof(tipoMatriz));

    for (i=0; i<nlinA; i++){
        for (j=0; j<ncolB; j++){
            (**M)[i][j]=multiplicaLinhaColuna(A,i,B,j,ncolA);
        }
    }
}


void main(void){

    tipoMatriz *A, *B, *C;

    int nLinA, nColA, nLinB, nColB, nLinC, nColC;

    srand(time(NULL));

    leDimensoes(&nLinA, &nColA, &nColB);
    nLinB=nColA;
    nLinC=nLinA;
    nColC=nColB;

    A=geraMatriz(nLinA, nColA);
    B=geraMatriz(nLinB, nColB);


    mostraMatriz("Matriz A Gerada",*A,nLinA, nColA);

    mostraMatriz("Matriz B Gerada",*B,nLinB, nColB);

    multiplicaMatriz(*A,nLinA,nColA,*B,nColB,&C);

    mostraMatriz("Matriz C Calculada",*C,nLinC, nColC);
}
