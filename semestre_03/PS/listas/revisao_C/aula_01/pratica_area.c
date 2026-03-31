#include <stdio.h>

/* Calcule a área de um circulo de raio=2 e apresente a medida na tela, use a 
variavel auxiliar pi valendo 3.14. A formula da área é Area = pi.raio^2.*/

void main(void) {
    int raio = 2;
    float pi = 3.14, area;
    area = pi * raio * raio;
    printf("%f \n",area);
}
