package com.exercicios;

public class Aluno {
    private String nome;
    private String curso;
    private Carteirinha carteirinha;
    
    public Aluno(String nome, String curso, Carteirinha carteirinha) {
        this.nome = nome;
        this.curso = curso;
        this.carteirinha = carteirinha;
    }

    public String getNome() {
        return nome;
    }
    public String getCurso() {
        return curso;
    }
    public Carteirinha getCarteirinha() {
        return carteirinha;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }
    public void setCurso(String curso) {
        this.curso = curso;
    }


    public void exibirDados() {
        System.out.println("Nome: " + nome);
        System.out.println("Curso: " + curso);
        this.carteirinha.exibirDados();
    }
    
}
