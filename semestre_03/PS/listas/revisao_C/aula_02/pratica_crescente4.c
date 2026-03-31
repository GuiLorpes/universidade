#include <stdio.h>

int x,y,z,a;
void crescente(void) {
    if (x <= y) { // x < y
        if (y <= z) { // x < y < z
            if (z <= a) { // x < y < z < a
                printf("[%i, %i, %i, %i]\n", x, y, z, a);
            }
            else if (y <= a){ // x < y < a < z 
                printf("[%i, %i, %i, %i]\n", x, y, a, z);
            }
            else if (x <= a){
                printf("[%i, %i, %i, %i]\n", x, a, y, z);
            }
            else { // a < x
                printf("[%i, %i, %i, %i]\n", a ,x, y, z);
            }
        }
        else { // z < y 
            if (z <= x) { // x < y e z < y 
                if (y <= a){ // z < x < y < a
                    printf("[%i, %i, %i, %i]\n", z, x, y, a);
                }
                else if (x <= a){ // z < x < a < y
                    printf("[%i, %i, %i, %i]\n", z, x, a, y);
                }
                else if (z <= a) {
                    printf("[%i, %i, %i, %i]\n", z, a, x, y);
                }
                else { // a < z
                    printf("[%i, %i, %i, %i]\n", a, z, x, y);
                }
            }
            else { // x < z < y
                if (y <= a) { // x < z < y < a
                    printf("[%i, %i, %i, %i]\n", x, z, y, a);
                }
                else if (z <= a) { // x < z < a < y
                    printf("[%i, %i, %i, %i]\n", x, z, a, y);
                }
                else if (x <= a) { // x < a < z < y
                    printf("[%i, %i, %i, %i]\n", x, a, z, y);
                }
                else { // a < x < z < y
                    printf("[%i, %i, %i, %i]\n", a, x, z, y);
                }
            }
        }
    }
    else {  // y < x
        if (z <= y) { // z < y < x
            if (x <= a) { // z < y < x < a
                printf("[%i, %i, %i, %i]\n", z, y, x, a);
            }
            else if (y <= a) { // z < y < a < x 
                printf("[%i, %i, %i, %i]\n", z, y, a, x);
            }
            else if (z <= a) { // z < a < y < x
                printf("[%i, %i, %i, %i]\n", z, a, y, x);
            }
            else { // a < z < y < x
                printf("[%i, %i, %i, %i]\n", a, z, y, x);
            }
        }
        else { // y < z 
            if (x <= z) { // y < x < z 
                if (z <= a) { // y < x < z < a
                    printf("[%i, %i, %i, %i]\n", y, x, z, a);
                }
                else if (x <= a) { // y < x < a < z
                    printf("[%i, %i, %i, %i]\n", y, x, a, z);
                }
                else if (y <= a) { // y < a < x < z
                    printf("[%i, %i, %i, %i]\n", y, a, x, z);
                }
                else { // a < y < x < z
                    printf("[%i, %i, %i, %i]\n", a, y, x, z);
                }
            }
            else { // y < z < x
                if (x <= a) { // y < z < x < a
                    printf("[%i, %i, %i, %i]\n", y, z, x, a);
                }
                else if (z <= a) { // y < z < a < x
                    printf("[%i, %i, %i, %i]\n", y, z, a, x);
                }
                else if (y <= a) { // y < a < z < x
                    printf("[%i, %i, %i, %i]\n", y, a, z, x);
                }
                else { // a < y < z < x
                    printf("[%i, %i, %i, %i]\n", a, y, z, x);
                }
            }
        }
    }
}

void main(void) {
    printf("Insira 4 valores inteiros: \n");
    printf("Insira o valor de x: \n");
    scanf("%i", &x);
    printf("Insira o valor de y: \n");
    scanf("%i", &y);
    printf("Insira o valor de z: \n");
    scanf("%i", &z);
    printf("Insira o valor de a: \n");
    scanf("%i", &a);
    crescente();
}