package com.aula_13;

public class Tarefa {
    private int id;
    private String descricao;
    private Usuario usuarioResponsavel;

    public Tarefa (int id, String descricao, Usuario usuarioResponsavel) {
        this.id = id;
        this.descricao = descricao;
        this.usuarioResponsavel = usuarioResponsavel;
    }

    public String getDescricao() {
        return descricao;
    }
    public Usuario getUsuarioResponsavel() {
        return usuarioResponsavel;
    }

    @Override
    public String toString() {
        return "Tarefa:" + descricao + "\n" + "Usuario:" + usuarioResponsavel;
    }
}