package com.exemplo_aula05;

public class Main {
    public static void main(String[] args) {
        Livro noitesBrancas = new Livro("Noites Brancas", 
        "Fiódor Dotoiévski" , 1848);
        Livro kaoruHana = new Livro("Kaoru Hana wa Rin to Saku", 
        "Mikami Saka", 2021);
        System.err.println(noitesBrancas.getTitulo());
        System.out.println(noitesBrancas.getAutor());
        System.out.println(noitesBrancas.getAnoPublicacao());
        System.out.println(kaoruHana.toString());

        noitesBrancas.emprestar();
        noitesBrancas.emprestar();
        noitesBrancas.devolver();
        kaoruHana.devolver();
    }
}