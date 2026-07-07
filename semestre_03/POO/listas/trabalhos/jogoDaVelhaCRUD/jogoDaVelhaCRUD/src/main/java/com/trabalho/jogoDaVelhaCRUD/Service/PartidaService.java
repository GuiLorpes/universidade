package com.trabalho.jogoDaVelhaCRUD.Service;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import com.trabalho.jogoDaVelhaCRUD.Excecao.*;
import com.trabalho.jogoDaVelhaCRUD.Model.*;
import com.trabalho.jogoDaVelhaCRUD.Repository.PartidaRepository;

@Service
public class PartidaService {

    private final PartidaRepository partidaRepository;

    public PartidaService(PartidaRepository partidaRepository) {
        this.partidaRepository = partidaRepository;
    }

    public Partida criarPartida(String nomeJogadorX, String nomeJogadorO) {
        if (nomeJogadorX == null || nomeJogadorX.isBlank()) {
            throw new DadosInvalidosException("O nome do jogador X não pode estar em branco.");
        }
        if (nomeJogadorO == null || nomeJogadorO.isBlank()) {
            throw new DadosInvalidosException("O nome do jogador O não pode estar em branco.");
        }

        Jogador jogadorX = new Jogador(nomeJogadorX, Simbolo.X);
        Jogador jogadorO = new Jogador(nomeJogadorO, Simbolo.O);

        Partida partida = new Partida(jogadorX, jogadorO);

        return partidaRepository.save(partida);
    }

    public List<Partida> listarPartidas() {
        return partidaRepository.findAll();
    }

    public Partida buscarPartida(Long id) {
        return partidaRepository.findById(id)
                .orElseThrow(() -> new PartidaNaoEncontradaException("Partida com id " + id + " não encontrada."));
    }

    public Partida jogar(Long id, Simbolo simbolo, int linha, int coluna) {
        Partida partida = buscarPartida(id);

        if (partida.getStatus() != StatusPartida.EM_ANDAMENTO) {
            throw new PartidaEncerradaException("Não é possível jogar em uma partida já encerrada.");
        }

        if (partida.getTurnoAtual() != simbolo) {
            throw new JogadaInvalidaException("Não é a vez do símbolo " + simbolo + ".", HttpStatus.CONFLICT);
        }

        if (linha < 0 || linha > 2 || coluna < 0 || coluna > 2) {
            throw new JogadaInvalidaException("Linha e coluna devem estar entre 0 e 2.");
        }

        if (!partida.posicaoLivre(linha, coluna)) {
            throw new JogadaInvalidaException("A posição informada já está ocupada.", HttpStatus.CONFLICT);
        }

        partida.marcarPosicao(linha, coluna, simbolo);

        Simbolo vencedorSimbolo = partida.verificarVencedor();

        if (vencedorSimbolo != null) {
            Jogador vencedor = (vencedorSimbolo == Simbolo.X) ? partida.getJogadorX() : partida.getJogadorO();
            partida.setVencedor(vencedor);
            partida.setStatus(StatusPartida.VITORIA);
        } else if (partida.tabuleiroCompleto()) {
            partida.setStatus(StatusPartida.EMPATE);
        } else {
            partida.alternarTurno();
        }

        return partidaRepository.save(partida);
    }

    public void excluir(Long id) {
        Partida partida = buscarPartida(id);
        partidaRepository.delete(partida);
    }
}