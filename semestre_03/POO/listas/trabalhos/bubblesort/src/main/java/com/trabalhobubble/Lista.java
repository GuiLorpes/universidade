package com.trabalhobubble;

public class Lista {
    private int[] lista;
    
    public Lista(int[] lista) {
        this.lista = lista;
    }


    public int[] getLista() {
        return lista;
    }


    public void setLista(int[] lista) {
        this.lista = lista;
    }

    
    public void bubbleSort() { 
        for (int i = 0; i < lista.length; i++) {
            for (int j = 0; j < lista.length - i - 1; j ++) {
                if (lista[j] > lista[j+1]) {
                    int temp = lista[j];
                    lista[j] = lista[j+1];
                    lista[j+1] = temp;
                } 
            }
        }
    }
    
}