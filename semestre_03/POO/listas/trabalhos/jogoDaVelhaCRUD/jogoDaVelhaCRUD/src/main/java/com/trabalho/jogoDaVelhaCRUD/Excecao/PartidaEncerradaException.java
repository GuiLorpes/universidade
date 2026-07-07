package com.trabalho.jogoDaVelhaCRUD.Excecao;

public class PartidaEncerradaException extends RuntimeException {
    public PartidaEncerradaException(String mensagem) {
        super(mensagem);
    }
}