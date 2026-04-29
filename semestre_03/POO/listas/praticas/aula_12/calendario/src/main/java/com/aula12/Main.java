package com.aula12;

import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        DiaSemana dia = DiaSemana.SEXTA;
        Atividade ativ1 = new Atividade("Estudar para POO", "10:30", dia); 

        System.out.println(DiaSemana.values()[0]);
        System.out.println(DiaSemana.QUARTA.ordinal());
        System.out.println(DiaSemana.values()[1]);

        NivelAcesso admin = NivelAcesso.ADMIN;
        NivelAcesso user = NivelAcesso.USUARIO;
        NivelAcesso leitor = NivelAcesso.LEITOR;
        System.out.println(admin);
        System.out.println(admin.getDescricao());

        ArrayList <NivelAcesso> lstUsers = new ArrayList<>();
        lstUsers.add(leitor);
        lstUsers.add(user);
        lstUsers.add(admin);

        for (NivelAcesso u : lstUsers) {
            if (u == NivelAcesso.ADMIN) {
                Atividade ativ2 = new Atividade("Estudar para ORD", "10:30", dia); 
                System.err.println("Atividade criada!");
            }
            else {
                System.out.println("Não possui permissão para essa ação");
            }
        }
    }
}