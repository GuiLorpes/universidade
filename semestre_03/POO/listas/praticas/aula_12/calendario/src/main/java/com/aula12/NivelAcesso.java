package com.aula12;

public enum NivelAcesso {
    ADMIN("Administrador"),
    USUARIO("Usuário"),
    LEITOR("Visitante");

    private String descricao;

    NivelAcesso(String descricao){
        this.descricao = descricao;
    }

    public String getDescricao() {
        return descricao;
    }
    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }
}