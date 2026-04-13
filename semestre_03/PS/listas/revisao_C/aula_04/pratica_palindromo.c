#include <stdio.h>

void main(void) {
    int n, ehPalindromo = 1;
    printf("Insira a quantia de caracteres que deseja fornecer: \n");
    scanf("%i", &n);
    char string[n];
    printf("Insira a sequência que deseja: \n");
    getchar();
    scanf("%c", &string[n]);
    int i = 0, j = n-1;
    while ((i < j) && (ehPalindromo == 1)) {
        if (!(string[i] == string[j])) {
            ehPalindromo = 0;
        }
        else {
            i++;
            j--;
        }
    } 
    if (ehPalindromo == 1) {
        printf("%s é palindromo", string);
    }
    else {
        printf("%s não é palindromo", string);
    }
}