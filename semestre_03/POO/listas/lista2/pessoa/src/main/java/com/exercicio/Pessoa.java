package com.exercicio;

public class Pessoa {
    private String nome;
    private int idade;
    private CPF cpf;


    public Pessoa(String nome, int idade, CPF cpf) {
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
    public CPF getCpf() {
        return cpf;
    }


    public void exibirDados() {
        System.out.println("Nome: " + this.getNome());
        System.out.println("Idade: " + this.getIdade());
        this.cpf.exibirDados();
    }
    
}
