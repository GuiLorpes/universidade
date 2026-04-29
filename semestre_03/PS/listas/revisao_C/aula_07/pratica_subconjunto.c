#include <stdio.h>

void main(void) {
    int t1,t2;
    printf("Insira o tamanho dos seus vetores: \n");
    printf("Tamanho do vetor 1: ");
    scanf("%d", &t1);
    printf("Tamanho do vetor 2: ");
    scanf("%d", &t2);
    int v1[t1], v2[t2];
    
    srand(time(NULL));
    if (t1 > t2) {  
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
    }
}