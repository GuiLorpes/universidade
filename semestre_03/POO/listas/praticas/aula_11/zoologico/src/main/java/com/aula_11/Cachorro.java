package com.aula_11;

public class Cachorro extends Animal implements Terrestre{
    private String raca;
    
    public Cachorro(String nome, String raca) {
        super(nome);
        this.raca = raca;
    }

    public String getRaca() {
        return raca;
    }

    public void setRaca(String raca) {
        this.raca = raca;
    }

    @Override
    public void emitirSom() {
        System.err.println(this.getNome() + ": au au");
    }

    @Override
    public void andar() {
        System.err.println(getNome() + " está andando");
    }
}