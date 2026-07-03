#include <stdio.h>
#include <stdlib.h>

FILE *arq;

void main(void){
    int i, fimDeLinha, quantValores;
    char car, linha[256];
    float num;

    printf("\nTestando Arquivos!\n\n");

    arq=fopen("matriz.txt","r");

    printf("\nTeste 1: imprimindo valor por valor ate o fim de arquivo!:\n");

    i=1;
    while (!feof(arq)){
      fscanf(arq,"%f",&num);
      printf("%f\n",num);
      i++;
    }
    fclose(arq);

    arq=fopen("matriz.txt","r");
    printf("\n\nTeste 2: imprimindo linha por linha ate o fim de arquivo!:\n");

    i=1;
    while (!feof(arq)){
      fimDeLinha=0;
      while ((!fimDeLinha)&&(!feof(arq))){
        fscanf(arq,"%f",&num);
        if (!feof(arq))
          printf("%8.2f  ",num);
        i++;

        car = fgetc(arq);

        if (car == '\n')
              fimDeLinha=1;
      }
      printf("\n");
    }
    fclose(arq);

    arq=fopen("matriz.txt","r");
    printf("\n\nTeste 3: imprimindo partes das linhas ate o fim de arquivo!:\n");

    i=1;
    while (!feof(arq)){
      quantValores=0;
      while ((quantValores<3)&&(!feof(arq))){
        fscanf(arq,"%f",&num);
        if (!feof(arq))
          printf("%8.2f  ",num);
        i++;
        quantValores++;
        if (quantValores==3)
            fgets(linha,256,arq);
      }
      printf("\n");
    }
    fclose(arq);
}
