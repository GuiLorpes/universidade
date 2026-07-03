#include "Memoria.h"
#include <stdlib.h>

#define TAM_MEMORIA 1000
#define TAM_PALAVRA 40

void alocaMemoria(Memoria *m) {
    m->memoria = calloc(TAM_MEMORIA, sizeof(ull));
    if (m->memoria == NULL) {
        printf("Erro ao alocar memória");
    }
}

void liberaMemoria(Memoria *m) {
    if (m->memoria != NULL) {
        free(m->memoria);
        m->memoria = NULL;
    }
}