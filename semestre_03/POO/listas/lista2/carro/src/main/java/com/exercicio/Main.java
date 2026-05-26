package com.exercicio;

public class Main {
    public static void main(String[] args) {
        Motor v8 = new Motor("V8", 488, 67869);
        Carro mustang = new Carro("Ford", "Mustang", v8);
        mustang.exibirFichaTecnica();
        mustang.ligarCarro();
        System.out.println(mustang.getEstado().getDescricao());
        mustang.desligarCarro();
        System.out.println(mustang.getEstado().getDescricao());
    }
}