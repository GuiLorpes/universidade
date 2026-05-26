package com.exercicio;

public class Aluno extends Pessoa{
    private String matricula;
    private String curso;

    public Aluno(String nome, int idade, String cpf, String matricula, 
        String curso) {
        super(nome, idade, cpf);
        this.matricula = matricula;
        this.curso = curso;
    }

    public String getMatricula() {
        return matricula;
    }
    public String getCurso() {
        return curso;
    }

    
    public void setMatricula(String matricula) {
        this.matricula = matricula;
    }
    public void setCurso(String curso) {
        this.curso = curso;
    }
    
    
    @Override
    public void exibirDados() {
        System.out.println("Nome: " + this.getNome());
        System.out.println("Idade: " + this.getIdade());
        System.out.println("CPF: " + this.getCpf());
        System.out.println("Numero de matricula: " + matricula);
        System.out.println("Curso: " + curso);
    }
}
