package com.aula_10;

public abstract class FiguraGeometrica {
    private String nome;
    private int qtdLados;


    public FiguraGeometrica(String nome, int qtdLados) {
        this.nome = nome;
        this.qtdLados = qtdLados;
    }


    public String getNome() {
        return nome;
    }
    public int getQtdLados() {
        return qtdLados;
    }


    public void setNome(String nome) {
    this.nome = nome;
    }
    public void setQtdLados(int qtdLados) {
        this.qtdLados = qtdLados;
    }

    
    public abstract double calcularArea();
}