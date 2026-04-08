package com.aula_06;

public class Pessoa {
    private String nome;
    private String cpf;
    private int idade;
    private double altura;
    private Endereco endereco;

    public Pessoa() {}

    public Pessoa(String nome, String cpf, int idade, double altura, Endereco 
        endereco) {
        this.nome = nome;
        this.cpf = cpf;
        this.idade = idade;
        this.altura = altura;
        this.endereco = endereco;
    }

    public String getNome() {
        return this.nome;
    }
    public String getCPF() {
        return this.cpf;
    }
    public int getIdade() {
        return this.idade;
    }
    public double getAltura() {
        return this.altura;
    }
    public Endereco getEndereco() {
        return this.endereco;
    } 


    public void setNome(String n) {
        this.nome = n;
    }
    public void setCPF(String c) {
        this.cpf = c;
    }
    public void setIdade(int i) {
        this.idade = i;
    }
    public void setAltura(double altura) {
        this.altura = altura;
    }
    public void setEndereco(Endereco endereco) {
        this.endereco = endereco;
    }
    
}
