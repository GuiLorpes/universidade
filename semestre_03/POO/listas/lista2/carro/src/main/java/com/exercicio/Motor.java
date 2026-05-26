package com.exercicio;

public class Motor {
    private String tipo;
    private double potencia;
    private int numeroSerie;

    
    public Motor(String tipo, double potencia, int numeroSerie) {
        this.tipo = tipo;
        this.potencia = potencia;
        this.numeroSerie = numeroSerie;
    }


    public String getTipo() {
        return tipo;
    }
    public double getPotencia() {
        return potencia;
    }
    public int getNumeroSerie() {
        return numeroSerie;
    }


    public void setTipo(String tipo) {
        this.tipo = tipo;
    }
    public void setPotencia(double potencia) {
        this.potencia = potencia;
    }
    public void setNumeroSerie(int numeroSerie) {
        this.numeroSerie = numeroSerie;
    }

    
}
