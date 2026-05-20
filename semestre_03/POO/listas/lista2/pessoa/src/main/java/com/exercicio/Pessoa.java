package com.exercicio;

public class Pessoa extends CPF {
    private String nome;
    private int idade;
    private CPF cpf;


    public Pessoa(String nome, int idade, String numero, Situacao situacao) {
        super(numero, situacao);
        this.nome = nome;
        this.idade = idade;
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

}
