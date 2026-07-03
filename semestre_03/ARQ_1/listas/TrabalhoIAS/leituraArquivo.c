#include <ctype.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "leituraArquivo.h"


/*
Remove os comentários de uma linha linha
*/
static void removeComentario(char *linha) {
    char *comentario = strchr(linha, '#');
    if (comentario) {
        *comentario = '\0';
    }
}


/*
Retira os espaços presentes no começo e no fim de uma string
*/
static void trim(char *s) {
    char *inicio = s;
    // Verifica se o primeiro digito de s é um espaço
    while (*inicio && isspace((unsigned char)*inicio)) inicio ++;
    // Muda s para ficar igual ao inicio, sem espaços no começo
    if (inicio != s) memmove(s, inicio, strlen(inicio) + 1);

    char *fim = s + strlen(s) - 1;
    // Verifica o ultimo digito se é um espaço, se for remove ele
    while (fim >= s && isspace((unsigned char)*fim)) *fim-- = '\0';
}


/*
Verifica se a string é apenas um inteiro, ou se possui digitos
*/
static int isInteiro(const char *s, long *valor) {
    char *fim;
    /* Pega o valor, salva o inteiro no valor, e o restante da string no fim */
    *valor = strtol(s, &fim, 10);
    // Se não pegou valor nenhum, retorna 0 (false)
    if (fim == s) return 0;
    // Se algum momento fim tiver um caractere, retorna false
    while (*fim) {
        if (!isspace((unsigned char)*fim)) return 0;
        fim++;
    }
    return 1;
}


/*
Separa uma string entre o mnemonico, o valor do endereço, e a posição inicial
Retorna 1 se foi possivel decodificar corretamente
*/
static int decodificaString(const char *linha, char *mnemonico, int *endereco, \
    int *posInicial) {
    *endereco = 0;
    *posInicial = 0;

    char copia[256];
    strncpy(copia, linha, sizeof(copia)-1);
    copia[sizeof(copia) - 1] = '\0';

    // Verifica se tem um '(' para indicar que tem argumentos
    char *parenteses = strchr(copia, '(');
    if (parenteses == NULL) {
        trim(copia);
        // Instrução sem argumentos
        strcpy(mnemonico, copia);
        return 1;
    }

    *parenteses = '\0';
    trim(copia);
    strcpy(mnemonico, copia);
    char *fim = strchr(parenteses + 1, ')');
    if (fim == NULL) return 0; // formato invalido (não fechou parenteses)
    *fim = '\0';

    char *argumentos = parenteses + 1;
    
    // Se tiver virgula tem posição inicial
    char *virgula = strchr(argumentos, ',');
    if (virgula) {
        *virgula = '\0';
        trim(argumentos);
        *endereco = atoi(argumentos);
        char *intervalo = virgula + 1;
        trim(intervalo);
        char *doisPontos = strchr(intervalo, ':');
        if (doisPontos) *doisPontos = '\0';
        trim(intervalo);
        *posInicial = atoi(intervalo);
    }
    else {
        *endereco = atoi(argumentos);
    }
    return 1;
}


/*
Verifica uma instrução e retorna seu opcode
*/
static int getOpcode(char *mnemonico, int posInicial) {
    if (strcmp(mnemonico, "LOAD MQ") == 0) return 10;
    else if (strcmp(mnemonico, "LOAD MQ,M") == 0) return 9;
    else if (strcmp(mnemonico, "LOAD M") == 0) return 1;
    else if (strcmp(mnemonico, "LOAD -M") == 0) return 2;
    else if (strcmp(mnemonico, "LOAD |M") == 0) return 3;
    else if (strcmp(mnemonico, "LOAD -|M") == 0) return 4;
    else if (strcmp(mnemonico, "JUMP M") == 0) {
        if (posInicial == 0) return 13;
        if (posInicial == 20) return 14;
    }
    else if (strcmp(mnemonico, "JUMP +M") == 0) {
        if (posInicial == 0) return 15;
        if (posInicial == 20) return 16;
    }
    else if (strcmp(mnemonico, "ADD M") == 0) return 5;
    else if (strcmp(mnemonico, "ADD |M") == 0) return 7;
    else if (strcmp(mnemonico, "SUB M") == 0) return 6;
    else if (strcmp(mnemonico, "SUB |M") == 0) return 8;
    else if (strcmp(mnemonico, "MUL M") == 0) return 11;
    else if (strcmp(mnemonico, "DIV M") == 0) return 12;
    else if (strcmp(mnemonico, "LSH") == 0) return 20;
    else if (strcmp(mnemonico, "RSH") == 0) return 21;
    else if (strcmp(mnemonico, "STOR M") == 0) {
        if (posInicial == 8) return 18;
        if (posInicial == 28) return 19;
        return 33;
    }
    return -1;
}


/*

*/
static void gravaInstrucao(Memoria *m, int *enderecoInstrucao, int *esquerdaLivre, ull instrucao) {
    if (*esquerdaLivre) {
        m->memoria[*enderecoInstrucao] = instrucao << 20;
        *esquerdaLivre = 0;
    }
    else {
        m->memoria[*enderecoInstrucao] |= instrucao & 0xFFFFF;
        (*enderecoInstrucao)++;
        *esquerdaLivre = 1;
    }
}


int leArquivoPrograma(char *nomeArq, Memoria *m) {
    FILE *arq = fopen(nomeArq, "r");
    if (!arq) {
        perror(nomeArq);
        return 0;
    }

    int enderecoData = 0;
    int enderecoInstrucao = 100;
    int esquerdaLivre = 1;


    char linha[256];
    while (fgets(linha, sizeof(linha), arq) != NULL) {
        removeComentario(linha);
        trim(linha);
        if (linha[0] == '\0') continue;

        long int valor;
        if (isInteiro(linha, &valor)) {
            m->memoria[enderecoData++] = (ull)valor;
            printf("%ld\n", valor);
            continue;
        }
        
        char mnemonico[64];
        int endereco;
        int posInicial;

        if (!decodificaString(linha, mnemonico, &endereco, &posInicial)) {
            fprintf(stderr, "Erro no opcode : %s\n", mnemonico);
            return 0;
        }

        int opcode = getOpcode(mnemonico, posInicial);
        if (opcode < 0) {
            fprintf(stderr, "Erro no opcode %s\n", mnemonico);
            return 0;
        }

        ull instrucao = (((ull)opcode << 12) & 0xFF000) | ((ull)endereco & 0xFFF);
        gravaInstrucao(m, &enderecoInstrucao, &esquerdaLivre, instrucao);
        printf("%s, %i, %i\n", mnemonico, endereco, posInicial);
    }
    fclose(arq);
    return 1;
}