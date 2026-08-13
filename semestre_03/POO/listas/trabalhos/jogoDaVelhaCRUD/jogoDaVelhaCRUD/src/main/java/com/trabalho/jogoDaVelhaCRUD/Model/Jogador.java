package com.trabalho.jogoDaVelhaCRUD.Model;

import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Jogador {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String nome;

    @Enumerated(EnumType.STRING)
    private Simbolo simbolo;

    protected Jogador() {
        // construtor exigido pelo JPA
    }

    public Jogador(String nome, Simbolo simbolo) {
        this.nome = nome;
        this.simbolo = simbolo;
    }

    public Long getId() { return id; }
    public String getNome() { return nome; }
    public Simbolo getSimbolo() { return simbolo; }
    public void setNome(String nome) { this.nome = nome; }
    public void setSimbolo(Simbolo simbolo) { this.simbolo = simbolo; }
}
