package com.aula_13;

import java.util.List;
import java.util.ArrayList;

public class SistemaRegistro {
    private List<Tarefa> tarefas;

    public SistemaRegistro() {
        this.tarefas = new ArrayList<>();
    }

    public boolean registrarTarefa(int id, String descricao, Usuario usuario) {
        if (usuario.getTipo() == TipoUsuario.PADRAO) {
            Tarefa tarefa = new Tarefa(id ,descricao, usuario);
            tarefas.add(tarefa);
            return true;
        }
        return false;
    }

    public boolean removerTarefa(int id) {
        is (usuario.getTipo() == TipoUsuario.ADMIN) {
            for ( )
        }
    }

}