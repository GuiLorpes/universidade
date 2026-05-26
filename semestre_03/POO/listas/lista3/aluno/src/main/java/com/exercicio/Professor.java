package com.exercicio;

public class Professor extends Pessoa{
    private String disciplina;
    private double salario;

    
    public Professor(String nome, int idade, String cpf, String disciplina, double salario) {
        super(nome, idade, cpf);
        this.disciplina = disciplina;
        this.salario = salario;
    }


    public String getDisciplina() {
        return disciplina;
    }
    public double getSalario() {
        return salario;
    }

    
    public void setDisciplina(String disciplina) {
        this.disciplina = disciplina;
    }
    public void setSalario(double salario) {
        this.salario = salario;
    }
    
    
    @Override
    public void exibirDados() {
        System.out.println("Nome: " + this.getNome());
        System.out.println("Idade: " + this.getIdade());
        System.out.println("CPF: " + this.getCpf());
        System.out.println("Disciplina: " + disciplina);
        System.out.println("Salário: " + salario);
    }
}
