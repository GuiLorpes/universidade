package com.exercicio;

public class Aluno {
    String nome;
    String matricula;
    double nota1;
    double nota2;


    public String getNome() {
        return nome;
    }
    public String getMatricula() {
        return matricula;
    }
    public double getNota1() {
        return nota1;
    }
    public double getNota2() {
        return nota2;
    }
    
    public void setNome(String nome) {
        this.nome = nome;
    }
    public void setMatricula(String matricula) {
        this.matricula = matricula;
    }
    public void setNota1(double nota) {
        this.nota1 = nota;
    }
    public void setNota2(double nota) {
        this.nota2 = nota;
    }


    public double calcularMedia() {
        return (nota1 + nota2) / 2;
    }

    public void verificarSituacao() {
        if (this.calcularMedia() >= 7.0) {
            System.out.println("Aprovado");
        }
        else {
            System.out.println("Reprovado");
        }
    }
}