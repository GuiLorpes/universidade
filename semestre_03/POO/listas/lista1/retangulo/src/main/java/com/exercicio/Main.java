package com.exercicio;

public class Main {
    public static void main(String[] args) {
        Retangulo r = new Retangulo();
        r.setAltura(6.7);
        r.setBase(4);
        System.out.println(r.calcularArea());
        System.out.println(r.calcularPerimetro());
    }
}