#include <stdio.h>

long int fatorial(int n) {
    int valor = 1;
    for (int i = n; i > 0; i--) {
        valor *= i;
    }
    return valor;
}

int fibonnaci()


void main() {
    int condicao = 0;
    do {
        printf("Insira a operação que deseja realizar:\n");
        printf("1 -> Calcular Fatorial \n2 -> Imprimir Fibonnaci \n");
        printf("3 -> Calcular Potencia \n 4 -> Imprimir numeros primos \n5 -> Sair");
        scanf("%i", &condicao);
        switch (condicao)
        {
        case 1:
            int n;
            printf("Insira o numero que deseja calcular o fatorial!");
            scanf("%i", &n);
            resultado = fatorial(n);
            printf("O fatorial de %i = %ld", n, resultado);
        case 2:

        case 3:

        case 4:

        case 5:
            printf("Obrigado por usar o meu código! ^^");
        default:
            printf("Número inserido é inválido!");
        } 
    } while (condicao != 5);
}