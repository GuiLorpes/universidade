package com.exercicio;

public class Main {
    public static void main(String[] args) {
        Perfil shigamesplays = new Perfil("Shimano Gameplays",
         "Canal de gameplays de LoL de segunda a segunda com videos novos :O",
          "https://img2.lovecell.com.br/90feb4fece21e6b591abc970dfbd5e2de84991ef1c7e5b363807d7256b3d78fe.webp", 
          Visibilidade.PUBLICO);
        Usuario shimano = new Usuario("shishi", "shimanogameplays67@gmail.com", shigamesplays);
        shimano.exibirUsuario();
    }
}