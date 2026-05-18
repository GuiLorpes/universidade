package com.exercicio;

public class Jogador {
    private String nome;
    private int pontuacao;
    private int nivel;


    public String getNome() {
        return nome;
    }
    public int getPontuacao() {
        return pontuacao;
    }
    public int getNivel() {
        return nivel;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }
    public void setPontuacao(int pontuacao) {
        this.pontuacao = pontuacao;
    }
    public void setNivel(int nivel) {
        this.nivel = nivel;
    }

    
    void adicionarPontos(int valor) {
        pontuacao += valor;
        if (pontuacao / 100 > 0) {
            pontuacao = (pontuacao / 100 + pontuacao % 100);
            this.subirNivel();
        }
    }

    void subirNivel() {
        nivel++;
    }
}
