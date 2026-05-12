#include <stdio.h>
#include <stdlib.h>

// // Verifica o tamanho da matriz
// //     Se a matriz for:
// //         >= 4 calcula por Laplace
// //         == 3 calcula por Sarrus
// //         == 2 calcula por determinante 2x2
// //         == 1 retorna ele mesmo
// int calculaMatriz(matriz) {
    
// }


// // Verifica qual a linha/coluna com mais zeros
// // A partir dela, faz os calculos da soma dos cofatores
// //     Para os cofatores, calcula a matriz resultande da exclusão da linha ij
// int calculaLaplace(matriz) {

// }


// // Multiplica os resultados
// int calculaSarrus() {

// }

// Recebe uma matriz para ser calculada
void recebeMatrizes(float **matriz){
    int ordem;
    printf("Insira qual a ordem da sua matriz:\n");
    scanf("%i", &ordem);
    *matriz = malloc(ordem * sizeof(float));
    for (int i = 0; i < ordem; i++) {
        matriz[i] = malloc(ordem * sizeof(float));
        for (int j = 0; j < ordem; j++) {
            printf("Insira o elemento a%i%i da matriz:\n", i, j);
            matriz[i][j] = scanf("%f\n");
        }
    }
    for (int i = 0; i < ordem; i++) {
        for (int j = 0; j < ordem; j++) {
            printf("%f ", matriz[i][j]);
        }
        printf("\n");
    }
} 

void main(void) {
    float *matriz = NULL; 
    recebeMatrizes(&matriz);
    // printf(calculaMatriz(matriz));
}
 
