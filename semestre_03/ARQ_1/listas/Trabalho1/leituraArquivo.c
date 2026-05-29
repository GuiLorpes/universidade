#include "leituraArquivo.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

void leArquivoPrograma(char *nomeArq, Memoria *m) {
    FILE *arq;
    arq = fopen(nomeArq, "r");
    
}

int decodificaString(char *mnemonico, int qtdParametros, int posInicial) {
    if (mnemonico == ""){}
    else if (){}
    else if (){}
    else if (){}
    else if (){}
    else if (){}
    else if (){}
    else if (){}
    else if (){}
    else if (){}
    else if (){}
    else if (){}
    else if (){}
    else if (){}
    else if (){}
    else if (){}
    else if (mnemonico == "LSH"){
        return 20;
    }
    else if (mnemonico == "RSH"){
        return 21;
    }
    else if (){}
    else if (){}
    else if (){}
    else if (){}



LOAD MQ,M(X)
STOR M(X)
LOAD M(X)
LOAD-M(X)
LOAD IM(X)I
LOAD -IM(X)I
JUMP M(X,0:19)
JUMP M(X,20:39)
JUMP + M(X,0: 19)
JUMP + M(X,20:39)
ADD M(X)
ADD IM(X)I
SUB M(X)
SUB IM(X)I
MUL M(X)
DIV M(X)
LSH
RSH
STOR M(X,8: 19)
STOR M(X,28:39)
}