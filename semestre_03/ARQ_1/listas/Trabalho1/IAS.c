#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include "Memoria.h"
#include "BancoRegistradores.h"

int TAM_MEMORIA = 1000;
int TAM_PALAVRA = 40;


/* 
Todas as funções recebem um ponteiro para um banco de registradores e para 
a memória
*/


/*
Verifica se a proxima instrução está no IBR, se não estiver, faz a busca da 
próxima instrução na memória de acordo com o endereço que está no PC, e 
decodifica essa instrução.
*/
void busca(BancoRegistradores *br, Memoria *m) {
    ull instrucao;
    ul endereco;
    int opcode;
    if (br->IBR == 0) {
        printf("IBR não possui a próxima instrução\n");
        printf("Inserindo a instrução do PC no MAR\n");
        br->MAR = m->memoria[br->PC];
        
        printf("Verificando se a instrução à esquerda do MAR é necessária\n");
        instrucao = br->MAR;
        long int instrucaoDir = instrucao & 0xFFFFF;
        long int instrucaoEsq = (instrucao >> 20) & 0xFFFFF; 
        
        if (instrucaoEsq == 0) {
            printf("Instrução a esquerda não é necessária");
            endereco = instrucaoDir & 0xFFF;
            opcode = (instrucaoDir >> 12) & 0xFF;
            br->IR = opcode;
            br->MAR = endereco;
        }
        else {
            printf("Instrução a esquerda é necessária");
            endereco = instrucaoEsq & 0xFFF;
            opcode = (instrucaoEsq >> 12) & 0xFF;
            br->IBR = instrucaoEsq;
        }
    }
    else {
        printf("IBR possui a próxima instrução\n");
        instrucao = br->IBR;
        endereco = instrucao & 0xFFF;
        opcode = (instrucao >> 12) & 0xFF;
        br->IR = opcode;
        br->MAR = endereco;
        br->PC++;
    }

    printf("%d", br->IR);
    printf("%ld", br->MAR);
}

/* 
Verifica a instrução contida no IR, realiza a instrução dependendo do OPCODE
*/
void execucao(BancoRegistradores *br, Memoria *m) {
    int opcode = br->IR;
    ul endereco = br->MAR;

    switch (opcode)
    {
    // Transferência de Dados
    case 10: // LOAD_MQ()
        br->AC = br->MQ;
        break;
    case 9: // LOAD_MQ_M(int x)
        br->MQ = m->memoria[endereco];
        break;
    case 33: // STOR_M(int x)
        m->memoria[endereco] = br->AC;
        break;
    case 1: // LOAD_M(int x)
        br->AC = m->memoria[endereco];
        break;
    case 2: // LOAD_negM(int x)
        br->AC = -(m->memoria[endereco]);
        break;
    case 3: // LOAD_absM(int x)
        br->AC = abs(m->memoria[endereco]);
        break;
    case 4: // LOAD_neg_absM(int x)
        br->AC = -abs(m->memoria[endereco]);
        break;

    // Instruções aritméticas
    case 5: // ADD_M(int x)
        br->AC = br->AC + m->memoria[endereco];
        break;
    case 7: // ADD_absM(int x)
        br->AC = br->AC + abs(m->memoria[endereco]);
        break;
    case 6: // SUB_M(int x)
        br->AC = br->AC - m->memoria[endereco];
        break;
    case 8: // SUB_absM(int x)
        br->AC = br->AC - abs(m->memoria[endereco]);
        break;
    case 11: // MUL_M(int x) 
        br->AC = br->AC * m->memoria[endereco] & 0xFFFFFFFFFF;
        br->MQ = ((br->MQ * m->memoria[endereco]) >> 40) & 0xFFFFFFFFFF;
        break;
    case 12: // DIV_M(int x)
        br->MQ = br->AC / m->memoria[endereco];
        br->AC = br->AC % m->memoria[endereco];
    case 20: // LSH
        br->AC = br->AC << 1;
        break;
    case 21: // RSH
        br->AC = br->AC >> 1;
        break;

    // Salto incondicional
    case 13: // JUMP_M(int x, 0)
        long int instrucaoEsq = (m->memoria[endereco] >> 20) & 0xFFFFF; 
        br->IR = (instrucaoEsq >> 12) & 0xFF;
        br->MAR = instrucaoEsq & 0xFFF;
        break;
    case 14: // JUMP_M(int x, 20)
        long int instrucaoDir = m->memoria[endereco] & 0xFFFFF;      
        br->IR = (instrucaoDir >> 12) & 0xFF;
        br->MAR = instrucaoDir & 0xFFF;  
        break;
    
    // Salto condicional
    case 15: // JUMP_posiM(int x, 0)
        if (br->AC >= 0) {
            long int instrucaoEsq = (m->memoria[endereco] >> 20) & 0xFFFFF; 
            br->IR = (instrucaoEsq >> 12) & 0xFF;
            br->MAR = instrucaoEsq & 0xFFF;
        }
        break;
    case 16: // JUMP_posiM(int x, 20)
        if (br->AC >= 0) {
            long int instrucaoDir = m->memoria[endereco] & 0xFFFFF;      
            br->IR = (instrucaoDir >> 12) & 0xFF;
            br->MAR = instrucaoDir & 0xFFF;  
        }
        break;
    
    // Alteração de endereço
    case 18: // STOR_M(int x, 0)
        
        break;
    case 19: // STOR_M(int x, 20)
        
        break;

    default:
        break;
    }
}


void cicloDeExecucao(BancoRegistradores *br, Memoria *m){

}




int main(void) {
    // Inicializa a memoria e o banco de registradores
    Memoria m;
    BancoRegistradores br;
    alocaMemoria(&m);
    inicializaRegistradores(&br);
    char nomeArq[256];
    printf("Insira o nome do arquivo do seu programa: \n");
    fgets(nomeArq, sizeof(nomeArq), stdin);
    nomeArq[strcspn(nomeArq, "\n")] = '\0';
    leArquivoPrograma(nomeArq, &m);



    liberaMemoria(&m);
    return 0;
}

// gcc -Wall -std=c99 IAS.c Memoria.c BancoRegistradores.c -o ias