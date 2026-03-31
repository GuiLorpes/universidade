#include <stdio.h>

int x,y,z;
void crescente(void) {
    if (x <= y) { // x < y
        if (y <= z) { // x < y < z
            printf("[%i, %i, %i]\n", x, y, z);
        }
        else { // z < y 
            if (z <= x) { // x < x < y
                printf("[%i, %i, %i]\n", z, x, y);
            }
            else { // x < z < y
                printf("[%i, %i, %i]\n", x, z, y);
            }
        }
    }
    else {  // y < x
        if (z <= y) { // z < y < x
            printf("[%i, %i, %i]\n", z, y, x);
        }
        else { // y < z 
            if (x <= z) { // y < x < z 
                printf("[%i, %i, %i]\n", y, x, z);
            }
            else { // y < z < x
                printf("[%i, %i, %i]\n", y, z, x);
            }
        }
    }
}

void main(void) {
    printf("Insira 2 valores inteiros: \n");
    printf("Insira o valor de x: \n");
    scanf("%i", &x);
    printf("Insira o valor de y: \n");
    scanf("%i", &y);
    printf("Insira o valor de z: \n");
    scanf("%i", &z);
    crescente();
}