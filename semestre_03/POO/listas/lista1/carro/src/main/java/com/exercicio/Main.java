package com.exercicio;

public class Main {
    public static void main(String[] args) {
        Carro bibi = new Carro();
        bibi.setMarca("Lamborghini");
        bibi.setCarro("Revuelto");
        bibi.setVelocidade(0);
        double i = 0;
        while (i < 10) {
            bibi.acelerar();
            bibi.mostrarVelocidade();
            i += 0.5;
        }
        bibi.mostrarVelocidade();
        i = 0;
        while (i < 15) {
            bibi.frear();
            bibi.mostrarVelocidade();
            i += 0.5;
        }
        bibi.mostrarVelocidade();
    }
}