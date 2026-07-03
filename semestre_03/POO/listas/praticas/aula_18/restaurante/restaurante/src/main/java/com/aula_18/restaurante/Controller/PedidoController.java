package com.aula_18.restaurante.Controller;
import com.aula_18.restaurante.Model.Pedido;
import com.aula_18.restaurante.Service.PedidoService;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/pedidos")
public class PedidoController {
    @Autowired
    private PedidoService pedidoService;
    
    @GetMapping
    public List<Pedido> lerPedidos() {
        return pedidoService.lerPedidos();
    }

    @PostMapping
    public Pedido inserirPedido(@RequestBody Pedido pedido) {
        return pedidoService.inserirPedidos(pedido);
    }
}
