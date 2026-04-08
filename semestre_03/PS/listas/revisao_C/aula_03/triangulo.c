#include <stdio.h>
int numCamadas;


void main(void) {
    int camada = 0;
    printf("Quantas camadas você deseja para a sua piramide?\n");
    scanf("%d", &numCamadas);
    do {
        for (int i = 0; i < (numCamadas - camada); i++) {
            printf(" ");
        }
        for (int i = 0; i < ((camada * 2) - 1); i ++) {
            printf("*");
        }
        for (int i = 0; i < (numCamadas - camada); i++) {
            printf(" ");
        }
        printf("\n");
        camada++;
    } while (camada <= numCamadas);
}
