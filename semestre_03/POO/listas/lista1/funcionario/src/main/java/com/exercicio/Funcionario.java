package com.exercicio;

public class Funcionario {
    private String nome;
    private String cargo;
    private double salario;

    
    public String getNome() {
        return nome;
    }
    public String getCargo() {
        return cargo;
    }
    public double getSalario() {
        return salario;
    }

    
    public void setNome(String nome) {
        this.nome = nome;
    }
    public void setCargo(String cargo) {
        this.cargo = cargo;
    }
    public void setSalario(double salario) {
        this.salario = salario;
    }


    public void aumentarSalario(double percentual) {
        this.salario *= 1.00 + percentual;
    }

    public void exibirFuncionario() {
        System.out.println("Nome: " + nome);
        System.out.println("Cargo: " + cargo);
        System.out.println("Salario: " + salario + "R$");
    }
}
