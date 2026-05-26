package com.exercicio;

import java.security.PublicKey;

public class Carro {
    private String marca;
    private String modelo;
    private Motor motor;
    private Estado estado;


    public Carro(String marca, String modelo, Motor motor) {
        this.marca = marca;
        this.modelo = modelo;
        this.motor = motor;
        this.estado = Estado.DESLIGADO;
    }


    public String getMarca() {
        return marca;
    }
    public String getModelo() {
        return modelo;
    }
    public Motor getMotor() {
        return motor;
    }
    public Estado getEstado() {
        return estado;
    }


    public void setMarca(String marca) {
        this.marca = marca;
    }
    public void setModelo(String modelo) {
        this.modelo = modelo;
    }
    public void setMotor(Motor motor) {
        this.motor = motor;
    }
    public void setEstado(Estado estado) {
        this.estado = estado;
    }


    public void ligarCarro() {
        this.estado = Estado.LIGADO;
    }
    public void desligarCarro() {
        this.estado = Estado.DESLIGADO;
    }


    public void exibirFichaTecnica() {
        System.out.println("Marca: " + marca);
        System.out.println("Modelo: " + modelo);
        System.out.println("Tipo do motor: " + motor.getTipo());
        System.out.println("Potencia do motor: " + motor.getPotencia());
        System.out.println("Numero de serie do motor: " + motor.getNumeroSerie());
        System.out.println("Estado do carro: " + estado.getDescricao());
    }
}
