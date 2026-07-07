package com.lista_05.vendas.Controller;

import java.util.List;

public record OrcamentoRequest(
    double valor,
    long clienteId,
    List<Long> produtoIds
) {
}