#include <stdio.h>

void main(void) {
    int dig_fib, i = 0;
    long long int fibonacci = 1, num_anterior = 0;
    printf("Quantos digitos da sequência de Fibonacci você deseja ver? ");
    scanf("%i", &dig_fib);
    while (i < dig_fib) {
        double aux;
        if (i == 0){
            fibonacci += num_anterior;
        }
        else {
            aux = fibonacci;
            fibonacci += num_anterior;
        }
        printf("%lld\n", fibonacci);
        num_anterior = aux;
        i++;
    }
}