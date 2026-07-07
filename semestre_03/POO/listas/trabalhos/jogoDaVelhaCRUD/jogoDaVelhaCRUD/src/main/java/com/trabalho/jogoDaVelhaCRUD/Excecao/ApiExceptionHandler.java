package com.trabalho.jogoDaVelhaCRUD.Excecao;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ApiExceptionHandler {

    @ExceptionHandler(PartidaNaoEncontradaException.class)
    public ResponseEntity<ErroResponse> tratarPartidaNaoEncontrada(PartidaNaoEncontradaException ex) {
        return construirResposta(HttpStatus.NOT_FOUND, ex.getMessage());
    }

    @ExceptionHandler(PartidaEncerradaException.class)
    public ResponseEntity<ErroResponse> tratarPartidaEncerrada(PartidaEncerradaException ex) {
        return construirResposta(HttpStatus.CONFLICT, ex.getMessage());
    }

    @ExceptionHandler(JogadaInvalidaException.class)
    public ResponseEntity<ErroResponse> tratarJogadaInvalida(JogadaInvalidaException ex) {
        return construirResposta(ex.getStatus(), ex.getMessage());
    }

    @ExceptionHandler(DadosInvalidosException.class)
    public ResponseEntity<ErroResponse> tratarDadosInvalidos(DadosInvalidosException ex) {
        return construirResposta(HttpStatus.BAD_REQUEST, ex.getMessage());
    }

    private ResponseEntity<ErroResponse> construirResposta(HttpStatus status, String mensagem) {
        String erro = switch (status) {
            case BAD_REQUEST -> "Requisição inválida";
            case CONFLICT -> "Conflito";
            case NOT_FOUND -> "Não encontrado";
            default -> "Erro interno";
        };
        return ResponseEntity.status(status).body(new ErroResponse(status.value(), erro, mensagem));
    }
}