package com.aula_18.restaurante.Repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.aula_18.restaurante.Model.Pedido;

public interface PedidoRepository extends JpaRepository<Pedido, Integer> {
    
}
