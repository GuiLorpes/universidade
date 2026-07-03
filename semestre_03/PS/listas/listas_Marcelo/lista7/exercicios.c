#include <stdio.h>
#include <string.h>

void ex_1() {
    char c = 'x';
    float f = 1.23;
    int i = 4567;

    char *ptr_c = &c;
    float *ptr_f = &f;
    int *ptr_i = &i;

    printf("%c\n%.2f\n%i\n", *ptr_c, *ptr_f, *ptr_i);
}

void ex_2() {
    char *lista[] = {"jfd", "kj", "usjkfhcs", "nbxh", "yt", "muoi", "x", "rhd"};
    char *maiorStr = NULL;
    int maiorTamanho = 0;
    for (int i = 0; i < 8; i++) {
        if (strlen(lista[i]) > maiorTamanho) {
            maiorTamanho = strlen(lista[i]);
            maiorStr = lista[i];
        }
    }
    printf("%s\n", maiorStr);
}

int main() {
    ex_1();
    ex_2();

    return 0;
}

