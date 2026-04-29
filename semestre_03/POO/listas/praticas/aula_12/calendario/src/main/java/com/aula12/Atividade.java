package com.aula12;

public class Atividade {
    private String descricao;
    private String hora;
    private DiaSemana dia;

    
    public Atividade(String descricao, String hora, DiaSemana dia) {
        this.descricao = descricao;
        this.hora = hora;
        this.dia = dia;
    }


    public String getDescricao() {
        return descricao;
    }
    public String getHora() {
        return hora;
    }
    public DiaSemana getDia() {
        return dia;
    } 


    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }
    public void setHora(String hora) {
        this.hora = hora;
    }
    public void setDia(DiaSemana dia) {
        this.dia = dia;
    }
}