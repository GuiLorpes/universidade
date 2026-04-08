#include <stdio.h> 

void main(void) {
    int n, j = 0;
    double soma = 0, media, maior, menor;
    printf("Quantos numeros você deseja usar?\n");
    scanf("%d", &n);
    double vet[n];
    for (int i = 0; i < n; i++) {
        printf("Defina o valor da posição %i\n", i);
        scanf("%lf", &vet[i]);
        for (int k = 0; k < i; k++) {
            if (vet[k] == vet[i]) {
                while (vet[k] == vet[i]) {
                    printf("Valor repetido! Insira outro valor!\n");
                    printf("Defina o valor da posição %i\n", i);
                    scanf("%lf", &vet[i]);
                }
            }
        }
        soma += vet[i];
    }
    media = soma / n;
    maior = menor = vet[j];
    do {
        if (vet[j] <  menor) {
            menor = vet[j];
        }
        else if (vet[j] > maior) {
            maior = vet[j];
        }
        j++;
    } while (j < n);
    printf("A média dos %d números do vetor é igual a: %.2lf\n", n, media);
    printf("O menor dos %d números do vetor é: %.2lf\n", n, menor);
    printf("O maior dos %d números do vetor é: %.2lf\n", n, maior);
}   