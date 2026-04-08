package com.exemplo_aula05;

public class Livro {
    private int id;
    private String titulo;
    private String autor;
    private int anoPublicacao;
    private boolean disponivel;
    
    // Construtor
    public Livro(String titulo, String autor, int anoPublicacao) {
        this.titulo = titulo;
        this.autor = autor;
        this.anoPublicacao = anoPublicacao;
        this.disponivel = true;
    }

    // Métodos "get"
    public int getId() {
        return this.id;
    }
    public String getTitulo() {
        return this.titulo;
    }
    public String getAutor() {
        return this.autor;
    }
    public int getAnoPublicacao() {
        return this.anoPublicacao;
    }
    public boolean isDisponivel() {
        return this.disponivel;
    }

    // Métodos "set"
    public void setId(int id) {
        this.id = id;
    }
    public void setTitulo(String titulo) {
        this.titulo = titulo;
    }
    public void setAutor(String autor) {
        this.autor = autor;
    }
    public void setAnoPublicacao(int ano) {
        this.anoPublicacao = ano;
    }
    public void setDisponivel(boolean disponivel) {
        this.disponivel = disponivel;
    }

    // Métodos de emprestimo e devolução
    public void emprestar() {
        if (this.disponivel) {
            System.out.println("Livro emprestado!");
            this.setDisponivel(false);
        }
        else {
            System.out.println("Livro indisponivel!");
        }
    }

    public void devolver() {
        if (!(this.disponivel)) {
        System.out.println("Livro devolvido!");
        this.setDisponivel(true);
        }
        else {
            System.out.println("Livro já está disponivel!");
            System.out.println("Não é possivel devolver!");
        }
    }

    public String toString() {
        String disponibilidade;
        if (this.disponivel) {
            disponibilidade = "DISPONIVEL";
        } 
        else {
            disponibilidade = "INDISPONIVEL";
        }
        return "Titulo: " + this.titulo + "\nAutor: " + this.autor + 
        "\nAno de publicação: " + this.anoPublicacao + "\nDisponibilidade: " 
         + disponibilidade; 
    }
}