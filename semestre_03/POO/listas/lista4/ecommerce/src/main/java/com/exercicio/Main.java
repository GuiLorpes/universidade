package com.exercicio;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);

        Usuario user1 = new Usuario("Guilherme", NivelAcesso.ADMIN);
        Usuario user2 = new Usuario("José", NivelAcesso.USUARIO);

        List<Usuario> usuarios = new ArrayList<>();
        usuarios.add(user1); usuarios.add(user2);

        List<Produto> produtos = new ArrayList<>();
        Usuario user;
        System.err.println("Insira seu nome de usuário");
        String usr = scan.nextLine();
        int i = 0;
        while (i < usuarios.size() && !usuarios.get(i).getNome().equals(usr)) {
            i++;
        }
        if (usuarios.get(i).getNome().equals(usr)) {
            user = usuarios.get(i);
        }
        else {
            System.out.println("Usuário não registrado!");
            scan.close();
            return;
        }

        if (user.getAcesso() == NivelAcesso.ADMIN) {
            int caso = 0;
            do {
                System.out.println("Deseja ver os produtos ou inserir um novo?");
                System.out.println("1 -> Inserir | 2 -> Vizualizar | 0 -> Sair");
                caso = scan.nextInt();
                scan.nextLine();
                switch (caso) {
                    case 1:
                        System.err.println("Insira os dados do produto");
                        System.out.println("Nome: ");
                        String nome = scan.nextLine();
                        System.out.println("Preço: ");
                        double preco = scan.nextDouble();
                        Produto prod = new Produto(nome, preco);
                        produtos.add(prod);
                        break;
                    
                    case 2:
                        for (Produto p : produtos) {
                            System.out.println("Nome: " + p.getNome());
                            System.out.println("Preço: " + p.getPreco()); 
                            System.out.println("====================================");
                        }
                        break;
                }
            } while (caso !=0);
        }
        else {
            for (Produto p : produtos) {
            System.out.println("Nome: " + p.getNome());
            System.out.println("Preço: " + p.getPreco()); 
            System.out.println("====================================");
            }
        }
    scan.close();
    }
}