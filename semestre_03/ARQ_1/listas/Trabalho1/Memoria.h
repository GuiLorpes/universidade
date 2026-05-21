#ifndef MEMORIA_H
#define MEMORIA_H
#include <stdio.h>

typedef struct Memoria{
    double *memoria;
} Memoria;

void alocaMemoria(Memoria *m);
void liberaMemoroa(Memoria *m);

#endif