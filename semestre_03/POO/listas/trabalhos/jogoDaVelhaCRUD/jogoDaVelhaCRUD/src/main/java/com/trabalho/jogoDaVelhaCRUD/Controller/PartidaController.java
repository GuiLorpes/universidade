package com.trabalho.jogoDaVelhaCRUD.Controller;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.trabalho.jogoDaVelhaCRUD.Model.Partida;
import com.trabalho.jogoDaVelhaCRUD.Model.Simbolo;
import com.trabalho.jogoDaVelhaCRUD.Service.PartidaService;

@RestController
@RequestMapping("/partidas")
public class PartidaController {

    private final PartidaService partidaService;

    public PartidaController(PartidaService partidaService) {
        this.partidaService = partidaService;
    }

    @PostMapping
    public ResponseEntity<Partida> criar(
            @RequestParam String nomeJogadorX,
            @RequestParam String nomeJogadorO) {
        Partida partida = partidaService.criarPartida(nomeJogadorX, nomeJogadorO);
        return ResponseEntity.status(HttpStatus.CREATED).body(partida);
    }

    @GetMapping
    public ResponseEntity<List<Partida>> listar() {
        return ResponseEntity.ok(partidaService.listarPartidas());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Partida> buscar(@PathVariable Long id) {
        return ResponseEntity.ok(partidaService.buscarPartida(id));
    }

    @PostMapping("/{id}/jogadas")
    public ResponseEntity<Partida> jogar(
            @PathVariable Long id,
            @RequestParam Simbolo simbolo,
            @RequestParam int linha,
            @RequestParam int coluna) {
        Partida partida = partidaService.jogar(id, simbolo, linha, coluna);
        return ResponseEntity.ok(partida);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> excluir(@PathVariable Long id) {
        partidaService.excluir(id);
        return ResponseEntity.noContent().build();
    }
}
