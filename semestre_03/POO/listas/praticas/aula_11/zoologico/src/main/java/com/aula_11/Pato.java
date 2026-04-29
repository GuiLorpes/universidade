package com.aula_11;

public class Pato extends Animal implements Terrestre, Voador, Aquatico {

    public Pato(String nome) {
        super(nome);
    }
    
    @Override
    public void andar() {
        System.err.println(getNome() + " está andando");
    }

    @Override
    public void nadar() {
        System.err.println(getNome() + " está nadando");
    }

    @Override
    public void voar() {
        System.err.println(getNome() + " está voando");
    }

    @Override
    public void emitirSom() {
        System.out.println(getNome() + ": quack");
    }
}  