#include <stdio.h>

int i1,f1,i2,f2;

void coleta_coords(void) {
    printf("Insira as coordenadas para o segmento de reta r:\n");
    printf("Coordenada inicial: ");
    scanf("%i", &i1);
    printf("Coordenada final: ");
    scanf("%i", &f1);
    if (i1 > f1) {
        int temp = f1;
        f1 = i1;
        i1 = f1;
        printf("A cordenada inicial era maior que a final! Coordenadas \
trocadas!\n");
    }
    printf("Insira as coordenadas para o segmento de reta s:\n");
    printf("Coordenada inicial: ");
    scanf("%i", &i2);
    printf("Coordenada final: ");
    scanf("%i", &f2);
    if (i2 > f2) {
        int temp = f2;
        f2 = i2;
        i2 = f2;
        printf("A cordenada inicial era maior que a final! Coordenadas \
trocadas!\n");
    }
}

void main(void) {
    coleta_coords();
    if ((i1 > f2) || (i2 > f1)) {
        printf("r e s não possuem interseção\n");
    }
    else if (i1 == i2) {
        if (f1 == f2) {
            printf("r e s são retas coincidentes\n");
        }
        else if (f1 > f2) {
            printf("r e s tem interseção dentro do intervalo [%i, %i]\n", i1, f2);
        }
        else { // f1 < f2
            printf("r e s tem interseção dentro do intervalo [%i, %i]\n", i1, f1);
        }
    }  
    else if (i1 > i2) {
        if (f1 == f2) {
            printf("r e s tem interseção dentro do intervalo [%i, %i]\n", i1, f1);
        }
        else if (f1 > f2) {
            printf("r e s tem interseção dentro do intervalo [%i, %i]\n", i1, f2);
        }
        else { // f1 < f2
            printf("r e s tem interseção dentro do intervalo [%i, %i]\n", i1, f1);
        }
    }
    else { // i1 < i2
        if (f1 == f2) {
            printf("r e s tem interseção dentro do intervalo [%i, %i]\n", i2, f1);
        }
        else if (f1 > f2) {
            printf("r e s tem interseção dentro do intervalo [%i, %i]\n", i2, f2);
        }
        else { // f1 < f2
            printf("r e s tem interseção dentro do intervalo [%i, %i]\n", i2, f1);
        }
    }
}