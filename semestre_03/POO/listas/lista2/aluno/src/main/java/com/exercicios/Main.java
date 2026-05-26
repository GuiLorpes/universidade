package com.exercicios;

public class Main {
    public static void main(String[] args) {
        Carteirinha cGi = new Carteirinha("143844", "03/04/2025");
        Aluno giovana = new Aluno("Giovana", "Ciencia da Computação", cGi);
        giovana.exibirDados();
    }
}