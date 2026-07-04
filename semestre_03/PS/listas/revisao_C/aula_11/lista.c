// Vídeo apresentação: https://drive.google.com/file/d/1IJu79qmIUNaKqjg_pvgKj0YUL_DhEAH9/view?usp=sharing

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

typedef struct Tipo1 {
    char *cpf;
    char *rg;
    char *nome;
    int idade;
    char *numCelular;
    char *profissao;
} Tipo1;


typedef struct Tipo2 {
    char *nome;
    char *cpf;
    char *cep;
    char *rua;
    char *bairro;
} Tipo2;


typedef struct Tipo3 {
    char *empresa;
    char *nomeProprio;
    char *nomeMae;
    char *nomePai;
    char *cpf;
    float salario;
} Tipo3;


typedef struct Node {
    struct Node *ante;
    void *dado;
    struct Node *prox; 
    int tipoDado; 
} Node; 


typedef struct Lista {
    Node *inicio;
    Node *fim;
    int quantidadeElem; 
} Lista;


Lista iniciaLista() {
    Lista l;
    l.inicio = NULL;
    l.fim = NULL;
    l.quantidadeElem = 0;
    return l;
}

// Verifica se l é uma lista vazia
int ehVazia(Lista l) {
    if (l.inicio == NULL && l.fim == NULL) return 1;
    else return 0;
}

// Verifica o tipo de dado de um elemento e retorna seu CPF
char* getCPF(void *dado, int tipoDado) {
    switch (tipoDado) {
        case 1: return ((Tipo1 *)dado)->cpf;
        case 2: return ((Tipo2 *)dado)->cpf;
        case 3: return ((Tipo3 *)dado)->cpf;
    }
    return NULL;
}

void liberaDado(void *dado, int tipoDado) {
    if (dado == NULL) return;

    switch (tipoDado) {
        case 1: {
            Tipo1 *t = (Tipo1 *)dado;
            free(t->cpf);
            free(t->rg);
            free(t->nome);
            free(t->numCelular);
            free(t->profissao);
            free(t);
            break;
        }
        case 2: {
            Tipo2 *t = (Tipo2 *)dado;
            free(t->nome);
            free(t->cpf);
            free(t->cep);
            free(t->rua);
            free(t->bairro);
            free(t);
            break;
        }
        case 3: {
            Tipo3 *t = (Tipo3 *)dado;
            free(t->empresa);
            free(t->nomeProprio);
            free(t->nomeMae);
            free(t->nomePai);
            free(t->cpf);
            free(t);
            break;
        }
    }
}

void exibeLista(Lista l) {
    printf("["); 
    Node *p = l.inicio;
    if (p==NULL) printf("\n{}");
    while (p != NULL) {
        switch (p->tipoDado) {
            case 1:
                Tipo1 *dado1 = (Tipo1 *)p->dado;
                printf("\n{\n");
                printf("CPF: %sRG: %sNome: %sIdade: %i\nNúmero de celular: %s"
                    "Profissão: %s", 
                dado1->cpf, dado1->rg, dado1->nome, dado1->idade, 
                dado1->numCelular, dado1->profissao);
                printf("}");
                break;
            case 2:
                Tipo2 *dado2 = (Tipo2 *)p->dado;
                printf("\n{\n");
                printf("Nome: %sCPF: %sCEP: %sRua: %sBairro: %s", 
                dado2->nome, dado2->cpf, dado2->cep, dado2->rua, dado2->bairro);
                printf("}");
                break;
            case 3:
                Tipo3 *dado3 = (Tipo3 *)p->dado;
                printf("\n{\n");
                printf("Empresa: %sNome: %sNome mãe: %sNome pai: %sCPF: %s"
                    "Salário: %.2f R$\n", 
                dado3->empresa, dado3->nomeProprio, dado3->nomeMae, 
                dado3->nomePai, dado3->cpf, dado3->salario);
                printf("}");
                break;
            default:
                break;
        }
        if (p == l.fim) {
            p = p->prox; 
        }
        else {
            printf(",");
            p = p->prox;
        }
    }
    
    printf("\n]\n");
}


int insereElementoOrdenado(Lista *l, int tipoDado) {
    Node *novoItem = (Node *)malloc(sizeof(Node));
    novoItem->tipoDado = tipoDado;
    novoItem->ante = NULL;
    novoItem->prox = NULL;

    printf("Insira seus dados:\n");
    getchar();
    
    switch (tipoDado) {
        case 1:
            Tipo1 *dado1 = (Tipo1 *)malloc(sizeof(Tipo1));
            dado1->cpf = (char *)malloc(20);
            dado1->rg = (char *)malloc(16);
            dado1->nome = (char *)malloc(256);
            dado1->numCelular = (char *)malloc(24);
            dado1->profissao = (char *)malloc(256);
            
            printf("CPF -> ");
            fgets(dado1->cpf, 20, stdin);
            printf("RG -> ");
            fgets(dado1->rg, 16, stdin);
            printf("Nome -> ");
            fgets(dado1->nome, 256, stdin);            
            printf("Idade -> ");
            scanf("%i", &dado1->idade);
            getchar();
            printf("Número de celular -> ");
            fgets(dado1->numCelular, 24, stdin);
            printf("Profissão -> ");
            fgets(dado1->profissao, 256, stdin);

            novoItem->dado = (void *)dado1;
            break;
        
        case 2:
            Tipo2 *dado2 = (Tipo2 *)malloc(sizeof(Tipo2));
            dado2->nome = (char *)malloc(256);
            dado2->cpf = (char *)malloc(20);
            dado2->cep = (char *)malloc(15);
            dado2->bairro = (char *)malloc(256);
            dado2->rua = (char *)malloc(256);

            printf("Nome -> ");
            fgets(dado2->nome, 256, stdin);
            printf("CPF -> ");
            fgets(dado2->cpf, 20, stdin);
            printf("CEP -> ");
            fgets(dado2->cep, 15, stdin);
            printf("Rua -> ");
            fgets(dado2->rua, 256, stdin);
            printf("Bairro -> ");
            fgets(dado2->bairro, 256, stdin);

            novoItem->dado = (void *)dado2;
            break;
        
        case 3:
            Tipo3 *dado3 = (Tipo3 *)malloc(sizeof(Tipo3));
            dado3->empresa = (char *)malloc(256);
            dado3->nomeProprio = (char *)malloc(256);
            dado3->nomeMae = (char *)malloc(256);
            dado3->nomePai = (char *)malloc(256);
            dado3->cpf = (char *)malloc(20); 
            
            printf("Empresa -> ");
            fgets(dado3->empresa, 256, stdin);
            printf("Nome -> ");
            fgets(dado3->nomeProprio, 256, stdin);
            printf("Nome da mãe -> ");
            fgets(dado3->nomeMae, 256, stdin);
            printf("Nome do pai -> ");
            fgets(dado3->nomePai, 256, stdin);
            printf("CPF -> ");
            fgets(dado3->cpf, 20, stdin);
            printf("Salário -> ");
            scanf("%f", &dado3->salario);

            novoItem->dado = (void *)dado3;
            break;

        default:
            printf("Tipo de dado inválido!\n");
            return 0;
    }
    // Caso a lista for vazia, inicio é igual ao fim
    if (ehVazia(*l)) {
         l->inicio = novoItem;
         l->fim = novoItem;
         return 1;
    }

    Node *q = l->inicio;

    int comparaCPF = strcmp(getCPF(q->dado, q->tipoDado), 
    getCPF(novoItem->dado, novoItem->tipoDado));

    while (q != NULL && comparaCPF < 0) {
        q = q->prox;
        if (q != NULL) {
            comparaCPF = strcmp(getCPF(q->dado, q->tipoDado), 
            getCPF(novoItem->dado, novoItem->tipoDado));
        }
    }

    if (q != NULL && comparaCPF == 0) {
        printf("CPF já registrado!\n");
        switch (novoItem->tipoDado) {
            case 1: {
                Tipo1 *t = (Tipo1 *)novoItem->dado;
                free(t->cpf);
                free(t->rg);
                free(t->nome);
                free(t->numCelular);
                free(t->profissao);
                free(t);
                break;
            }
            case 2: {
                Tipo2 *t = (Tipo2 *)novoItem->dado;
                free(t->nome);
                free(t->cpf);
                free(t->cep);
                free(t->rua);
                free(t->bairro);
                free(t);
                break;
            }
            case 3: {
                Tipo3 *t = (Tipo3 *)novoItem->dado;
                free(t->empresa);
                free(t->nomeProprio);
                free(t->nomeMae);
                free(t->nomePai);
                free(t->cpf);
                free(t);
                break;
            }
        }
        free(novoItem);
        return 0;
    }

    if (q == NULL) {
        novoItem->ante = l->fim;
        l->fim->prox = novoItem;
        l->fim = novoItem;
    } else if (q == l->inicio) {
        novoItem->prox = q;
        q->ante = novoItem;
        l->inicio = novoItem;
    } else {
        novoItem->prox = q;
        novoItem->ante = q->ante;
        q->ante->prox = novoItem;
        q->ante = novoItem;
    }

    l->quantidadeElem++;
    return 1;
}


int removeElemento(Lista *l, char *cpf) {
    Node *q = l->inicio;

    if (ehVazia(*l)) {
        printf("Lista vazia! \n"); 
        return 0;
    }
    
    int comparaCPF = strcmp(getCPF(q->dado, q->tipoDado), cpf);

    while (q != NULL) {
        if (comparaCPF == 0) {
            // Encontrou o elemento
            if (q == l->inicio && q == l->fim) {
                // Único elemento
                l->inicio = NULL;
                l->fim = NULL;
            } else if (q == l->inicio) {
                // Primeiro elemento
                l->inicio = q->prox;
                l->inicio->ante = NULL;
            } else if (q == l->fim) {
                // Último elemento
                l->fim = q->ante;
                l->fim->prox = NULL;
            } else {
                // Elemento no meio
                q->ante->prox = q->prox;
                q->prox->ante = q->ante;
            }
            
            // Libera memória
            liberaDado(q->dado, q->tipoDado);
            free(q);
            l->quantidadeElem--;
            return 1;
        }
        q = q->prox;
        if (q != NULL) comparaCPF = strcmp(getCPF(q->dado, q->tipoDado), cpf);
    }
    printf("CPF não encontrado!\n");
    return 0;
}

int editarElemento(Lista *l, char *cpf) {
    Node *q = l->inicio;

    if (ehVazia(*l)) {
        printf("Lista vazia!\n");
        return 0;
    }

    int comparaCPF = strcmp(getCPF(q->dado, q->tipoDado), cpf);
    
    while (q != NULL) {
        if (comparaCPF == 0) {
            int tipoAtual = q->tipoDado;
            int novoTipo;
            printf("Editando elemento com CPF: %s\n", cpf);
            printf("Qual tipo deseja usar? | 1 | 2 | 3 |\n");
            scanf("%i", &novoTipo);
            getchar();
            while (novoTipo != 1 && novoTipo != 2 && novoTipo != 3) {
                printf("Tipo inserido inválido! Tipos válidos: | 1 | 2 | 3 |\n");
                printf("Qual tipo deseja usar? | 1 | 2 | 3 |\n");
                scanf("%i", &novoTipo);
                getchar();
            }

            if (novoTipo != tipoAtual) {
                void *novoDado = NULL;

                switch (novoTipo) {
                    case 1: {
                        Tipo1 *dado = (Tipo1 *)malloc(sizeof(Tipo1));
                        dado->cpf = (char *)malloc(20);
                        dado->rg = (char *)malloc(16);
                        dado->nome = (char *)malloc(256);
                        dado->numCelular = (char *)malloc(24);
                        dado->profissao = (char *)malloc(256);

                        if (tipoAtual == 2) {
                            Tipo2 *antigo = (Tipo2 *)q->dado;
                            strcpy(dado->cpf, antigo->cpf);
                        } else if (tipoAtual == 3) {
                            Tipo3 *antigo = (Tipo3 *)q->dado;
                            strcpy(dado->cpf, antigo->cpf);
                        } else {
                            Tipo1 *antigo = (Tipo1 *)q->dado;
                            strcpy(dado->cpf, antigo->cpf);
                        }

                        printf("RG -> ");
                        fgets(dado->rg, 16, stdin);
                        printf("Nome -> ");
                        fgets(dado->nome, 256, stdin);
                        printf("Idade -> ");
                        scanf("%i", &dado->idade);
                        getchar();
                        printf("Número de celular -> ");
                        fgets(dado->numCelular, 24, stdin);
                        printf("Profissão -> ");
                        fgets(dado->profissao, 256, stdin);

                        novoDado = (void *)dado;
                        break;
                    }
                    case 2: {
                        Tipo2 *dado = (Tipo2 *)malloc(sizeof(Tipo2));
                        dado->nome = (char *)malloc(256);
                        dado->cpf = (char *)malloc(20);
                        dado->cep = (char *)malloc(15);
                        dado->bairro = (char *)malloc(256);
                        dado->rua = (char *)malloc(256);

                        if (tipoAtual == 1) {
                            Tipo1 *antigo = (Tipo1 *)q->dado;
                            strcpy(dado->cpf, antigo->cpf);
                        } else if (tipoAtual == 3) {
                            Tipo3 *antigo = (Tipo3 *)q->dado;
                            strcpy(dado->cpf, antigo->cpf);
                        } else {
                            Tipo2 *antigo = (Tipo2 *)q->dado;
                            strcpy(dado->cpf, antigo->cpf);
                        }

                        printf("Nome -> ");
                        fgets(dado->nome, 256, stdin);
                        printf("CEP -> ");
                        fgets(dado->cep, 15, stdin);
                        printf("Rua -> ");
                        fgets(dado->rua, 256, stdin);
                        printf("Bairro -> ");
                        fgets(dado->bairro, 256, stdin);

                        novoDado = (void *)dado;
                        break;
                    }
                    case 3: {
                        Tipo3 *dado = (Tipo3 *)malloc(sizeof(Tipo3));
                        dado->empresa = (char *)malloc(256);
                        dado->nomeProprio = (char *)malloc(256);
                        dado->nomeMae = (char *)malloc(256);
                        dado->nomePai = (char *)malloc(256);
                        dado->cpf = (char *)malloc(20);

                        if (tipoAtual == 1) {
                            Tipo1 *antigo = (Tipo1 *)q->dado;
                            strcpy(dado->cpf, antigo->cpf);
                        } else if (tipoAtual == 2) {
                            Tipo2 *antigo = (Tipo2 *)q->dado;
                            strcpy(dado->cpf, antigo->cpf);
                        } else {
                            Tipo3 *antigo = (Tipo3 *)q->dado;
                            strcpy(dado->cpf, antigo->cpf);
                        }

                        printf("Empresa -> ");
                        fgets(dado->empresa, 256, stdin);
                        printf("Nome -> ");
                        fgets(dado->nomeProprio, 256, stdin);
                        printf("Nome da mãe -> ");
                        fgets(dado->nomeMae, 256, stdin);
                        printf("Nome do pai -> ");
                        fgets(dado->nomePai, 256, stdin);
                        printf("Salário -> ");
                        scanf("%f", &dado->salario);
                        getchar();

                        novoDado = (void *)dado;
                        break;
                    }
                }

                liberaDado(q->dado, tipoAtual);
                q->dado = novoDado;
                q->tipoDado = novoTipo;
            } else {
                switch (tipoAtual) {
                    case 1: {
                        Tipo1 *dado = (Tipo1 *)q->dado;
                        printf("RG -> ");
                        fgets(dado->rg, 16, stdin);
                        printf("Nome -> ");
                        fgets(dado->nome, 256, stdin);
                        printf("Idade -> ");
                        scanf("%i", &dado->idade);
                        getchar();
                        printf("Número de celular -> ");
                        fgets(dado->numCelular, 24, stdin);
                        printf("Profissão -> ");
                        fgets(dado->profissao, 256, stdin);
                        break;
                    }
                    case 2: {
                        Tipo2 *dado = (Tipo2 *)q->dado;
                        printf("Nome -> ");
                        fgets(dado->nome, 256, stdin);
                        printf("CEP -> ");
                        fgets(dado->cep, 15, stdin);
                        printf("Rua -> ");
                        fgets(dado->rua, 256, stdin);
                        printf("Bairro -> ");
                        fgets(dado->bairro, 256, stdin);
                        break;
                    }
                    case 3: {
                        Tipo3 *dado = (Tipo3 *)q->dado;
                        printf("Empresa -> ");
                        fgets(dado->empresa, 256, stdin);
                        printf("Nome -> ");
                        fgets(dado->nomeProprio, 256, stdin);
                        printf("Nome da mãe -> ");
                        fgets(dado->nomeMae, 256, stdin);
                        printf("Nome do pai -> ");
                        fgets(dado->nomePai, 256, stdin);
                        printf("Salário -> ");
                        scanf("%f", &dado->salario);
                        getchar();
                        break;
                    }
                }
            }
            return 1;
        }
        q = q->prox;
        if (q != NULL) comparaCPF = strcmp(getCPF(q->dado, q->tipoDado), cpf);
    }
    printf("CPF não encontrado!\n");
    return 0;
}


int main() {
    Lista l = iniciaLista();
    printf("BEM VINDO A MINHA LISTA\n");
    
    int op = 0;
    do {
        printf("QUAL OPERAÇÃO DESEJA REALIZAR?\n1 -> INSERIR\n2 -> REMOVER\n");
        printf("3 -> EDITAR\n4 -> VER LISTA\n0 -> SAIR\n");
        scanf("%i", &op);
        getchar();
        switch (op) {
            case 1:
                int tipoDado;
                printf("QUAL TIPO DE DADO DESEJA INSERIR? | 1 | 2 | 3 |\n");
                scanf("%i", &tipoDado);
                if (insereElementoOrdenado(&l, tipoDado)) {
                    printf("ELEMENTO INSERIDO COM SUCESSO!\n");
                }
                else {
                    printf("ELEMENTO NÃO INSERIDO!\n");
                }
                break;
            
            case 2: 
                char cpfRemover[20];
                printf("DIGITE O CPF QUE DESEJA REMOVER: \n");
                fgets(cpfRemover, 20, stdin);
                if (removeElemento(&l, cpfRemover)) {
                    printf("ELEMENTO REMOVIDO!\n");
                }
                break;
            
            
            case 3: 
                char cpfEditar[20];
                printf("DIGITE O CPF QUE DESEJA EDITAR: \n");
                fgets(cpfEditar, 20, stdin);
                if (editarElemento(&l, cpfEditar)) {
                    printf("ELEMENTO ATUALIZADO!\n");
                }
                break;
            
            
            case 4:
                exibeLista(l);
                break; 

            case 0:
                break;

            default:
                printf("INSIRA UM VALOR VÁLIDO!\n");
                break;
        }
    } while (op != 0);
    printf("ADEUS!\n");
    return 0;
}

