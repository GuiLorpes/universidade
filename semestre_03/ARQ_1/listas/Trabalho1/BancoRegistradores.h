#ifndef BANCOREGISTRADORES_H
#define BANCOREGISTRADORES_H
#include <stdio.h>

typedef struct {
    double AC;
    double MQ;
    double PC;
    double MBR;
    double IR;
    double MAR;
} BancoRegistradores;

void inicializaRegistradores(BancoRegistradores *reg);

#endif

