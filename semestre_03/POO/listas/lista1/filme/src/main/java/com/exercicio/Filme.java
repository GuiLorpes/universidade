package com.exercicio;

public class Filme {
    private String titulo;
    private String genero;
    private String duracao;
    private double avaliacao;

    
    public String getTitulo() {
        return titulo;
    }
    public String getGenero() {
        return genero;
    }
    public String getDuracao() {
        return duracao;
    }
    public double getAvaliacao() {
        return avaliacao;
    }


    public void setTitulo(String titulo) {
        this.titulo = titulo;
    }
    public void setGenero(String genero) {
        this.genero = genero;
    }
    public void setDuracao(String duracao) {
        this.duracao = duracao;
    }
    public void setAvaliacao(double avaliacao) {
        this.alterarAvaliacao(avaliacao);
    }


    public void alterarAvaliacao(double avaliacao) {
        if (avaliacao > 10) {
            avaliacao = 10;
        }
        if (avaliacao < 0) {
            avaliacao = 0;
        }
        this.avaliacao = avaliacao;
    }


    public void exibirFichaTecnica() {
        System.out.println("Titulo: " + titulo);
        System.out.println("Genero: " + genero);
        System.out.println("Duração: " + duracao);
        System.out.println("Avaliação: " + avaliacao);
    }
}
