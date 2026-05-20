package com.exercicio;

public class CPF {
    private String numero;
    private Situacao situacao;

    
    public CPF(String numero, Situacao situacao) {
        this.numero = numero;
        this.situacao = situacao;
    }


    public String getNumero() {
        return numero;
    }
    public Situacao getSituacao() {
        return situacao;
    }

    public void setNumero(String numero) {
        this.numero = numero;
    }
    public void setSituacao(Situacao situacao) {
        this.situacao = situacao;
    }
    
    
    public void exibirDados() {
        System.out.println("CPF: " + situacao);
    }
}
