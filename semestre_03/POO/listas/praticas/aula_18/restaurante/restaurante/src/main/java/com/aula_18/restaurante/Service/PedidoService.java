package com.aula_18.restaurante.Service;

import org.springframework.beans.factory.annotation.Autowired;

import com.aula_18.restaurante.Repository.PedidoRepository;

public class PedidoService {
    @Autowired
    private PedidoRepository pedidoRepository;
}
