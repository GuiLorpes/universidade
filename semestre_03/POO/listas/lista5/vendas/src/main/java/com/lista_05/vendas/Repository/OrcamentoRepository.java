package com.lista_05.vendas.Repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.lista_05.vendas.Model.Orcamento;

public interface OrcamentoRepository extends JpaRepository<Orcamento, Long> {
    
}
