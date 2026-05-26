package com.trabalhobubble;

import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        int[] numeros = {3,5,1,6,9,2,12,32,6,8,9,0,7};
        Lista listaNum = new Lista(numeros);

        System.out.println(Arrays.toString(listaNum.getLista()));
        listaNum.bubbleSort();
        System.out.println(Arrays.toString(listaNum.getLista()));
    }
}