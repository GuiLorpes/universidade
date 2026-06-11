#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include "Memoria.h"
#include "BancoRegistradores.h"
#include "leituraArquivo.h"


/* 
Todas as funções recebem um ponteiro para um banco de registradores e para 
a memória
*/


/*
Verifica se a proxima instrução está no IBR, se não estiver, faz a busca da 
próxima instrução na memória de acordo com o endereço que está no PC, e 
decodifica essa instrução.
*/
int busca(BancoRegistradores *br, Memoria m) {
    ull instrucao;
    ul endereco;
    int opcode;
    if (br->IBR == 0) {
        printf("IBR não possui a próxima instrução\n");
        printf("Inserindo a instrução do PC no MAR\n");
        // Não há mais instruções a serem realizadas, retorna 0.
        if (m.memoria[br->PC] == 0) {
            printf("\nNão há mais instruções a serem realizadas!\n");
            return 0;
        }
        br->MAR = m.memoria[br->PC];
        
        printf("Verificando se a instrução à esquerda do MAR é necessária\n");
        instrucao = br->MAR;
        ul instrucaoDir = instrucao & 0xFFFFF;
        ul instrucaoEsq = (instrucao >> 20) & 0xFFFFF; 
        
        if (instrucaoEsq == 0) {
            printf("Instrução a esquerda não é necessária\n");
            endereco = instrucaoDir & 0xFFF;
            opcode = (instrucaoDir >> 12) & 0xFF;
            br->IR = opcode;
            br->MAR = endereco;
            br->PC++;
        }
        else {
            printf("Instrução a esquerda é necessária\n");
            endereco = instrucaoEsq & 0xFFF;
            opcode = (instrucaoEsq >> 12) & 0xFF;
            br->IR = opcode;
            br->MAR = endereco;

            if (instrucaoDir != 0) {
                br->IBR = instrucaoDir;
            }
            else {
                br->PC++;
            }
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
        br->IBR = 0;
    }

    return 1;
}

/* 
Verifica a instrução contida no IR, realiza a instrução dependendo do OPCODE
*/
void execucao(BancoRegistradores *br, Memoria *m) {
    int opcode = br->IR;
    ul endereco = br->MAR;

    int enderecoNovo;
    ul instrucaoEsq, instrucaoDir, instrucaoNova;

    switch (opcode) {
    // Transferência de Dados
    case 10: // LOAD_MQ()
        printf("LOAD MQ\n");
        printf("AC <- MQ (%lld <- %lld)\n", br->AC, br->MQ);
        br->AC = br->MQ;
        break;
    case 9: // LOAD_MQ_M(int x)
        printf("LOAD MQ, M(%ld)\n", endereco);
        printf("MQ <- M(%ld) (%lld <- %lld)\n", endereco, br->MQ, 
            m->memoria[endereco]);
        br->MQ = m->memoria[endereco];
        break;
    case 33: // STOR_M(int x)
        printf("STOR M(%ld)\n", endereco);
        printf("M(%ld) <- AC (%lld <- %lld)\n", endereco, m->memoria[endereco], 
            br->AC);
        m->memoria[endereco] = br->AC;
        break;
    case 1: // LOAD_M(int x)
        printf("LOAD M(%ld)\n", endereco);
        printf("AC <- M(%ld) (%lld <- %lld)\n", endereco, br->AC, 
            m->memoria[endereco]);
        br->AC = m->memoria[endereco];
        break;
    case 2: // LOAD_negM(int x)
        printf("LOAD -M(%ld)\n", endereco);
        printf("AC <- -M(%ld) (%lld <- %lld)\n", endereco, br->AC, 
            -m->memoria[endereco]);
        br->AC = -(m->memoria[endereco]);
        break;
    case 3: // LOAD_absM(int x)
        printf("LOAD |M(%ld)|\n", endereco);
        printf("AC <- |M(%ld)| (%lld <- %d)\n", endereco, br->AC, 
            abs(m->memoria[endereco]));
        br->AC = abs(m->memoria[endereco]);
        break;
    case 4: // LOAD_neg_absM(int x)
        printf("LOAD -|MQ(%ld)|\n", endereco);
        printf("AC <- -|M(%ld)| (%lld <- %d)\n", endereco, br->AC, 
            -abs(m->memoria[endereco]));
        br->AC = -abs(m->memoria[endereco]);
        break;

    // Instruções aritméticas
    case 5: // ADD_M(int x)
        printf("ADD M(%ld)\n", endereco);
        br->AC = br->AC + m->memoria[endereco];
        break;
    case 7: // ADD_absM(int x)
        printf("ADD |M(%ld)|\n", endereco);
        br->AC = br->AC + abs(m->memoria[endereco]);
        break;
    case 6: // SUB_M(int x)
        printf("SUB M(%ld)\n", endereco);
        br->AC = br->AC - m->memoria[endereco];
        break;
    case 8: // SUB_absM(int x)
        printf("SUB |M(%ld)|\n", endereco);
        br->AC = br->AC - abs(m->memoria[endereco]);
        break;
    case 11: // MUL_M(int x) 
        printf("MUL M(%ld)\n", endereco);
        br->MQ = br->AC * m->memoria[endereco] & 0xFFFFFFFFFF;
        br->AC = ((br->AC * m->memoria[endereco]) >> 40) & 0xFFFFFFFFFF;
        break;
    case 12: // DIV_M(int x)
        printf("DIV M(%ld)\n", endereco);
        br->MQ = br->AC / m->memoria[endereco];
        br->AC = br->AC % m->memoria[endereco];
        break;
    case 20: // LSH
        printf("LSH\n");
        br->AC = (br->AC) << 1;
        break;
    case 21: // RSH
        printf("RSH\n");
        br->AC = (br->AC) >> 1;
        break;

    // Salto incondicional
    case 13: // JUMP_M(int x, 0)
        printf("JUMP M(%ld, 0:19)\n", endereco);
        br->IBR = 0;
        br->PC = endereco;
        break;
    case 14: // JUMP_M(int x, 20)
        printf("JUMP M(%ld, 20:39)\n", endereco);
        instrucaoDir = m->memoria[endereco] & 0xFFFFF;      
        br->IBR = instrucaoDir;  
        br->PC = endereco;
        break;
    
    // Salto condicional
    case 15: // JUMP_posiM(int x, 0)
        printf("JUMP +M(%ld, 0:19)\n", endereco);
        if (br->AC >= 0) {
            br->IBR = 0;
            br->PC = endereco;
        }
        else printf("jump não feito\n");
        break;
    case 16: // JUMP_posiM(int x, 20)
        printf("JUMP +M(%ld, 20:39)\n", endereco);
        if (br->AC >= 0) {
            instrucaoDir = m->memoria[endereco] & 0xFFFFF;      
            br->IBR = instrucaoDir;  
            br->PC = endereco;
        }
        else printf("jump não feito\n");
        break;
    
    // Alteração de endereço
    case 18: // STOR_M(int x, 8)
        printf("STOR M(%ld, 8:19)\n", endereco);
        instrucaoEsq = (m->memoria[endereco] >> 20) & 0xFFFFF; 
        enderecoNovo = br->AC & 0xFFF;
        instrucaoNova = (instrucaoEsq & 0xFF000) + enderecoNovo;
        m->memoria[endereco] = (m->memoria[endereco] & 0x00000FFFFF) + 
        (instrucaoNova << 20);
        break;
    case 19: // STOR_M(int x, 28)
        printf("STOR M(%ld, 28:39)\n", endereco);
        instrucaoDir = m->memoria[endereco] & 0xFFFFF; 
        enderecoNovo = br->AC & 0xFFF;
        instrucaoNova = (instrucaoDir & 0xFF000) | enderecoNovo;
        m->memoria[endereco] = (m->memoria[endereco] & 0xFFFFF00000)
         | instrucaoNova;
        break;

    default:
        printf("OPCODE inválido");
        break;
    }
}

void mostraMemoriaDados(Memoria *m) {
    printf("\nAmostra da memoria de dados (M[0] ate M[99]):\n");
    for (int i = 0; i < 100; i++) {
        printf("M[%02d] = %lld", i, (ll)m->memoria[i]);
        if ((i + 1) % 10 == 0) {
            printf("\n");
        }
        else {
            printf(" | ");
        }
    }
}


int main(void) {
    // Inicializa a memoria e o banco de registradores
    Memoria m;
    BancoRegistradores br;
    alocaMemoria(&m);
    inicializaRegistradores(&br);

    // Verifica o arquivo onde está a instrução, e o extrai para a memória
    char nomeArq[256];
    printf("Insira o nome do arquivo do seu programa: \n");
    fgets(nomeArq, sizeof(nomeArq), stdin);
    nomeArq[strcspn(nomeArq, "\n")] = '\0';
    leArquivoPrograma(nomeArq, &m);
    br.PC = 100;
    
    // Ciclo de Instruções
    int i = 1;
    while (busca(&br, m)) {
        printf("\nExcecução: %i\n", i);
        execucao(&br, &m);
        i++;
    }

    mostraMemoriaDados(&m);

    liberaMemoria(&m);
    return 0;
}

// gcc -Wall -std=c99 IAS.c Memoria.c BancoRegistradores.c leituraArquivo.c -o ias
