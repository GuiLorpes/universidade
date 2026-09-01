#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned long ul;
typedef unsigned long long ull;

typedef struct Registrador {
    valor; 
} Registrador;


typedef struct FilaInstrucoes {
    ull *instrucao;
} FilaInstrucoes;


typedef struct BancoReg {
    Registrador *listaReg;
} BancoReg;
 
typedef struct Processador {
    ull *instrucao;
} Processador;

typedef struct EstacaoReserva {
    int busy;
    int operador;
    ul vj;
    ul vk;
    ul qj;
    ul qk;

} EstacaoReserva;



int emissao(FilaInstrucoes fila, EstacaoReserva estacaoReserva, Processador cpu, BancoReg bancoReg) {
    if (!verificaEstacoes(estacaoReserva)) {
        return 0;
    }
    ull instrucao = retira(fila);
    envia(estacaoReserva, instrucao);
}

void execucao(FilaInstrucoes fila, EstacaoReserva estacaoReserva, Processador cpu, BancoReg bancoReg) {
    verificaOperandos(estacaoReserva);
}


// O estado busy só é atualizado no fim da escrita dos resultados