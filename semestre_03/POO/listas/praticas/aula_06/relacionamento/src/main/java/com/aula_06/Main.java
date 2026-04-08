package com.aula_06;

public class Main {
    public static void main(String[] args) {
        Endereco casa1 = new Endereco(111, "Rua Uau", "Jardim Legal", "67694200");
        Pessoa guiLopes = new Pessoa("Guilherme Lopes", "111.222.333-44", 20, 1.80, casa1);
        Pessoa giWater = new Pessoa();
    }
}