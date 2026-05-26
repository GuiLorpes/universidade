package com.exercicio;

public class Endereco {
    private String rua;
    private int numero;
    private String bairro;
    private String cidade;


    public Endereco(String rua, int numero, String bairro, String cidade) {
        this.rua = rua;
        this.numero = numero;
        this.bairro = bairro;
        this.cidade = cidade;
    }
    
    
    public String getRua() {
        return rua;
    }
    public int getNumero() {
        return numero;
    }
    public String getBairro() {
        return bairro;
    }
    public String getCidade() {
        return cidade;
    }
    
    
    public void setRua(String rua) {
        this.rua = rua;
    }
    public void setNumero(int numero) {
        this.numero = numero;
    }
    public void setBairro(String bairro) {
        this.bairro = bairro;
    }
    public void setCidade(String cidade) {
        this.cidade = cidade;
    }


    public void exibirDados() {
        System.out.println("Rua: " + rua);
        System.out.println("Número: " + numero);
        System.out.println("Bairro: " + bairro);
        System.out.println("Cidade: " + cidade);
    }
}
