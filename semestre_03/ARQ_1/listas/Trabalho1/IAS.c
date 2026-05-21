#include <stdlib.h>
#include <stdio.h>
#include "Memoria.h"
#include "BancoRegistradores.h"

int TAM_MEMORIA = 1000;
int TAM_PALAVRA = 40;


// Memória
/* Aloca 1000 espaços (palavras) de 40 bytes na memória */
void alocaMemoria(Memoria *m) {
    m = malloc(TAM_MEMORIA * TAM_PALAVRA);
}
// Registradores
/* Cria os registradores AC, MQ, PC, MBR, IR, MAR */

int main(void) {
    Memoria *m;
    alocaMemoria(m);
    *(m)[67] = 69.0;
    printf("%d", m[67]);
    printf("%d", m[69]);
    free(m);
}