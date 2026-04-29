#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int n;

void main(void) {
    char condicao;
    do {
        printf("Insira o tamanho dos seus vetores: \n");
        scanf("%d", &n);
        int vetor[n];
        srand(time(NULL));
        for (int i = 0; i < n; i++) {
            vetor[i] = rand() % 94;
        }
        printf("Inserido o vetor: ");
        for (int i = 0; i < n; i++) {
            if (i == 0) {
                printf("[%d", vetor[i]);
            }
            else {
                printf(", %d", vetor[i]);
            }
        }
        printf("]\n");
        for (int i = 0; i < n - 1; i++) {
            int indice_minimo = i;
            for (int j = i + 1; j < n; j++) {
                if (vetor[j] < vetor[indice_minimo]) {
                    indice_minimo = j;
                }
            }
        int aux = vetor[i];
        vetor[i] = vetor[indice_minimo];
        vetor[indice_minimo] = aux;

        }
        printf("Vetor ordendo: ");
        for (int i = 0; i < n; i++) {
            if (i == 0) {
                printf("[%d", vetor[i]);
            }
            else {
                printf(", %d", vetor[i]);
            }
        }
        printf("]\n");
        printf("Deseja realizar a operação novamente? s/n\n");
        getchar();
        scanf("%c", &condicao);
    } while (condicao == 's' || condicao == 'S');
} 
