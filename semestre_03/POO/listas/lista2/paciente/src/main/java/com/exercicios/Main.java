package com.exercicios;

public class Main {
    public static void main(String[] args) {
        Prontuario pront = new Prontuario(67, TipoSanguineo.B_POS, "Estudar");
        Paciente guilherme = new Paciente("Guilherme", 20, pront);
        guilherme.exibirPaciente();
    }
}