package com.lista_05.vendas.Controller;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.lista_05.vendas.Exception.Validacao;
import com.lista_05.vendas.Model.Produto;
import com.lista_05.vendas.Service.ProdutoService;

@RestController
@RequestMapping("/produtos")
public class ProdutoController {
    @Autowired
    private ProdutoService produtoService;
    
    @GetMapping
    public List<Produto> getAllProdutos() {
        return produtoService.getAllProdutos();
    }

    @GetMapping("/id:{id}")
    public Optional<Produto> getProdutoByID(@PathVariable long id) {
        return produtoService.getProdutoByID(id);
    }

    @PostMapping
    public Produto postProduto(@RequestBody Produto produto) throws Validacao {
        return produtoService.postProduto(produto);
    }

    @PutMapping("/id:{id}")
    public Produto putProduto(@PathVariable long id, @RequestBody Produto produto) throws Validacao {
        return produtoService.putProduto(id, produto);
    }

    @DeleteMapping("/id:{id}")
    public void deleteProduto(@PathVariable long id) throws Validacao {
        produtoService.deleteProduto(id);
    }
}
