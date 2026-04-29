#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define tamMax 100

int vet[tamMax], nElem, i, posOrd, posPost, posMenor, auxTroca, opcao;

void main(void) {

  srand(time(NULL));

  do {

    printf("\nPrograma para Ordenar Vetores por Selecao Direta\n");

    nElem=0;
    while (nElem<1){
      printf("\nDigite o Numero de Elementos dos Vetor (nao nulo) => ");
      scanf("%d",&nElem);
    }

    printf("\nGeracao Aleatoria do Vetor:\n");
    for (i=0; i<nElem-1; i++){
      vet[i]=rand()%1000;
      printf("%d, ",vet[i]);
    }
    vet[i]=rand()%1000;
    printf("%d\n",vet[i]);


    for (posOrd=0; posOrd<nElem-1; posOrd++){

       posMenor=posOrd;

       for (posPost=posOrd+1; posPost<nElem; posPost++){

           if (vet[posMenor]>vet[posPost])
               posMenor=posPost;
       }

       auxTroca=vet[posOrd];
       vet[posOrd]=vet[posMenor];
       vet[posMenor]=auxTroca;
    }

    printf("\nVetor Ordenado:\n");
    for (i=0; i<nElem-1; i++){
      printf("%d, ",vet[i]);
    }
    printf("%d\n",vet[i]);

    printf("\nDeseja Nova Execucao <1>Sim ou <2>Nao? > ");
    scanf("%d", &opcao)
    ;
  } while (opcao==1);
}