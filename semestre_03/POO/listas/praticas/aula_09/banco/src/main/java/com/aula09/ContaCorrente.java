package com.aula09;

public class ContaCorrente extends ContaBancaria{
    private double limiteConta;

    public ContaCorrente(int id, int numConta, Pessoa titular, double limiteConta) {
        super(id, numConta, titular);
        this.limiteConta = limiteConta;
    }
    
    @Override
    public void depositar(double valor) {
        this.setSaldo((this.getSaldo() + valor));
    }
    @Override
    public void sacar(double valor) {
        if (this.getSaldo() + limiteConta >= valor) {
            this.setSaldo((this.getSaldo() - valor));
            System.out.println("Saldo realizado com sucesso");
        }
        else {
            System.out.println("Saldo insuficiente");
        }
    }
    @Override
    public void exibirTipoConta() {
        System.out.println("Tipo de conta: CORRENTE");
    }
}