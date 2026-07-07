package com.lista_05.vendas.Model;

import java.util.List;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.ManyToOne;

@Entity
public class Orcamento {
    @Id
    private int id;
    private double valor;
    private StatusOrcamento status = StatusOrcamento.PENDENTE;
    @ManyToOne
    private Cliente cliente;
    @ManyToMany 
    private List<Produto> produtos;

    
    public int getId() {
        return id;
    }
    public double getValor() {
        return valor;
    }
    public StatusOrcamento getStatus() {
        return status;
    }
    public Cliente getCliente() {
        return cliente;
    }
    public List<Produto> getProdutos() {
        return produtos;
    }


    public void setId(int id) {
        this.id = id;
    }
    public void setValor(double valor) {
        this.valor = valor;
    }
    public void setStatus(StatusOrcamento status) {
        this.status = status;
    }
    public void setCliente(Cliente cliente) {
        this.cliente = cliente;
    }
    public void setProdutos(List<Produto> produtos) {
        this.produtos = produtos;
    }
    

    public void aprovar() {
        this.status = StatusOrcamento.APROVADO;
    }
    public void rejeitar() {
        this.status = StatusOrcamento.REJEITADO;
    }

    public double calcularValorTotal() {
        double total = 0.0;
        for (Produto p : produtos) {
            total += p.getPreco();
        }
        return total;
    }
}
