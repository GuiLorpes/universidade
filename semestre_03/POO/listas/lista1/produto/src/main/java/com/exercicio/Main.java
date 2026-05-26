package com.exercicio;

public class Main {
    public static void main(String[] args) {
        Produto monsterBranco = new Produto();
        monsterBranco.setNome("Monster Branco");
        monsterBranco.setPreco(10.95);
        Produto toddynho = new Produto();
        toddynho.setNome("Toddynho");
        toddynho.setPreco(4.75);
        monsterBranco.mostrarInformacoes();
        toddynho.mostrarInformacoes();
    }
}