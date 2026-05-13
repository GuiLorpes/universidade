package com.exercicio;

public class Main {
    public static void main(String[] args) {
        ContaBancaria conta = new ContaBancaria();
        conta.setNumero("123");
        conta.setTitular("guilherme");
        conta.setSaldo(0);
        conta.depositar(45.8);
        conta.consultarSaldo();
        conta.sacar(51.2);
        conta.sacar(3);
        conta.consultarSaldo();
    }
}