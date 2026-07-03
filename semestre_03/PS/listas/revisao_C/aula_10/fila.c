#include <stdio.h>
#include <stdlib.h>


typedef struct Node {
    int item;
    struct Node *proximo;      // Vai alterar diretamente o endereço
} Node;

typedef struct Fila{
    Node *inicio;
    Node *fim;
} Fila;    // Começo de uma fila é o endereço


Fila iniciaFila() {
    Fila f;
    f.inicio = NULL;
    f.fim = NULL;
    return f;
}


int ehVazia(Fila f) {
    if (f.inicio == NULL && f.fim == NULL) return 1;
    else return 0;
} 


int enfileira(Fila *f, int i) {
    Node *novoElem = malloc(sizeof(Node));
    novoElem->item = i;
    novoElem->proximo = NULL;
    if (ehVazia(*f)) {
        f->inicio = novoElem;
        f->fim = f->inicio;
    }
    else {
        f->fim->proximo = novoElem;
        f->fim = f->fim->proximo;
    }
    return 1;
}


int desenfileira(Fila *f, int *item) {
    if (ehVazia(*f)) {
        printf("Não é possivel desenfileirar!\nFila vazia");
        return 0;
    }
    Node *removido = f->inicio;
    *item = removido->item;
    f->inicio = removido->proximo;
    if (f->inicio == NULL) {
        f->fim == NULL;
    }
    free(removido);
    return 1;
}


int main() {
    Fila f = iniciaFila();
    int v[10] = {3,5,1,67,4,6,7,69,10,9};
    for (int i = 0; i < 10; i++) {
        enfileira(&f, v[i]);
    }
    printf("%i", v[0]);
    for (int i = 1; i < 10; i++) {
        printf(", %i", v[i]);
    }
    printf("\n");
    int item;
    for (int i = 11; i > 0; i--) {
        if (desenfileira(&f, &item)) printf("Item removido: %i\n", item);
    }    
    return 0;
}

