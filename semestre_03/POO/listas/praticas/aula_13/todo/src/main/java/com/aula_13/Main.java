package com.aula_13;

public class Main {
    public static void main(String[] args) {
        Usuario user1 = new Usuario("Guilherme", TipoUsuario.PADRAO);
        Usuario user2 = new Usuario("João", TipoUsuario.VISITANTE);

        SistemaRegistro sr = new SistemaRegistro();

        boolean tarefa1 = sr.registrarTarefa(43,"Estudar ARQ 1", user1);
        boolean tarefa2 = sr.registrarTarefa(67, "Ir catar coquinho", user2);

        System.err.println("user1 registrou? " + tarefa1);
        System.out.println("user2 registrou? " + tarefa2);
    }
}