package com.aula_16.spring.Controller;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/")
public class ProdutoController {
    
    @GetMapping
    public String getOrcamento() {
        return "Olá mundo!";
    }
    
    @PostMapping
    public String setOrcamento() {
        return "Orçamento criado";
    }

    @PutMapping
    public String putOrcamento() {
        return "Editar orçamento";
    }

    @DeleteMapping
    public String deleteOrcamento() {
        return "Orçamento excluido";
    }
}
