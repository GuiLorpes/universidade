package com.lista_05.vendas.Service;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.lista_05.vendas.Exception.Validacao;
import com.lista_05.vendas.Model.Cliente;
import com.lista_05.vendas.Repository.ClienteRepository;

@Service
public class ClienteService {
    @Autowired
    private ClienteRepository clienteRepository;

    public List<Cliente> getAllClientes() {
        return clienteRepository.findAll();
    }

    public Optional<Cliente> getClienteID(long id) {
        return clienteRepository.findById(id);
    }

    public Optional<Cliente> findByEmail(String email) {
        return clienteRepository.findByEmail(email);
    }

    public Cliente postCliente(Cliente cliente) throws Validacao{
        validarCliente(cliente);
        return clienteRepository.save(cliente);
    }

    public Cliente putCliente(long id, Cliente cliente) throws Validacao{
        clienteExiste(id);
        validarCliente(cliente);
        return clienteRepository.saveAndFlush(cliente);
    }

    public void deleteClienteID(long id) throws Validacao {
        clienteExiste(id);
        clienteRepository.deleteById(id);;
    }


    public void validarCliente(Cliente cliente) throws Validacao {
        boolean nomeVazio = cliente.getNome() == null || 
                            cliente.getNome().isBlank();
        boolean emailVazio = cliente.getEmail() == null || 
                            cliente.getEmail().isBlank();
        if (nomeVazio || emailVazio) {
            throw new Validacao("Cadastro de cliente inválido!");
        }
    }

    public void clienteExiste(long id) throws Validacao {
        if (!clienteRepository.existsById(id)) {
            throw new Validacao("Cliente de id: " + id + " não existe!");
        }
    }
}
