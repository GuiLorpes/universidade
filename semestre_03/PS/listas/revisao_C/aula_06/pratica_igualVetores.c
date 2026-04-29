#include <stdio.h>

int n, boolean = 1, TAM_MAX = 15;

void main(void) {
    char condicao;
    do {
        printf("Qual o tamanho dos seus vetores: \n");
        scanf("%d", &n);
        while (n > TAM_MAX) {
            printf("Tamanho do vetor ultrapassou o tamanho máximo de %d, insira \
um valor menor\n", TAM_MAX);
            printf("Qual o tamanho dos seus vetores: \n");
            scanf("%d", &n);
        }
        int v1[n], v2[n];
        for (int i = 0; i < n; i++) {
            printf("Insira o valor da posição %d do vetor 1\n", (i+1));
            scanf("%d", &v1[i]);
        }
        printf("\n");
        for (int i = 0; i < n; i++) {
            printf("Insira o valor da posição %d do vetor 2\n", (i+1));
            scanf("%d", &v2[i]);
        }
        int iguais = 0;
        for (int i = 0; i < n; i++) {
            int j = 0, achou = 0;
            while ((j < n) && (achou != 1)) {
                if (v1[i] == v2[j]) {
                    achou = 1;
                    iguais++;
                }
                j++;
            }
        }
        for (int i = 0; i < n; i++) {
            int j = 0, achou = 0;
            while ((j < n) && (achou != 1)) {
                if (v2[i] == v1[j]) {
                    achou = 1;
                    iguais++;
                }
                j++;
            }
        }
        if (iguais == (2*n)) {
            printf("Os vetores 1 e 2 possuem os mesmos elementos!\n");
        }
        else {
            printf("Os vetores 1 e 2 não possuem os mesmos elementos!\n");
        }
        printf("Deseja realizar a operação novamente? s/n\n");
        getchar();
        scanf("%c", &condicao);
    } while ((condicao == 'S') || (condicao == 's'));
    printf("Adeus!\n");
}