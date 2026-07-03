#include <stdio.h>

void ex1(void) {
    int a = 14, b = 3, c = 18, d = 22;
    int mediaAritmeticaInteira = (a + b + c + d) / 4;
    float mediaAritmeticaReal = (a + b + c + d) / 4.0;
    printf("%i\n", mediaAritmeticaInteira);
    printf("%.2f\n", mediaAritmeticaReal);
}

void ex2(void) {
    int produtos = 333, caixas = 12;
    int resultado = produtos / caixas;
    int sobra = produtos % caixas;
    printf("%i\n%i\n", resultado, sobra);   
}


void ex3() {
    int a, b, resultado;
    printf("Insira o valor de a: ");
    scanf("%i", &a);
    printf("Insira o valor de b: ");
    scanf("%i", &b);
    resultado = (a + b) % 360;
    printf("%i\n", resultado);
}

void ex4() {
    
}



int main(void) {
    ex1();
    ex2();
    ex3();
}