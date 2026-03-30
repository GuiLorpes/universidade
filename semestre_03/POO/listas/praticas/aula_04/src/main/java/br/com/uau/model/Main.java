package main.java.br.com.uau.model;

public class Main {
    public static void main(String[] args) {
        Pessoa lopes = new Pessoa();
        lopes.nome = "Guilherme Lopes";
        lopes.falar();
        System.out.println("Meu nome é " + lopes.nome);
        }
}