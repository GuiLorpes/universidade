#include <stdio.h>
#include <stdlib.h>

int myStrlen(char *c) {
    int i = 0;
    while (*c != '\0') {
        c++;
        i++;
    }
    return i;
}

void myStrcpy(char *c, char *copy) {
    while (*c != '\0') {
        *copy = *c;
        c++;
        copy++;
    }
    *copy = '\0';
}

int myStrcmp(char *p1, char *p2) {
    while (*p1 != '\0' && *p2 != '\0') {}
    return 0;
}

int main() {
    char palavra1[256], palavra2[256];
    printf("Insira a palavra 1: \n");
    fgets(palavra1, sizeof(palavra1), stdin);
    printf("Insira a palavra 2: \n");
    fgets(palavra1, sizeof(palavra2), stdin);
    
    printf("Tamanho da palavra 1: %i\n", myStrlen(palavra1));

    char copia[256];
    myStrcpy(palavra2, copia);
    printf("Copia da palavra 2: %s\n", copia);




    return 0;
}