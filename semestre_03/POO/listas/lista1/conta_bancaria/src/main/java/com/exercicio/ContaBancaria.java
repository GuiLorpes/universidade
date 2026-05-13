package com.exercicio;

public class ContaBancaria {
    private String numero;
    private String titular;
    private double saldo;


    public String getNumero() {
        return numero;
    }
    public String getTitular() {
        return titular;
    }
    public double getSaldo() {
        return saldo;
    }

    public void setNumero(String numero) {
        this.numero = numero;
    }
    public void setSaldo(double saldo) {
        this.saldo = saldo;
    }
    public void setTitular(String titular) {
        this.titular = titular;
    }


    public void depositar(double valor) {
        this.saldo += valor;
    }

    public boolean sacar(double valor) {
        if (valor > saldo) {
            System.err.println("Saldo insuficiente!");
            return false;
        }
        else {
            this.saldo -= valor;
            System.out.println("Saque realizado com sucesso!");
            return true;
        }
    }

    public void consultarSaldo() {
        System.out.println("Saldo disponivel:" + this.saldo);
    }
}
