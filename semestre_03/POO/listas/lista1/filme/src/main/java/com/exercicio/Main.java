package com.exercicio;

public class Main {
    public static void main(String[] args) {
        Filme kungFuPanda = new Filme();
        kungFuPanda.setTitulo("Kung Fu Panda");;
        kungFuPanda.setGenero("Infantil/Comédia");
        kungFuPanda.setDuracao("1h 32min");
        kungFuPanda.setAvaliacao(7.6);
        kungFuPanda.exibirFichaTecnica();
        kungFuPanda.alterarAvaliacao(10000000);
        System.out.println("Avaliação: " + kungFuPanda.getAvaliacao());
    }
}