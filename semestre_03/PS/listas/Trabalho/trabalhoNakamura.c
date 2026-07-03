#include <stdio.h>
#include <stdlib.h>

typedef float **matriz

// Verifica o tamanho da matriz
//     Se a matriz for:
//         >= 4 calcula por Laplace
//         == 3 calcula por Sarrus
//         == 2 calcula por determinante 2x2
//         == 1 retorna ele mesmo
int calculaMatriz(matriz) {
    
}


// Verifica qual a linha/coluna com mais zeros
// A partir dela, faz os calculos da soma dos cofatores
//     Para os cofatores, calcula a matriz resultande da exclusão da linha ij
int calculaLaplace(matriz mat, int ordem) {
    float det;
    if (ordem == 3){
        return calculaSarrus();
    }
    else{
        float* linha  = mat[0];
        for (int j = 0; j< ordem; j++){
            matriz resultante = matrizResultante(mat, 0, j, ordem);
            det += (calculaLaplace(resultante, ordem -1 ) * mat[0][j]) *  potencia(-1, j + 1);
        }
    }

}

/*Produz a matriz que resulta da remoção da *i-ésima* linha e *j-ésima* coluna
da matriz *mat*, de ordem *ordem**/
matriz matrizResultante(matriz mat, int i, int j, int ordem){
    matriz res = criar_matriz(ordem -1);
    int res_k, res_l = -1;
    for (int k = 0;k< ordem;k++){
        if (k == i){k++;}
        else{res_k++;}
        for (int l = 0;l < ordem;l++){
            if (l == j){l ++;}
            else{res_l++;}
            res[res_k][res_l] = mat[k][l]; 
        }
    }
    return res;
}
/*Calcula a n-esima potencia de x (x deve ser maior que 0)*/
int potencia(float x, int n){
    float pot = 1;
    for (int i = 0;i < n; i ++){
        pot = pot * x;
    }
    return pot;
}


// Multiplica os resultados
int calculaSarrus(matriz) {

}

// Recebe uma matriz para ser calculada
void recebeMatrizes(ponteiro){
    printf("Insira o valor do ");
} 

void main(void) {
    int matriz;
    recebeMatrizes(matriz);
    printf(calculaMatriz(matriz));
}

/*retorna uma matriz vazia de ordem *ordem* */
matriz criar_matriz(int ordem){
    matriz mat = malloc(ordem*sizeof(double*));
    for (int k = 0; k < ordem; k++){
        mat[k] = malloc(ordem* sizeof(double));
    }
}