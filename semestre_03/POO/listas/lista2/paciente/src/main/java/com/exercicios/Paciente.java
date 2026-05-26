package com.exercicios;

public class Paciente {
    private String nome;
    private int idade;
    private Prontuario prontuario;

    
    public Paciente(String nome, int idade, Prontuario prontuario) {
        this.nome = nome;
        this.idade = idade;
        this.prontuario = prontuario;
    }


    public String getNome() {
        return nome;
    }
    public int getIdade() {
        return idade;
    }
    public Prontuario getProntuario() {
        return prontuario;
    }


    public void setNome(String nome) {
        this.nome = nome;
    }
    public void setIdade(int idade) {
        this.idade = idade;
    }
    public void setProntuario(Prontuario prontuario) {
        this.prontuario = prontuario;
    }


    public void exibirPaciente() {
        System.out.println("Nome: " + nome);
        System.out.println("Idade: " + idade);
        System.out.println("Registro: " + prontuario.getNumRegistro());
        System.out.println(("Tipo sanguineo: " + prontuario.getTipoSanguineo().getDescricao()));
        System.out.println("Alergias: " + prontuario.getAlergias());
    }
}
