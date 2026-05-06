package com.aula_14.controller;

import java.util.ArrayList;
import java.util.List;
import com.aula_14.model.Tarefa;

public class TarefaControle {
    private List<Tarefa> tarefas;

    public TarefaControle() {
        this.tarefas = new ArrayList<>();
    }
    
    public boolean cadastrarTarefa(String titulo, String descricao) {
        if (titulo == null || titulo.isBlank()) {
            return false;
        }  
        Tarefa tr = new Tarefa(titulo, descricao);
        tarefas.add(tr);
        return true;
    }

    public List<Tarefa> listarTarefas() {
        return tarefas;
    }

}
