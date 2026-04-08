#include <stdio.h>

int raio;

void main(void) {
    int nivel = 0; // vai até 2 * raio 
    printf("Que tamanho você deseja para o seu raio?\n");
    scanf("%i", &raio);
    do {
        for (i = 0; i < (nivel % (raio + 1))) // espaços
        
        printf("\n");
        nivel++;
    } while (nivel <= ((2 * raio) + 1));
}


* nivel = 0, raio 0

*** nivel = 0, raio = 1, espaços = 0, asteriscos = 3
*** nivel = 1, raio = 1, espaços = 0, asteriscos = 3
*** nivel = 2, raio = 1, espaços = 0, asteriscos = 3

 *** nivel = 0, raio = 2, espaços = 1, asteriscos = 3
***** nivel = 1, raio = 2, espaços = 0, asteriscos = 5
***** nivel = 2, raio = 2, espaços = 0, asteriscos = 5
***** nivel = 3, raio = 2, espaços = 0, asteriscos = 5
 *** nivel = 4, raio = 2, espaços = 1, asteriscos = 3

  *** 
 *****
*******
*******
*******
 *****
  ***