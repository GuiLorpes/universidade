package com.exercicio;

public enum Estado {
    LIGADO("Ligado"),
    DESLIGADO("Desligado");

    private String descricao;

    Estado(String descricao) {
        this.descricao = descricao;
    }

    public String getDescricao() {
        return descricao;
    }
}
