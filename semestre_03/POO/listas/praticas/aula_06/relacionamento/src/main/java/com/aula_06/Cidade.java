package com.aula_06;

public class Cidade {
    private String nome;
    private String coords;

    public Cidade(String nome, String coords) {
        this.nome = nome;
        this.coords = coords;
    }

    public String getNome() {
        return this.nome;
    }
    public String getCoords() {
        return this.coords;
    }
}