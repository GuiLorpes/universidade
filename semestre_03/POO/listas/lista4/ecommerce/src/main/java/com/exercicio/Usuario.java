package com.exercicio;

public class Usuario {
    private String nome;
    private NivelAcesso acesso;

    
    public Usuario(String nome, NivelAcesso acesso) {
        this.nome = nome;
        this.acesso = acesso;
    }


    public String getNome() {
        return nome;
    }
    public NivelAcesso getAcesso() {
        return acesso;
    }
}
