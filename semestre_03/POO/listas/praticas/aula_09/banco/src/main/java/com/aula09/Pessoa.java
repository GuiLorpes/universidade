package com.aula09;

public class Pessoa {
    private String sobrenome;
    private String nome;
    private String cpf;
    private int idade;
    

    public Pessoa(String sobrenome, String nome, String cpf, int idade) {
        this.sobrenome = sobrenome;
        this.nome = nome;
        this.cpf = cpf;
        this.idade = idade;
    }


    public String getSobrenome() {
        return sobrenome;
    }
    public String getNome() {
        return nome;
    }
    public String getCpf() {
        return cpf;
    }
    public int getIdade() {
        return idade;
    }


    public void setSobrenome(String sobrenome) {
        this.sobrenome = sobrenome;
    }
    public void setNome(String nome) {
        this.nome = nome;
    }
   
}