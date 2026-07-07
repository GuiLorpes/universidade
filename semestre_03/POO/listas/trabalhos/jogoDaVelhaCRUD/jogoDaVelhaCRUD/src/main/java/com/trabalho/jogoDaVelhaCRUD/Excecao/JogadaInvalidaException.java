package com.trabalho.jogoDaVelhaCRUD.Excecao;

import org.springframework.http.HttpStatus;

public class JogadaInvalidaException extends RuntimeException {

    private final HttpStatus status;

    public JogadaInvalidaException(String mensagem) {
        this(mensagem, HttpStatus.BAD_REQUEST);
    }

    public JogadaInvalidaException(String mensagem, HttpStatus status) {
        super(mensagem);
        this.status = status;
    }

    public HttpStatus getStatus() {
        return status;
    }
}
