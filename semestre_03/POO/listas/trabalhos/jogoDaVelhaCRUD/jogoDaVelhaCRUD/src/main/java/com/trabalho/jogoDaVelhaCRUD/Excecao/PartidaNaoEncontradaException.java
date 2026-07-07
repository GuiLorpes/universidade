package com.trabalho.jogoDaVelhaCRUD.Excecao;

public class PartidaNaoEncontradaException extends RuntimeException {
    public PartidaNaoEncontradaException(String mensagem) {
        super(mensagem);
    }
}
