package com.exercicio;

public class Main {
    public static void main(String[] args) {
        Endereco endereco = new Endereco("Rua Martin Alfonso", 642,
        "Zona 2", "Maringá");
        Casa casa = new Casa(8, 287, "Campestre", endereco);
        casa.exibirCasa();
    }
}