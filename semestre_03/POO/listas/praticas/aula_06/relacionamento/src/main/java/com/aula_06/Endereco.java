package com.aula_06;

public class Endereco {
    private int numCasa;
    private String rua;
    private String bairro;
    private String cep;
    private Cidade cidade;

    public Endereco(int numCasa, String rua, String bairro, String cep, 
        Cidade cidade) {
        this.numCasa = numCasa;
        this.rua = rua;
        this.bairro = bairro;
        this.cep = cep;
        this.cidade = cidade;
    }

    public int getNumCasa() {
        return this.numCasa;
    }
    public String getRua() {
        return this.rua;
    }
    public String getBairro() {
        return this.bairro;
    }
    public String getCep() {
        return this.cep;
    }
    public Cidade getCidade() {
        return this.cidade;
    }
}

