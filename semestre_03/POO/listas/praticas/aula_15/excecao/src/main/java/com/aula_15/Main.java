package com.aula_15;

import com.aula_15.controller.AlunoControle;
import com.aula_15.excecao.Validacao;

public class Main {
    public static void main(String[] args) {
        AlunoControle aluno1 = new AlunoControle();
        AlunoControle aluno2 = new AlunoControle();


        try {
            aluno2.cadastrar("", 2);
            System.out.println("Cadastrado");
        } catch(Validacao e) {
            System.out.println(e.getMessage());
        }
        
        try {
            aluno1.cadastrar("Guilherme", 9);
            System.out.println("Cadastrado");
        } catch(Validacao e) {
            System.out.println(e.getMessage());
        }
    }
}