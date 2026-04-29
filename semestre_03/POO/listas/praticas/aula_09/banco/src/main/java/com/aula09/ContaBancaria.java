package com.aula09;

public abstract class ContaBancaria {
    private int id;
    private int numConta;
    private Pessoa titular;
    private double saldo;
    

    public ContaBancaria(int id, int numConta, Pessoa titular) {
        this.id = id;
        this.numConta = numConta;
        this.titular = titular;
        this.saldo = 0.0;
    }


    public int getId() {
        return id;
    }
    public int getNumConta() {
        return numConta;
    }
    public double getSaldo() {
        return saldo;
    }
    public String getTitular() {
        return titular.toString();
    }


    public void setSaldo(double saldo) {
        this.saldo = saldo;
    }


    public abstract void depositar(double valor);
    public abstract void sacar(double valor);
    public abstract void exibirTipoConta();


}