#include <stdio.h>

int x,y;
void crescente(void) {
    if (x <= y) {
        printf("[%i, %i]\n", x, y);
    }
    else {
        printf("[%i, %i]\n", y, x);
    }
}


void main(void) {
    printf("Insira 2 valores inteiros: \n");
    printf("Insira o valor de x: \n");
    scanf("%i", &x);
    printf("Insira o valor de y: \n");
    scanf("%i", &y);
    crescente();
}