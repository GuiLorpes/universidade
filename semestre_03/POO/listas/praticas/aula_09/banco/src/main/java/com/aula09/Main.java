package com.aula09;

public class Main {
    public static void main(String[] args) {
        Pessoa p = new Pessoa("Fulano", "Ciclano", "123-432-325-14", 25);
        ContaCorrente cc = new ContaCorrente(43, 42334, p, 4327.00);
        cc.exibirTipoConta();
        System.out.println(cc.getSaldo());
        cc.sacar(12);
        System.out.println(cc.getSaldo());
        cc.depositar(3289);
        System.out.println(cc.getSaldo());
        cc.sacar(437);
        System.out.println(cc.getSaldo());
        cc.sacar(45378);
        System.out.println(cc.getSaldo());
    }
}