package com.exercicio;

public class Main {
    public static void main(String[] args) {
        CPF cpfGui = new CPF("111.222.333-44", Situacao.REGULAR);
        Pessoa gui = new Pessoa("Guilherme", 20, cpfGui);
        gui.exibirDados();
        CPF cpfShiShi = new CPF("222.333.444-67", Situacao.CANCELADO);
        Pessoa shimano = new Pessoa("Shimano", 19, cpfShiShi);
        shimano.exibirDados();
    }
}