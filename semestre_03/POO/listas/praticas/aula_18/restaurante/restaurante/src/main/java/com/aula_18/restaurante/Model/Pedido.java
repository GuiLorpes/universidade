package com.aula_18.restaurante.Model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity
public class Pedido {
    @Id
    private int id; 
    private String item;


    public int getId() {
        return id;
    }
    public String getItem() {
        return item;
    }
}