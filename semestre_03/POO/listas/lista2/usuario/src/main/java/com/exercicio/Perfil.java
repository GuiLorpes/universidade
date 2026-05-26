package com.exercicio;

public class Perfil {
    private String nome;
    private String biografia;
    private String linkFoto;
    private Visibilidade visibilidade;

    
    public Perfil(String nome, String biografia, String linkFoto, Visibilidade 
        visibilidade) {
        this.nome = nome;
        this.biografia = biografia;
        this.linkFoto = linkFoto;
        this.visibilidade = visibilidade;
    }


    public String getNome() {
    return nome;
    } 
    public String getBiografia() {
        return biografia;
    }
    public String getLinkFoto() {
        return linkFoto;
    }
    public Visibilidade getVisibilidade() {
        return visibilidade;
    }


    public void setNome(String nome) {
        this.nome = nome;
    }
    public void setBiografia(String biografia) {
        this.biografia = biografia;
    }
    public void setLinkFoto(String linkFoto) {
        this.linkFoto = linkFoto;
    }
    public void setVisibilidade(Visibilidade visibilidade) {
        this.visibilidade = visibilidade;
    }
}