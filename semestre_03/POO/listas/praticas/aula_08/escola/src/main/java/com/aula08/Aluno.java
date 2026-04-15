package com.aula08;

public class Aluno extends Pessoa {
    private int nota;

    public Aluno(String nome, int idade, String cpf, int nota) {
        super(nome, idade, cpf);
        this.nota = nota;
    }

    public int getNota() {
        return nota;
    }
    
    @Override
    public void envelhecer() {
        this.idade = idade + 2; 
    }
}