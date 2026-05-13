package com.exercicio;

public class Carro {
    private String marca;
    private String carro;
    private double velocidade;


    public String getMarca() {
        return marca;
    }
    public String getCarro() {
        return carro;
    }
    public double getVelocidade() {
        return velocidade;
    }

    public void setMarca(String marca) {
        this.marca = marca;
    }
    public void setCarro(String carro) {
        this.carro = carro;
    }
    public void setVelocidade(double velocidade) {
        this.velocidade = velocidade;
    }

    
    public void acelerar() {
        this.velocidade += 10.4;
    }

    public void frear() {
        double freio = 7.5; 
        if (velocidade <= freio) {
            this.velocidade = 0;
        }
        else {
            this.velocidade -= freio;
        }
    }

    public void mostrarVelocidade() {
        System.out.println(velocidade + " Km/h");
    }
}
