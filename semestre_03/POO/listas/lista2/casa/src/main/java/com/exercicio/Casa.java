package com.exercicio;

public class Casa {
    private int qtdComodos;
    private double area;
    private String arquitetura;
    private Endereco endereco;


    public Casa(int qtdComodos, double area, String arquitetura, Endereco endereco) {
        this.qtdComodos = qtdComodos;
        this.area = area;
        this.arquitetura = arquitetura;
        this.endereco = endereco;
    }


    public int getQtdComodos() {
        return qtdComodos;
    }
    public double getArea() {
        return area;
    }
    public String getArquitetura() {
        return arquitetura;
    }
    public Endereco getEndereco() {
        return endereco;
    }


    public void setQtdComodos(int qtdComodos) {
        this.qtdComodos = qtdComodos;
    }
    public void setArea(double area) {
        this.area = area;
    }
    public void setArquitetura(String arquitetura) {
        this.arquitetura = arquitetura;
    }
    public void setEndereco(Endereco endereco) {
        this.endereco = endereco;
    }   
    
    
    public void exibirCasa() {
        System.out.println("Quantidade de comodos: " + qtdComodos);
        System.out.println("Área m^2:" + area);
        System.out.println("Estilo de arquitetura: " + arquitetura);
        endereco.exibirDados();
    }
}
