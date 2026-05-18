package com.aula_15.controller;

import java.util.ArrayList;
import java.util.List;

import com.aula_15.excecao.Validacao;
import com.aula_15.model.Aluno;

public class AlunoControle {
    // Todo aluno tem um nome não vazio
    // Todo aluno tem uma nota não vazia no intervalo de [0,10]

    private List<Aluno> listaAlunos;

    public AlunoControle() {
        this.listaAlunos = new ArrayList<>();
    }
    
    public void cadastrar(String nome, int nota) throws Validacao{
        validarNome(nome);
        Aluno aluno = new Aluno(nome, nota);
        listaAlunos.add(aluno);
    }

    private void validarNome(String nome) throws Validacao{
        if (nome == null || nome.isBlank()) {
            throw new Validacao("O nome do aluno é obrigatório");
        }
    }
}
