package com.exercicio;

import java.util.ArrayList;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        Aluno lopes = new Aluno("Guilherme Lopes", 20, "111.222.333-44", "123456", 
        "Ciência da Computação");
        Aluno shimano = new Aluno("Guilherme Shimano", 19, "122.233.344-55", 
        "234125", "Ciência da Computação");
        Aluno munir = new Aluno("Munir", 19, "432.543.134-10", "672347", 
        "Ciência da Computação");


        Professor anderson = new Professor("Anderson", 58, "321.545.132-56", 
        "Arquitetura e Organização de Computadores 1", 10432);
        Professor choma = new Professor("João Choma", 35, "123.890.435-12", 
        "Programação Orientada a Objetos", 0.02);
        Professor jonathan = new Professor("Jonathan", 28, "125.327.673-89", 
        "Organização e Recuperação de Dados", 5.50);


        ArrayList<Aluno> alunos = new ArrayList<>();
        alunos.add(munir); alunos.add(shimano); alunos.add(lopes);
        for (Aluno a : alunos) {
            a.exibirDados();
            System.out.println("=================================");
        }

        ArrayList<Professor> profs = new ArrayList<>();
        profs.add(jonathan); profs.add(anderson); profs.add(choma);
        int caso = 0;
        do {
            System.out.println("Deseja procurar por um professor ou ver todos?");
            System.out.println("1 -> Procurar por um | 2 -> Ver todos | 0 -> Sair");
            caso = scan.nextInt();
            scan.nextLine();
            switch (caso) {
                case 1:
                    System.err.println("Qual o nome do professor que deseja " + 
                    "procurar?");
                    String prof = scan.nextLine();
                    int i = 0;
                    while (i < profs.size() && !profs.get(i).getNome().equals(prof)) {
                        i++;
                    }
                    if (profs.get(i).getNome().equals(prof)) {
                        profs.get(i).exibirDados();
                        System.out.println("============================");
                    }
                    else {
                        System.out.println("Professor não registrado!");
                    }
                    break;
                
                case 2:
                    for (Professor p : profs) {
                        p.exibirDados();
                        System.out.println("====================================");
                    }
                    break;
            }
        } while (caso !=0);

        ArrayList<Pessoa> pessoas = new ArrayList<>();
        pessoas.add(choma); pessoas.add(anderson); 
        pessoas.add(lopes); pessoas.add(munir);
        for (Pessoa pessoa : pessoas) {
            pessoa.exibirDados();
            System.out.println("====================================");
        }
        scan.close();
    }
}