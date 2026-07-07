package com.lista_05.vendas.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.lista_05.vendas.Controller.OrcamentoRequest;
import com.lista_05.vendas.Exception.Validacao;
import com.lista_05.vendas.Model.Cliente;
import com.lista_05.vendas.Model.Orcamento;
import com.lista_05.vendas.Model.Produto;
import com.lista_05.vendas.Repository.ClienteRepository;
import com.lista_05.vendas.Repository.OrcamentoRepository;
import com.lista_05.vendas.Repository.ProdutoRepository;

@Service
public class OrcamentoService {
    @Autowired
    private OrcamentoRepository orcamentoRepository;
    @Autowired
    private ClienteRepository clienteRepository;
    private final ProdutoRepository produtoRepository;

    OrcamentoService(ProdutoRepository produtoRepository) {
        this.produtoRepository = produtoRepository;
    }

    public List<Orcamento> getAllOrcamentos() {
        return orcamentoRepository.findAll();
    }

    public Orcamento getOrcamentoByID(long id) throws Validacao {
        orcamentoExite(id);
        Optional<Orcamento> orcamento = orcamentoRepository.findById(id);
        return orcamento.get();
    }
    
    public Orcamento postOrcamento(OrcamentoRequest orcamentoRequest){
        Orcamento orcamento = new Orcamento();
        Optional<Cliente> cliente = clienteRepository.findById(orcamentoRequest.clienteId());
        if (!cliente.isPresent()) {
            throw new RuntimeException("Deve haver Cliente");
        }
        orcamento.setCliente(cliente.get());
        orcamento.setValor(orcamentoRequest.valor());
        List<Long> prodIds = orcamentoRequest.produtoIds();
        List<Produto> prods = new ArrayList<>();
        for (Long id : prodIds) {
            prods.add(produtoRepository.findById(id).orElse(null));
        }
        orcamento.setProdutos(prods);
        return orcamentoRepository.save(orcamento);
    }


    public void deleteOrcamento(long id) {
        orcamentoExite(id);
        orcamentoRepository.deleteById(id);
    }

    public Orcamento aprovarOrcamento(long id) {
        Orcamento orcamento = getOrcamentoByID(id);
        orcamento.aprovar();
        return orcamentoRepository.save(orcamento);
    }

    public Orcamento rejeitarOrcamento(long id) {
        Orcamento orcamento = getOrcamentoByID(id);
        orcamento.rejeitar();
        return orcamentoRepository.save(orcamento);
    }
    

    public void orcamentoExite(long id) throws Validacao {
        if (!orcamentoRepository.existsById(id)) {
            throw new Validacao("Orçamento de id: " + id + " não existe");
        }
    }
}
