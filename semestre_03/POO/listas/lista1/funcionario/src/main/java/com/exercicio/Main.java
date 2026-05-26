package com.exercicio;

public class Main {
    public static void main(String[] args) {
        Funcionario lopes = new Funcionario();
        lopes.setNome("Guilherme Lopes");
        lopes.setCargo("Dev Junior");
        lopes.setSalario(1895);
        lopes.exibirFuncionario();
        lopes.aumentarSalario(0.10);
        lopes.exibirFuncionario();
    }
}