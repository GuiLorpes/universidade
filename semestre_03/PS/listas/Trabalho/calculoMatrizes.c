#include <stdio.h>
#include <stdlib.h>
#include <math.h>


typedef double **Matriz;


const char *ARQUIVO_MATRIZ = "matriz.txt";


double calculaSarrus(Matriz m);
double calculaLaplace(Matriz mat, int ordem);
Matriz matrizResultante(Matriz mat, int i, int j, int ordem);
double potencia(double x, int n);
double calculaMatriz(Matriz m, int ordem);
Matriz criaMatriz(int ordem);
void esvaziaMemoria(Matriz matriz, int ordem);
void alocaValoresMatriz(Matriz *matriz, int ordem);
void exibirMatriz(Matriz matriz, int ordem) ;
 

/*Calcula a n-esima potencia de x (n deve ser maior ou igual a 0)*/
double potencia(double x, int n){
    double pot = 1;
    for (int i = 0;i < n; i ++){
        pot = pot * x;
    }
    return pot;
}

// Multiplica os resultados
double calculaSarrus(Matriz m) {
    double a = (m[0][0] * m[1][1] * m[2][2]) + (m[0][1] * m[1][2] * m[2][0]) + \
    (m[0][2] * m[1][0] * m[2][1]);

    double b = (m[2][0] * m[1][1] * m[0][2]) + (m[2][1] * m[1][2] * m[0][0]) + \
    (m[2][2] * m[1][0] * m[0][1]);

    return a - b;
}

void esvaziaMemoria(Matriz matriz, int ordem) {
    for (int i = 0; i < ordem; i++) {
        free(matriz[i]);
    }
    free(matriz);
} 


/*Produz a matriz que resulta da remoção da *i-ésima* linha e *j-ésima* coluna
da matriz *mat*, de ordem *ordem**/
Matriz matrizResultante(Matriz mat, int i, int j, int ordem){
    Matriz res = criaMatriz(ordem -1);
    int res_k = 0;
    int res_l = 0;
    for (int k = 0;k< ordem;k++){
        if (k == i){continue;}
        for (int l = 0;l < ordem;l++){
            if (l == j){continue;}
            res[res_k][res_l] = mat[k][l];
            res_l++;
        }
        res_l = 0;
        res_k++;
    }
    return res;
}

/*Retorna a determinante de uma matriz de ordem maior que 4*/
double calculaLaplace(Matriz mat, int ordem) {
    double det = 0;
    for (int j = 0; j< ordem; j++){
        Matriz resultante = matrizResultante(mat, ordem-1, j, ordem);
        det += (calculaMatriz(resultante, ordem -1 ) * mat[ordem-1][j]) *  potencia(-1, (ordem-1) + j);
        esvaziaMemoria(resultante, ordem -1);
    }
    return det;

}

/*  
Verifica o tamanho da matriz
    Se a matriz for:
        >= 4 calcula por Laplace
        == 3 calcula por Sarrus
        == 2 calcula por determinante 2x2
        == 1 retorna ele mesmo
*/
double calculaMatriz(Matriz m, int ordem) {
    if (ordem > 3) {
        return calculaLaplace(m, ordem); 
    }
    else {
        switch (ordem)
        {
        case 3:
            return calculaSarrus(m);
        case 2:
            return m[0][0] * m[1][1] - (m[0][1] * m[1][0]);
        case 1:
            return m[0][0];
        }
    }
}

// Cria uma matriz vazia para ser preenchida
Matriz criaMatriz(int ordem){
    Matriz matriz = malloc(ordem * sizeof(double*));
    for (int i = 0; i < ordem; i++) {
        matriz[i] = malloc(ordem * sizeof(double));
    }
    return matriz;
}
 

// Aloca os valores na matriz de acordo com um arquivo de entrada
void alocaValoresMatriz(Matriz *matriz, int ordem) {
    FILE *arq;
    char linha[256];
    arq = fopen(ARQUIVO_MATRIZ, "r");
    if (arq == NULL) {
        printf("Erro ao abrir o arquivo!\n");
        return;
    }
    for (int i = 0; i < ordem; i ++) {
        for (int j = 0; j < ordem; j++) {
            fscanf(arq, "%lf", &((*matriz)[i][j]));
        }
        fgets(linha,256,arq);
    }
}


void exibirMatriz(Matriz matriz, int ordem) {
    for (int i = 0; i < ordem; i++) {
        printf("|");
        for (int j = 0; j < ordem; j++) {
            printf("%6.2f ", (matriz)[i][j]);
        }
        printf("|\n");
    }
}

int main(void) {
    int ordem;
    printf("Insira qual a ordem da sua matriz:\n");
    scanf("%i", &ordem);
    if (ordem <= 0) {
        printf("Ordem inserida é inválida!");
        return 0;
    }
    Matriz m = criaMatriz(ordem);

    alocaValoresMatriz(&m, ordem);
    exibirMatriz(m, ordem);

    printf("\nDeterminante = %.2f\n", calculaMatriz(m, ordem));
    esvaziaMemoria(m, ordem);
    return 0;
}
 