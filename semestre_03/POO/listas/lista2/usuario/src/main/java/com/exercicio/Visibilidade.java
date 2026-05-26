package com.exercicio;

public enum Visibilidade {
    PUBLICO("Publico"),
    PRIVADO("Privado");

    private String descricao;

    Visibilidade(String descricao) {
        this.descricao = descricao;
    }

    public String getDescricao() {
        return descricao;
    }
}
