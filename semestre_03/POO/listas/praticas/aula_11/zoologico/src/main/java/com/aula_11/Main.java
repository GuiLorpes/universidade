package com.aula_11;

public class Main {
    public static void main(String[] args) {
        Cachorro toffee = new Cachorro("Toffee", "vira-lata");
        toffee.emitirSom(); 
        toffee.andar();

        PicaPau queroquero = new PicaPau("QueroQuero");
        queroquero.emitirSom();
        queroquero.voar();

        Pato feio = new Pato("feio");
        feio.emitirSom();
        feio.andar();
    }
}