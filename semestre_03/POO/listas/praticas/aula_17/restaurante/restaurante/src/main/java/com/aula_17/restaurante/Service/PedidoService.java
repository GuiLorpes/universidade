package com.aula_17.restaurante.Service;

import java.util.ArrayList;
import java.util.List;
import org.springframework.stereotype.Service;
import com.aula_17.restaurante.Model.Pedido;

@Service
public class PedidoService {
    private ArrayList<Pedido> pedidos = new ArrayList<>();

    public Pedido criarPedido(Pedido pedido) {
        pedidos.add(pedido);
        return pedido;
    }


    public List<Pedido> lerListaPedido() {
        return pedidos;
    }
}
