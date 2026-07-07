package com.lista_05.vendas.Controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.lista_05.vendas.Exception.Validacao;
import com.lista_05.vendas.Model.Orcamento;
import com.lista_05.vendas.Repository.ClienteRepository;
import com.lista_05.vendas.Service.OrcamentoService;

@RestController
@RequestMapping("/orcamentos")
public class OrcamentoController {
    @Autowired
    private OrcamentoService orcamentoService;
    private final ClienteRepository clienteRepository;

    OrcamentoController(ClienteRepository clienteRepository) {
        this.clienteRepository = clienteRepository;
    }

    @GetMapping
    public List<Orcamento> getAllOrcamentos() {
        return orcamentoService.getAllOrcamentos();
    }

    @GetMapping("/id:{id}")
    public Orcamento getOrcamentoByID(@PathVariable long id) throws Validacao{
        return orcamentoService.getOrcamentoByID(id);
    }
    
    @PostMapping
    public ResponseEntity<Orcamento> postOrcamento(@RequestBody OrcamentoRequest orcamentoRequest) {
        Orcamento orcamento = orcamentoService.postOrcamento(orcamentoRequest);
        return ResponseEntity.status(HttpStatus.CREATED).body(orcamento);
    }

    @DeleteMapping("/id:{id}")
    public void deleteOrcamento(@PathVariable long id) throws Validacao {
        orcamentoService.deleteOrcamento(id);
    }

    @PutMapping("/id:{id}/aprovar")
    public Orcamento aprovarOrcamento(@PathVariable long id) {
        return orcamentoService.aprovarOrcamento(id);
    }

    @PutMapping("/id:{id}/rejeitar")
    public Orcamento rejeitarOrcamento(@PathVariable long id) {
        return orcamentoService.rejeitarOrcamento(id);
    }
    
}
