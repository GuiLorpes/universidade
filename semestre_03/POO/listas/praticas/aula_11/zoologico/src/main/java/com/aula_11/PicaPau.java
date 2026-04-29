package com.aula_11;

public class PicaPau extends Animal implements Voador {

    public PicaPau(String nome) {
        super(nome);
    }

    @Override
    public void voar() {
        System.err.println(getNome() + " está voando");
    }

    @Override
    public void emitirSom() {
        System.out.println(getNome() + "hehehe hehehe hehehehehe");
    }
    
}