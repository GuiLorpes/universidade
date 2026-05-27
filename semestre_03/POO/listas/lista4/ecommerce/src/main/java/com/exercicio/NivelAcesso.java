package com.exercicio;

public enum NivelAcesso {
    USUARIO("Usuario"),
    ADMIN("Admin");

    private String descricao;

    NivelAcesso(String descricao) {
        this.descricao = descricao;
    }

    public String getDescricao() {
        return descricao;
    }
}
