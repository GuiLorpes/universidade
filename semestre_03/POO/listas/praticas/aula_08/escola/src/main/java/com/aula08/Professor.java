package com.aula08;

public class Professor extends Pessoa{
    private String materia;
    
    public Professor(String nome, int idade, String cpf, String materia) {
        super(nome, idade, cpf);
        this.materia = materia;
    }

    public String getMateria() {
        return materia;
    }
}