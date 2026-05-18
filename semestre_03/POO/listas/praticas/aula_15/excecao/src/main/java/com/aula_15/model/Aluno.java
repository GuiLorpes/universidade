package com.aula_15.model;

public class Aluno {
    private String name;
    private double nota;


    public Aluno(String name, double nota) {
        this.name = name;
        this.nota = nota;
    }


    public String getName() {
        return name;
    }
    public double getNota() {
        return nota;
    }
}
