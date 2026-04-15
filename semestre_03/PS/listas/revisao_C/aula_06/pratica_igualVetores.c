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
        for (int i = 0; i < n; i++) {
            printf("Insira o valor da posição %d do vetor 2\n", (i+1));
            scanf("%d", &v2[i]);
        }
        int j = 0;
        do {
            if (!(v1[j] == v2[j])) {
                boolean = 0;
            } 
            j++;
        } while ((j < n) && (boolean == 1));
        if (boolean == 1) {
            printf("O vetor 1 e o vetor 2 são iguais!\n");
        }
        else {
            printf("O vetor 1 é diferente do vetor 2!\n");
        }
        printf("Deseja realizar a operação novamente? s/n\n");
        getchar();
        scanf("%c", &condicao);
    } while ((condicao == 'S') || (condicao == 's'));
    printf("Adeus!\n");
}