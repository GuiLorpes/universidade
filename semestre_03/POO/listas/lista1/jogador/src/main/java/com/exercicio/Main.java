package com.exercicio;

public class Main {
    public static void main(String[] args) {
        Jogador p = new Jogador();
        p.setNome("Jogador");
        p.setNivel(0);
        p.setPontuacao(0);
        p.adicionarPontos(30);
        System.out.println(p.getPontuacao());
        p.adicionarPontos(69);
        System.out.println(p.getPontuacao());
        System.out.println(p.getNivel());
        p.adicionarPontos(2);
        System.out.println(p.getPontuacao());
        System.out.println(p.getNivel());
    }
}