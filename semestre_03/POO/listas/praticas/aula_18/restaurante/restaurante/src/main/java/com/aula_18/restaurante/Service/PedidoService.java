package com.aula_18.restaurante.Service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.aula_18.restaurante.Model.Pedido;
import com.aula_18.restaurante.Repository.PedidoRepository;

@Service
public class PedidoService {
    @Autowired
    private PedidoRepository pedidoRepository;


    public List<Pedido> lerPedidos() {
        return pedidoRepository.findAll();
    }


    public Pedido inserirPedidos(Pedido pedido) {
        return pedidoRepository.save(pedido);
    }


    // public Pedido 
}
