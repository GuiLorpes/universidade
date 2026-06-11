#ifndef BANCOREGISTRADORES_H
#define BANCOREGISTRADORES_H
#include <stdio.h>

typedef unsigned long long int ull;
typedef long long int ll;
typedef unsigned long int ul;
typedef unsigned int ui;

typedef struct {
    ll AC;
    ll MQ;
    ul PC;
    ull MBR;
    ui IR;
    ul MAR;
    ul IBR;
} BancoRegistradores;

void inicializaRegistradores(BancoRegistradores *reg);

#endif

