#ifndef MEMORIA_H
#define MEMORIA_H
#include <stdio.h>

typedef unsigned long long int ull;

typedef struct Memoria{
    ull *memoria;
} Memoria;

void alocaMemoria(Memoria *m);
void liberaMemoria(Memoria *m);

#endif