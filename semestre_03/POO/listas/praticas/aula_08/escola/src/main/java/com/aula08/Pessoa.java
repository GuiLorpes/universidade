package com.aula08;

public class Pessoa {
    private String nome;
    protected int idade;
    private String cpf;

    public Pessoa(String nome, int idade, String cpf) {
        this.nome = nome;
        this.idade = idade;
        this.cpf = cpf;
    }

    public String getNome() {
        return nome;
    } 
    public int getIdade() {
        return idade;
    }
    public String getCPF() {
        return cpf;
    }

    public void envelhecer() {
        idade++;
    }
}