package com.aula_10;

import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        ArrayList<FiguraGeometrica> estFiguras = new ArrayList<>();


        FiguraGeometrica bobesponja = new Quadrado(5.2);
        // System.out.println("Area quadrado = " + bobesponja.calcularArea());

        FiguraGeometrica phineas = new Triangulo(23, 7);
        // System.out.println("Area tringulo = " + phineas.calcularArea());

        estFiguras.add(bobesponja);
        estFiguras.add(phineas);
        estFiguras.add(new Quadrado(4.1));
        estFiguras.size();

        for (FiguraGeometrica fig : estFiguras) {
            System.out.println("Figura: " + fig.getNome());
            System.out.println("Area: " + fig.calcularArea());
            System.out.println("-----------");
        }
    }
}