package com.guilopes;

public class Calculadora {
    private double n1, n2;


    
    public double getN1() {
        return n1;
    }
    public double getN2() {
        return n2;
    }

    public void setN1(double n1) {
        this.n1 = n1;
    }
    public void setN2(double n2) {
        this.n2 = n2;
    }



    public double somar() {
        return n1 + n2;
    }
    public double subtrair() {
        return n1 - n2;
    }
    public double multiplicar() {
        return n1 * n2;
    }
    public double dividir () {
        if (n2 == 0) {
            throw new ArithmeticException("Divisão por 0");
        }
        return n1 / n2;
    } 
}