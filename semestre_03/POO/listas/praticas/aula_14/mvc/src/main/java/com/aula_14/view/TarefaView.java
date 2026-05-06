package com.aula_14.view;

import java.util.List;
import java.util.Scanner;
import com.aula_14.controller.TarefaControle;
import com.aula_14.model.Tarefa;

public class TarefaView {
    private Scanner scan;
    private TarefaControle controle;

    public TarefaView() {
        this.scan = new Scanner(System.in);
        this.controle = new TarefaControle();
    }

    public void exibirMenu() {
        int opcao;
        do {
            System.out.println("============================");
            System.out.println("     Sistema de Tarefas     ");
            System.out.println("============================");
            System.out.println("Digite que operação deseja");
            System.out.println("1 -> Criar Tarefa");
            System.out.println("2 -> Visualizar Tarefas");
            System.out.println("0 -> Sair");
            opcao = Integer.parseInt(scan.nextLine());
            switch (opcao) {
                case 1:
                    cadastrarTarefa();
                    System.out.println();
                    break;
                case 2:
                    listarTarefas();
                    System.out.println();
                    break;
                case 0:
                    System.out.println("Sayonara!");
                    break;
                default:
                    System.out.println("Opção inválida!");
                    break;
            }
        } while (opcao != 0);
    }

    private void cadastrarTarefa() {
        System.out.println("Insira o titulo da sua tarefa");
        String titulo = scan.nextLine();
        System.out.println("Insira a descrição da tarefa");
        String descricao = scan.nextLine();
        boolean sucesso = controle.cadastrarTarefa(titulo, descricao);
        if (sucesso) {
            System.out.println("Tarefa cadastrada!");
        }
        else {
            System.out.println("Não foi possivel cadastrar a tarefa.");
        }
    }

    private void listarTarefas() {
        System.out.println("Tarefas:");
        List<Tarefa> tarefas = controle.listarTarefas();
        for (Tarefa t: tarefas) {
            System.out.println(t.toString());
        
        }
    }
}
