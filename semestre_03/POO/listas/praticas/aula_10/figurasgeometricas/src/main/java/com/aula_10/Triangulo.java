package com.aula_10;

public class Triangulo extends FiguraGeometrica{
    private double base, altura;
    
    public Triangulo(double base, double altura) {
        super("Triangulo", 3);
        this.base = base;
        this.altura = altura;
    }


    public double getBase() {
        return base;
    }
    public double getAltura() {
        return altura;
    }
    
    
    public void setBase(double base) {
        this.base = base;
    }
    public void setAltura(double altura) {
        this.altura = altura;
    }
    
    
    public double calcularArea() {
        return this.base * this.altura;
    }
}