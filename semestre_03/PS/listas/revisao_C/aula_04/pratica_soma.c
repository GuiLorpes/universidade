#include <stdio.h>

int v[10] = {0,0,0,0,0,0,0,0,0,0}, soma_par = 0, soma_impar = 0;

void main(void) {
    for (int i = 0; i < 10; i++) {
        printf("Defina o valor da posição %i\n", i);
        scanf("%i", &v[i]);
    }
    for (int i = 0; i < 10; i += 2) {
        soma_par += v[i];
    }
    for (int i = 1; i < 10; i += 2) {
        soma_impar += v[i];
    }
    printf("Você inseriu o vetor: ");
    for (int i = 0; i < 10; i++) {
        if (i == 0) {
            printf("%i", v[i]);
        }
        else {
        printf(", %i", v[i]);
        }
    }
    
    printf("\nA soma dos indices pares é igual a: %i", soma_par);
    printf("\nA soma dos indices impares é igual a: %i", soma_impar);
}