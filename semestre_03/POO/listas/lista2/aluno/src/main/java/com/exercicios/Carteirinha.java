package com.exercicios;

public class Carteirinha {
    private String numero;
    private String dataEmissao;

    
    public Carteirinha(String numero, String dataEmissao) {
        this.numero = numero;
        this.dataEmissao = dataEmissao;
    }


    public String getNumero() {
        return numero;
    }
    public String getDataEmissao() {
        return dataEmissao;
    }


    public void setDataEmissao(String dataEmissao) {
        this.dataEmissao = dataEmissao;
    }
    public void setNumero(String numero) {
        this.numero = numero;
    }
    

    public void exibirDados() {
        System.out.println("Carteirinha: " + numero);
        System.out.println("Data de emissão: " + dataEmissao);
    }
}
