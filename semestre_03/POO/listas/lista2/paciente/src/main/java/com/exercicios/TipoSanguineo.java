package com.exercicios;

public enum TipoSanguineo {
    A_POS("A+"),
    B_POS("B+"),
    AB_POS("AB+"),
    O_POS("O+"),
    A_NEG("A-"),
    B_NEG("B-"),
    AB_NEG("AB-"),
    O_NEG("O-");
    private String descricao; 

    TipoSanguineo(String descricao) {
        this.descricao = descricao;
    }

    public String getDescricao() {
        return descricao;
    }
}
