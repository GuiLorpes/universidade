package com.aula08;

public class Main {
    public static void main(String[] args) {
        Aluno guilherme = new Aluno("Guilherme Lopes", 20, "111.222.333-44", 10);
        System.out.println("Idade: " + guilherme.getIdade());
        guilherme.envelhecer();
        System.out.println("Idade: " + guilherme.getIdade());
    }
}