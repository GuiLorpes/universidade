#include <stdio.h>

/* Escolha alguma temperatura em graus Celsius e atribua à variavel tempC. 
Apresente-a convertida em Fahrenheit, usando a fórmula de coneversão 
tempF = (9 * tempC + 160) / 5.*/

void main(void) {
    float tempC = 47.8, tempF;
    tempF = (9 * tempC + 160) / 5;
    printf("%f \n", tempF);
}