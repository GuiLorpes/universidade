#include "Memoria.h"
#include <stdlib.h>

#define TAM_MEMORIA 1000
#define TAM_PALAVRA 40

void alocaMemoria(Memoria *m) {
    m->memoria = malloc(TAM_MEMORIA * TAM_PALAVRA);
    if (m->memoria == NULL) {
        printf("Erro ao alocar memória");
    }
}

void liberarMemoria(Memoria *m) {
    if (m->memoria != NULL) {
        free(m->memoria);
        m->memoria = NULL;
    }
}