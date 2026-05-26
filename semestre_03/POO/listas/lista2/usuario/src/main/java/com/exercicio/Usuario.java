package com.exercicio;

public class Usuario {
    private String login;
    private String email;
    private Perfil perfil;

    
    public Usuario(String login, String email, Perfil perfil) {
        this.login = login;
        this.email = email;
        this.perfil = perfil;
    }


    public String getLogin() {
        return login;
    }
    public String getEmail() {
        return email;
    }
    public Perfil getPerfil() {
        return perfil;
    }


    public void setLogin(String login) {
        this.login = login;
    }
    public void setEmail(String email) {
        this.email = email;
    }
    public void setPerfil(Perfil perfil) {
        this.perfil = perfil;
    }
    
    
    public void exibirUsuario() {
        System.out.println("Nome: " + perfil.getNome());
        System.out.println("Biografia: " + perfil.getBiografia());
        System.out.println("Foto de perfil: " + perfil.getLinkFoto());
        System.out.println("Visibilidade: " + perfil.getVisibilidade()
        .getDescricao());
        System.out.println("Login: " + login);
        System.out.println("Email: " + email);
    }
}
