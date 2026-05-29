#ifndef BANCOREGISTRADORES_H
#define BANCOREGISTRADORES_H
#include <stdio.h>

typedef unsigned long long int ull;
typedef unsigned long int ul;
typedef unsigned int ui;

typedef struct {
    ull AC;
    ull MQ;
    ul PC;
    ull MBR;
    ui IR;
    ul MAR;
    ul IBR;
} BancoRegistradores;

void inicializaRegistradores(BancoRegistradores *reg);

#endif

