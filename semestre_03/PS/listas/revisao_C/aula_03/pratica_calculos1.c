#include <stdio.h>

void main(void) {
    int numeros;
    printf("Quantos numéros você deseja calcular?");
    scanf("%i", &numeros);
    int i = 0;
    float maior, menor, soma, media;
    while (i < numeros) { // soma de todos os numeros
        float num;
        printf("Insira um valor: ");
        scanf("%f", &num);
        if (i == 0) {
            maior = num;
            menor = num;
            soma = num;
        }
        else {
            if (maior < num) {
                maior = num;
            } 
            if (menor > num) {
                menor = num;
            }
            soma += num;
        }
        i++;
    }
    media = soma / numeros;
    printf("\n");
    printf("Você inseriu %i números\n", numeros);
    printf("O maior desses números é: %f\n", maior);
    printf("O menor desses números é: %f\n", menor);
    printf("A soma deles é: %f\n", soma);
    printf("A média deles é: %f\n", media);
}