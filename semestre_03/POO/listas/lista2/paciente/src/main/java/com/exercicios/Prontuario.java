package com.exercicios;

public class Prontuario {
    private int numRegistro;
    private TipoSanguineo tipoSanguineo;
    private String alergias;


    public Prontuario(int numRegistro, TipoSanguineo tipoSanguineo, String alergias) {
        this.numRegistro = numRegistro;
        this.tipoSanguineo = tipoSanguineo;
        this.alergias = alergias;
    }


    public int getNumRegistro() {
        return numRegistro;
    }
    public TipoSanguineo getTipoSanguineo() {
        return tipoSanguineo;
    }
    public String getAlergias() {
        return alergias;
    }


    public void setNumRegistro(int numRegistro) {
        this.numRegistro = numRegistro;
    }
    public void setTipoSanguineo(TipoSanguineo tipoSanguineo) {
        this.tipoSanguineo = tipoSanguineo;
    }
    public void setAlergias(String alergias) {
        this.alergias = alergias;
    }
    
    
}
