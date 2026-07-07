package com.trabalho.jogoDaVelhaCRUD.Model;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToOne;

@Entity
public class Partida {

    private static final String TABULEIRO_VAZIO = "---------";

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "jogador_x_id")
    private Jogador jogadorX;

    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "jogador_o_id")
    private Jogador jogadorO;

    private String tabuleiro;

    @Enumerated(EnumType.STRING)
    private Simbolo turnoAtual;

    @Enumerated(EnumType.STRING)
    private StatusPartida status;

    @ManyToOne
    @JoinColumn(name = "vencedor_id")
    private Jogador vencedor;

    protected Partida() {
        // construtor exigido pelo JPA
    }

    public Partida(Jogador jogadorX, Jogador jogadorO) {
        this.jogadorX = jogadorX;
        this.jogadorO = jogadorO;
        this.tabuleiro = TABULEIRO_VAZIO;
        this.turnoAtual = Simbolo.X;
        this.status = StatusPartida.EM_ANDAMENTO;
    }

    // ---------- comportamentos do tabuleiro ----------

    private int index(int linha, int coluna) {
        return linha * 3 + coluna;
    }

    public char consultarPosicao(int linha, int coluna) {
        return tabuleiro.charAt(index(linha, coluna));
    }

    public boolean posicaoLivre(int linha, int coluna) {
        return consultarPosicao(linha, coluna) == '-';
    }

    public void marcarPosicao(int linha, int coluna, Simbolo simbolo) {
        StringBuilder sb = new StringBuilder(tabuleiro);
        sb.setCharAt(index(linha, coluna), simbolo.name().charAt(0));
        this.tabuleiro = sb.toString();
    }

    public boolean tabuleiroCompleto() {
        return !tabuleiro.contains("-");
    }

    public void alternarTurno() {
        this.turnoAtual = (turnoAtual == Simbolo.X) ? Simbolo.O : Simbolo.X;
    }

    public Simbolo verificarVencedor() {
        int[][] combinacoes = {
                {0, 1, 2}, {3, 4, 5}, {6, 7, 8}, // linhas
                {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, // colunas
                {0, 4, 8}, {2, 4, 6}             // diagonais
        };

        for (int[] combinacao : combinacoes) {
            char a = tabuleiro.charAt(combinacao[0]);
            char b = tabuleiro.charAt(combinacao[1]);
            char c = tabuleiro.charAt(combinacao[2]);

            if (a != '-' && a == b && b == c) {
                return Simbolo.valueOf(String.valueOf(a));
            }
        }
        return null;
    }

    // ---------- getters e setters ----------

    public Long getId() { return id; }
    public Jogador getJogadorX() { return jogadorX; }
    public Jogador getJogadorO() { return jogadorO; }
    public String getTabuleiro() { return tabuleiro; }
    public Simbolo getTurnoAtual() { return turnoAtual; }
    public StatusPartida getStatus() { return status; }
    public Jogador getVencedor() { return vencedor; }

    public void setStatus(StatusPartida status) { this.status = status; }
    public void setVencedor(Jogador vencedor) { this.vencedor = vencedor; }
    
}

