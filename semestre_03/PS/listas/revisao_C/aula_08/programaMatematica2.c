#include <stdio.h>

long int fatorial(int n) {
    long int valor = 1;
    for (int i = n; i > 0; i--) {
        valor *= i;
    }
    printf("%ld", valor);
}

void fibonnaci(int fibonacci, int n) {
    int i = 1;
    long long int fibonacci[n];
    fibonacci[0] = 1;
    do {
        double aux;
        if (i == 1){
            fibonacci[1] = 1;
        }
        else {
            aux = fibonacci[i - 1] + fibonacci[i];
            fibonacci[i + 1] = aux;
        }
        i++;
    } while (i < n - 1);
}

long long int potencia(int x, int pot) {
    long long int resultado = x;
    for (int i = 1; i < pot; i++) {
        resultado *= x;
    }
    printf(resultado);
}

void imprime_impares(int *vetor, int n) {
    int i = 0, j = 0;
    while (i < n && j < sizeof(vetor))  {
        if (i % 2 == 1) {
            vetor[j] = n;
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
            long int r = fatorial(fat);
            printf("O fatorial de %i = %ld\n", fat, r);
            break;
        case 2:
            int fib;
            printf("Quantos digitos da sequência de Fibonacci você deseja "
                "ver?\n");
            scanf("%i", &fib);
            long long int fibo[fib] = fibonnaci(fib);
            for (int i = 0; i < fib; i++) {
                printf("%lld", fibo[i]);
            }
            
        case 3:
            int x, pot;
            printf("Insira qual o numero que elevar:\n");
            scanf("%i", &x);
            printf("Insira a potência que deseja usar: \n");
            scanf("%i", &pot);
            long long int resultado = potencia(x, pot);
            printf("%i^%i = %lld\n", x, pot, resultado);
            break;
        case 4:
            int numImpares;
            printf("Insira até que número gostaria de ver os números impares");
            printf("\n");
            scanf("%i", &impares);
            int vetImpares[numImpares / 2];
            imprime_impares(vetImpares, numImpares);
            for (int i = 0; i < numImpares; i++) {
                printf("%i\n", vetImpares[i]);
            }
            break;
        case 5:
            printf("Obrigado por usar o meu código! ^^\n");
            break;
        }
    } while (condicao != 5);
}
