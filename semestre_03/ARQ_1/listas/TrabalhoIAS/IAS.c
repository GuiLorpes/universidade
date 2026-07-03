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
    if (br->IBR == 0) {
        // Não há mais instruções a serem realizadas, retorna 0.
        if (m.memoria[br->PC] == 0) {
            printf("\nNão há mais instruções a serem realizadas!\n");
            return 0;
        }
        br->MAR = br->PC;
        br->MBR = m.memoria[br->MAR];
        
        ul instrucaoDir = br->MBR & 0xFFFFF;
        ul instrucaoEsq = (br->MBR >> 20) & 0xFFFFF; 
        
        if (instrucaoEsq == 0) {
            br->IR = (instrucaoDir >> 12) & 0xFF;
            br->MAR = instrucaoDir & 0xFFF;;
            br->PC++;
        }
        else {
            br->IR = (instrucaoEsq >> 12) & 0xFF;;
            br->MAR = instrucaoEsq & 0xFFF;;

            if (instrucaoDir != 0) {
                br->IBR = instrucaoDir;
            }
            else {
                br->PC++;
            }
        }
    }
    else {
        br->IR = (br->IBR >> 12) & 0xFF;
        br->MAR = br->IBR & 0xFFF;;
        br->PC++;
        br->IBR = 0;
    }

    return 1;
}

/* 
Verifica a instrução contida no IR, realiza a instrução dependendo do OPCODE
*/
void execucao(BancoRegistradores *br, Memoria *m) {
    int enderecoNovo;
    ul instrucaoEsq, instrucaoDir, instrucaoNova;

    switch (br->IR) {
    // Transferência de Dados
    case 10: // LOAD_MQ()
        br->MBR = br->MQ;

        printf("LOAD MQ\n");
        printf("AC <- MQ (%lld <- %lld)\n", br->AC, br->MBR);

        br->AC = br->MBR;
        break;
    case 9: // LOAD_MQ_M(int x)
        br->MBR = m->memoria[br->MAR];

        printf("LOAD MQ, M(%ld)\n", br->MAR);
        printf("MQ <- M(%ld) (%lld <- %lld)\n", br->MAR, br->MQ, 
            br->MBR);

        br->MQ = br->MBR;
        break;
    case 33: // STOR_M(int x)
        br->MBR = br->AC;

        printf("STOR M(%ld)\n", br->MAR);
        printf("M(%ld) <- AC (%lld <- %lld)\n", br->MAR, m->memoria[br->MAR], 
                                                br->MBR);

        m->memoria[br->MAR] = br->MBR;
        break;
    case 1: // LOAD_M(int x)
        br->MBR = m->memoria[br->MAR];

        printf("LOAD M(%ld)\n", br->MAR);
        printf("AC <- M(%ld) (%lld <- %lld)\n", br->MAR, br->AC, br->MBR);

        br->AC = br->MBR;
        break;
    case 2: // LOAD_negM(int x)
        br->MBR = m->memoria[br->MAR];

        printf("LOAD -M(%ld)\n", br->MAR);
        printf("AC <- -M(%ld) (%lld <- %lld)\n", br->MAR, br->AC, 
                                                -br->MBR);

        br->AC = -br->MBR;
        break;
    case 3: // LOAD_absM(int x)
        br->MBR = m->memoria[br->MAR];

        printf("LOAD |M(%ld)|\n", br->MAR);
        printf("AC <- |M(%ld)| (%lld <- %d)\n", br->MAR, br->AC, 
                                                abs(br->MBR));

        br->AC = abs(br->MBR);
        break;
    case 4: // LOAD_neg_absM(int x)
        br->MBR = m->memoria[br->MAR];

        printf("LOAD -|MQ(%ld)|\n", br->MAR);
        printf("AC <- -|M(%ld)| (%lld <- %d)\n", 
            br->MAR, br->AC, -abs(br->MBR));

        br->AC = -abs(br->MBR);
        break;

    // Instruções aritméticas
    case 5: // ADD_M(int x)
        br->MBR = m->memoria[br->MAR];

        printf("ADD M(%ld)\n", br->MAR);
        printf("AC <- AC + M(%ld) (%lld <- %lld + %lld)\n",
        br->MAR, br->AC, br->AC, br->MBR);
        
        br->AC = br->AC + br->MBR;
        break;
    case 7: // ADD_absM(int x)
        br->MBR = m->memoria[br->MAR];

        printf("ADD |M(%ld)|\n", br->MAR);
        printf("AC <- AC + |M(%ld)| (%lld <- %lld + |%lld|)\n",
        br->MAR, br->AC, br->AC, (ll)abs(br->MBR));

        br->AC = br->AC + (ll)abs(br->MBR);
        break;
    case 6: // SUB_M(int x)
        br->MBR = m->memoria[br->MAR];

        printf("SUB M(%ld)\n", br->MAR);
        printf("AC <- AC - M(%ld) (%lld <- %lld - %lld)\n",
        br->MAR, br->AC, br->AC, br->MBR);
        
        br->AC = br->AC - br->MBR;
        break;
    case 8: // SUB_absM(int x)
        br->MBR = m->memoria[br->MAR];
        
        printf("SUB |M(%ld)|\n", br->MAR);
        printf("AC <- AC - |M(%ld)| (%lld <- %lld - |%lld|)\n",
        br->MAR, br->AC, br->AC, (ull)abs(br->MBR));

        br->AC = br->AC - (ll)abs(br->MBR);
        break;
    case 11: // MUL_M(int x) 
        
        br->MBR = m->memoria[br->MAR];
        long long int multiplicacao = br->AC * br->MBR;
        printf("MUL M(%ld)\n", br->MAR);
        printf("MQ <- AC * M(%ld) (%lld <- %lld * %lld) (LSB)\n", 
            br->MAR, br->MQ, br->AC, br->MBR);
        printf("AC <- AC * M(%ld) (%lld <- %lld * %lld) (MSB)\n", 
        br->MAR, br->AC, br->AC, br->MBR);
        
        br->MQ = multiplicacao & 0xFFFFFFFFFF;
        br->AC = (multiplicacao >> 40) & 0xFFFFFFFFFF;
        break;
    case 12: // DIV_M(int x)
        br->MBR = m->memoria[br->MAR];

        printf("DIV M(%ld)\n", br->MAR);
        printf("MQ <- AC / M(%ld) (%lld <- %lld / %lld)\n", 
            br->MAR, br->MQ, br->AC, br->MBR);
            
        printf("AC <- AC %% M(%ld) (%lld <- %lld %% %lld)\n",
            br->MAR, br->AC, br->AC, br->MBR);

        if (br->MBR == 0) {
            printf("ERRO! Divisão por 0!\n");
            break;
        }
        br->MQ = br->AC / br->MBR;
        br->AC = br->AC % br->MBR;
        break;
    case 20: // LSH
        printf("LSH\n");
        printf("AC <- AC * 2 (%lld <- %lld * 2)\n", br->AC, br->AC);
        br->AC = (br->AC) << 1;
        break;
    case 21: // RSH
        printf("RSH\n");
        printf("AC <- AC / 2 (%lld <- %lld / 2)\n", br->AC, br->AC);
        br->AC = (br->AC) >> 1;
        break;

    // Salto incondicional
    case 13: // JUMP_M(int x, 0)
        printf("JUMP M(%ld, 0:19)\n", br->MAR);
        br->MBR = br->MAR;
        br->IBR = 0;
        br->PC = br->MBR;
        break;
    case 14: // JUMP_M(int x, 20)
        printf("JUMP M(%ld, 20:39)\n", br->MAR);
        br->MBR = br->MAR;
        br->IBR = m->memoria[br->MBR] & 0xFFFFF;  
        br->PC = br->MBR;
        break;
    
    // Salto condicional
    case 15: // JUMP_posiM(int x, 0)
        printf("JUMP +M(%ld, 0:19)\n", br->MAR);
        if (br->AC > 0) {
            br->MBR = br->MAR;
            br->IBR = 0;
            br->PC = br->MBR;
        }
        break;
    case 16: // JUMP_posiM(int x, 20)
        printf("JUMP +M(%ld, 20:39)\n", br->MAR);
        if (br->AC > 0) {
            br->MBR = br->MAR;
            br->IBR = m->memoria[br->MBR] & 0xFFFFF;  
            br->PC = br->MBR;
        }
        break;
    
    // Alteração de endereço
    case 18: // STOR_M(int x, 8:19)
        printf("STOR M(%ld, 8:19)\n", br->MAR);
        br->MBR = m->memoria[br->MAR];
        instrucaoEsq = (br->MBR >> 20) & 0xFFFFF; 
        enderecoNovo = br->AC & 0xFFF;
        instrucaoNova = (instrucaoEsq & 0xFF000) | enderecoNovo;
        m->memoria[br->MAR] = (br->MBR & 0x00000FFFFF) | (instrucaoNova << 20);
        break;
    case 19: // STOR_M(int x, 28:39)
        printf("STOR M(%ld, 28:39)\n", br->MAR);
        br->MBR = m->memoria[br->MAR];
        instrucaoDir = br->MBR & 0xFFFFF; 
        enderecoNovo = br->AC & 0xFFF;
        instrucaoNova = (instrucaoDir & 0xFF000) | enderecoNovo;
        m->memoria[br->MAR] = (br->MBR & 0xFFFFF00000) | instrucaoNova;
        break;

    default:
        printf("OPCODE inválido\n");
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
    printf("\n");
}


void mostraRegistradores(BancoRegistradores br) {
    printf("=== Registradores ===\n");
    printf("AC -> %lld\n", br.AC);
    printf("MQ -> %lld\n", br.MQ);
    printf("PC -> %ld\n", br.PC);
    printf("MBR -> %lld\n", br.MBR);
    printf("IR -> %d\n", br.IR);
    printf("MAR -> 0x%03lX\n", br.MAR);
    printf("IBR -> 0x%05lX\n", br.IBR);
    printf("=====================\n");
}


int main(void) {
    // Inicializa a memoria e o banco de registradores
    printf("==-------== SIMULADOR IAS 2000 ==-------== \n");
    int simulacao = 0;
    do {
        Memoria m;
        BancoRegistradores br;
        alocaMemoria(&m);
        inicializaRegistradores(&br);

        // Verifica o arquivo onde está a instrução, e o extrai para a memória
        char nomeArq[256];
        printf("Insira o nome do arquivo do seu programa: \n");
        fgets(nomeArq, sizeof(nomeArq), stdin);
        nomeArq[strcspn(nomeArq, "\n")] = '\0';
        if (!leArquivoPrograma(nomeArq, &m)) {
            printf("Erro na leitura do algoritmo!\nSimulador parando!\n");
            return 0;
        }
        br.PC = 100;
        
        // Ciclo de Instruções
        int i = 1;
        while (busca(&br, m)) {
            printf("\nExcecução: %i\n", i);
            execucao(&br, &m);
            mostraRegistradores(br);
            i++;
        }

        mostraMemoriaDados(&m);

        liberaMemoria(&m);

        printf("Deseja realizar algum outro programa? 1 -> Sim | 0 -> Não \n");
        scanf("%i", &simulacao);
        getchar();
    } while (simulacao);
    return 0;
}

// gcc -Wall -std=c99 IAS.c Memoria.c BancoRegistradores.c leituraArquivo.c -o ias
