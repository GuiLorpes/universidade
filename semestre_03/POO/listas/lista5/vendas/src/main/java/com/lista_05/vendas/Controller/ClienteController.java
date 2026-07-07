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
import com.lista_05.vendas.Model.Cliente;
import com.lista_05.vendas.Service.ClienteService;

@RestController
@RequestMapping("/clientes")
public class ClienteController {
    @Autowired
    private ClienteService clienteService;

    @GetMapping // funciona
    public List<Cliente> getAllClientes() {
        return clienteService.getAllClientes();
    }
    
    @GetMapping("/{id}")
    public Optional<Cliente> getClienteID(@PathVariable long id) {
        return clienteService.getClienteID(id);
    }

    @GetMapping("/{email}")
    public Optional<Cliente> findByEmail(@PathVariable String email) {
        return clienteService.findByEmail(email);
    }

    @PostMapping // funciona
    public Cliente postCliente(@RequestBody Cliente cliente) throws Validacao{
        return clienteService.postCliente(cliente);
    }

    @DeleteMapping("/{id}")
    public void deleteClienteID(@PathVariable long id) throws Validacao {
        clienteService.deleteClienteID(id);;
    }

    @PutMapping("/{id}")
    public Cliente putCliente(@PathVariable long id, @RequestBody Cliente cliente) throws Validacao{
        return clienteService.putCliente(id, cliente);
    } 
}
