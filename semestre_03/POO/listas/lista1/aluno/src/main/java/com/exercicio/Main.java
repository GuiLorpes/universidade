package com.exercicio;

public class Main {
    public static void main(String[] args) {
        Aluno jose = new Aluno();
        jose.setNome("jose");
        jose.setMatricula("676767");
        jose.setNota1(2.4);
        jose.setNota2(6.2);
        System.out.println(jose.calcularMedia());
        jose.verificarSituacao();

        Aluno guilherme = new Aluno();
        guilherme.setNome("guilherme");
        guilherme.setMatricula("143630");
        guilherme.setNota1(9.2);
        guilherme.setNota2(6.1);
        System.out.println(guilherme.calcularMedia());
        guilherme.verificarSituacao();
    }
}