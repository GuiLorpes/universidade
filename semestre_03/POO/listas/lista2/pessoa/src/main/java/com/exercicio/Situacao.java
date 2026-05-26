package com.exercicio;

public enum Situacao {
    REGULAR("Regular"),
    SUSPENSO("Suspenso"),
    CANCELADO("Cancelado");

    private String descricao;
    
    Situacao(String descricao) {
        this.descricao = descricao;
    }

    public String getDescricao() {
        return descricao;
    }
    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }

}
