#include <stdio.h>
#include <stdlib.h>

void fatorial(int n) {
    long int valor = 1;
    for (int i = n; i > 0; i--) {
        valor *= i;
    }
    printf("O fatorial de %i = %ld\n", n, valor);
}

void fibonnaci(long int *fibonacci, int n) {
    int i = 0;

    fibonacci[0] = 1;
    while (i < n - 1) {
        double aux;
        if (i == 0){
            fibonacci[1] = 1;
        }
        else {
            aux = fibonacci[i] + fibonacci[i - 1];
            fibonacci[i + 1] = aux;
        }
        i++;
    } 
}

void potencia(int x, int pot) {
    long long int resultado = x;
    for (int i = 1; i < pot; i++) {
        resultado *= x;
    }
    printf("%i^%i = %ld\n", x, pot, resultado);
}

void imprime_impares(int *vetor, int n) {
    int i = 0, j = 0;
    while (i <= n && j < (n / 2) + (n % 2))  {
        if ((i % 2) == 1) {
            vetor[j] = i;
            j++;
        }
        i++;
    }
}


void main() {
    int condicao = 0;
    do {
        printf("Insira a operação que deseja realizar:\n");
        printf("1 -> Calcular Fatorial \n2 -> Imprimir Fibonnaci \n"
        "3 -> Calcular Potencia \n4 -> Imprimir numeros primos \n5 -> Sair\n");
        scanf("%i", &condicao);
        switch (condicao) {
            case 1:
                int fat;
                printf("Insira o numero que deseja calcular o fatorial!\n");
                scanf("%i", &fat);
                fatorial(fat);
                break;
            case 2:
                int fib;
                printf("Quantos digitos da sequência de Fibonacci você deseja "
                    "ver?\n");
                scanf("%i", &fib);
                long int *vetFib = (long int *)malloc(fib * sizeof(long int));
                fibonnaci(vetFib, fib);
                for (int i = 0; i < fib; i++) {
                    printf("%ld", vetFib[i]);
                }
                free(vetFib);
                vetFib = NULL;
                break;
            case 3:
                int x, pot;
                printf("Insira qual o numero que elevar:\n");
                scanf("%i", &x);
                printf("Insira a potência que deseja usar: \n");
                scanf("%i", &pot);
                potencia(x, pot);
                break;
            case 4:
                int numImpares;
                printf("Insira até que número gostaria de ver os números impares");
                printf("\n");
                scanf("%i", &numImpares);
                int tamanhoVet = (numImpares / 2) + (numImpares % 2);
                int *vetImpares = (int *)malloc(tamanhoVet * sizeof(int));
                imprime_impares(vetImpares, numImpares);
                for (int i = 0; i < tamanhoVet; i++) {
                    printf("%i\n", vetImpares[i]);
                }
                free(vetImpares);
                vetImpares = NULL;
                break;
            case 5:
                printf("Obrigado por usar o meu código! ^^\n");
                break;
            default:
                printf("Valor inválido!\n");
                break;
        }
    } while (condicao != 5);
}
