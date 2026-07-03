#include "BancoRegistradores.h"
#include <stdlib.h>

void inicializaRegistradores(BancoRegistradores *reg) {
    reg->AC = 0;
    reg->MQ = 0;
    reg->PC = 0;
    reg->MBR = 0;
    reg->IR = 0;
    reg->MAR = 0;
    reg->IBR = 0;
}