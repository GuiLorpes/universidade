package com.lista_05.vendas.Service;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.lista_05.vendas.Exception.Validacao;
import com.lista_05.vendas.Model.Produto;
import com.lista_05.vendas.Repository.ProdutoRepository;

@Service
public class ProdutoService {
    @Autowired
    private ProdutoRepository produtoRepository;

    public List<Produto> getAllProdutos() {
        return produtoRepository.findAll();
    }

    public Optional<Produto> getProdutoByID(long id) {
        return produtoRepository.findById(id);
    }

    public Produto postProduto(Produto produto) throws Validacao{
        validarProduto(produto);
        return produtoRepository.save(produto);
    }

    public Produto putProduto(long id, Produto produto) throws Validacao{
        produtoExiste(id);
        validarProduto(produto);
        return produtoRepository.saveAndFlush(produto);

    }

    public void deleteProduto(long id) throws Validacao{
        produtoExiste(id);
        produtoRepository.deleteById(id);
    }

    public void validarProduto(Produto produto) throws Validacao {
        boolean nomeVazio = produto.getNome() == null || 
                            produto.getNome().isBlank();
        boolean precoInvalido = produto.getPreco() <= 0.0;
        if (nomeVazio || precoInvalido) {
            throw new Validacao("Produto cadastrado inválido");
        }
    }
    public void produtoExiste(long id) throws Validacao {
        if (!produtoRepository.existsById(id)) {
            throw new Validacao("Produto de id: " + id + " não existe!");
        } 
    }
}
