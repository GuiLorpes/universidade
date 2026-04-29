package com.aula_10;

public class Quadrado extends FiguraGeometrica{
    private double tamLado;

    public Quadrado(double tamLado) {
        super("Quadrado", 4);
        this.tamLado = tamLado;
    }


    public double getTamLado() {
    return tamLado;
    }

    public void setTamLado(double tamLado) {
        this.tamLado = tamLado;
    }


    public double calcularArea() {
        return tamLado * tamLado;
    }
}