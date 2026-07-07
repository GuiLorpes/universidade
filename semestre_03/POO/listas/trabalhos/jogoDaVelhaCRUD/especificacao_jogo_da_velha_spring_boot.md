# Especificação do Projeto — Jogo da Velha com Spring Boot

## 1. Apresentação

Desenvolver uma API REST para controlar partidas de jogo da velha entre dois jogadores humanos. A aplicação deverá permitir criar uma partida, registrar jogadas, consultar o tabuleiro e encerrar automaticamente o jogo quando houver vitória ou empate.

O projeto deverá aplicar conceitos de programação orientada a objetos e ser organizado em camadas utilizando Spring Boot, Spring Web, Spring Data JPA e banco de dados H2.

---

## 2. Objetivos de aprendizagem

- praticar classes, objetos, atributos, métodos e encapsulamento;
- representar estados por meio de `enum`;
- separar responsabilidades em camadas;
- criar endpoints REST;
- implementar regras de negócio no `service`;
- persistir dados com Spring Data JPA e H2;
- tratar erros e retornar códigos HTTP adequados.

---

## 3. Regras do jogo

1. A partida possui dois jogadores.
2. O primeiro jogador utiliza o símbolo `X`.
3. O segundo jogador utiliza o símbolo `O`.
4. O tabuleiro possui três linhas e três colunas.
5. Linhas e colunas devem ser identificadas pelos valores `0`, `1` e `2`.
6. O jogador com símbolo `X` realiza a primeira jogada.
7. Os jogadores alternam os turnos após cada jogada válida.
8. Uma posição ocupada não pode receber outra jogada.
9. Vence quem preencher uma linha, uma coluna ou uma diagonal com o próprio símbolo.
10. A partida termina empatada quando as nove posições forem preenchidas sem vencedor.
11. Não é permitido jogar em uma partida encerrada.

---

## 4. Requisitos funcionais

### RF01 — Criar partida

O sistema deve permitir a criação de uma partida informando o nome de dois jogadores.

### RF02 — Associar símbolos

Ao criar a partida, o sistema deve associar automaticamente:

- `X` ao jogador 1;
- `O` ao jogador 2.

### RF03 — Consultar partida

O sistema deve permitir consultar uma partida por seu identificador, retornando os jogadores, o tabuleiro, o jogador da vez, o status e o vencedor, quando existir.

### RF04 — Listar partidas

O sistema deve permitir listar todas as partidas cadastradas.

### RF05 — Registrar jogada

O sistema deve permitir registrar uma jogada por meio da linha e da coluna escolhidas.

### RF06 — Validar jogada

O sistema deve rejeitar uma jogada quando:

- a linha ou a coluna estiver fora do intervalo de `0` a `2`;
- a posição já estiver ocupada;
- não for a vez do jogador informado;
- a partida não existir;
- a partida já estiver encerrada.

### RF07 — Alternar turno

Depois de uma jogada válida, caso a partida continue, o sistema deve passar o turno ao outro jogador.

### RF08 — Verificar vitória

Após cada jogada válida, o sistema deve verificar todas as linhas, colunas e diagonais. Quando houver vitória, deve registrar o vencedor e alterar o status da partida para `VITORIA`.

### RF09 — Verificar empate

Quando todas as posições estiverem ocupadas e não houver vencedor, o sistema deve alterar o status para `EMPATE`.

### RF10 — Excluir partida

O sistema deve permitir excluir uma partida pelo seu identificador.

---

## 5. Requisitos técnicos

- utilizar Java 17 ou superior;
- utilizar Spring Boot;
- utilizar Spring Web para os endpoints REST;
- utilizar Spring Data JPA para persistência;
- utilizar o banco de dados H2;
- utilizar Maven para gerenciamento do projeto;
- separar a aplicação nos pacotes `model`, `repository`, `service`, `controller` e `exception`;
- não colocar regras de negócio no controller;
- utilizar injeção de dependência por construtor;
- retornar respostas no formato JSON;
- validar os dados recebidos pela API.

---

## 6. Modelo de domínio

### 6.1 Enum `Simbolo`

Representa os símbolos utilizados pelos jogadores.

```java
public enum Simbolo {
    X, O
}
```

### 6.2 Enum `StatusPartida`

Representa o estado atual de uma partida.

```java
public enum StatusPartida {
    EM_ANDAMENTO,
    VITORIA,
    EMPATE
}
```

### 6.3 Classe `Jogador`

| Atributo | Tipo | Regra |
|---|---|---|
| `id` | `Long` | Identificador gerado automaticamente |
| `nome` | `String` | Obrigatório e não pode estar em branco |
| `simbolo` | `Simbolo` | Deve ser `X` ou `O` |

### 6.4 Classe `Partida`

| Atributo | Tipo | Regra |
|---|---|---|
| `id` | `Long` | Identificador gerado automaticamente |
| `jogadorX` | `Jogador` | Jogador que utiliza `X` |
| `jogadorO` | `Jogador` | Jogador que utiliza `O` |
| `tabuleiro` | `String` | Estado das nove posições do tabuleiro |
| `turnoAtual` | `Simbolo` | Símbolo que deve realizar a próxima jogada |
| `status` | `StatusPartida` | Estado atual da partida |
| `vencedor` | `Jogador` | Nulo enquanto não houver vencedor |

O tabuleiro pode ser persistido como uma `String` com nove caracteres. O caractere `-` representa uma posição vazia.

Exemplo:

```text
X-O-X----
```

Representação visual:

```text
X | - | O
---------
- | X | -
---------
- | - | -
```

### 6.5 Comportamentos esperados no domínio

A classe `Partida`, ou uma classe específica de domínio chamada `Tabuleiro`, deve possuir métodos para:

- consultar uma posição;
- verificar se uma posição está livre;
- marcar uma posição;
- verificar linhas, colunas e diagonais;
- identificar se o tabuleiro está completo;
- alternar o turno.

---

## 7. Arquitetura em camadas

```text
Requisição HTTP
      ↓
Controller
      ↓
Service
      ↓
Repository
      ↓
Banco H2
```

### `controller`

Recebe as requisições HTTP, valida os dados de entrada e chama o service. Não deve decidir se uma jogada produz vitória ou empate.

### `service`

Concentra o fluxo e as regras de negócio: criação da partida, validação de jogadas, alternância de turno, verificação de vitória e empate.

### `repository`

Realiza o acesso ao banco de dados por meio de interfaces que estendem `JpaRepository`.

### `model`

Contém as entidades, enums e comportamentos do domínio.

### `exception`

Contém as exceções do sistema e o tratador global de erros.

---

## 8. Estrutura sugerida de pacotes

```text
src/main/java/com/exemplo/jogovelha
├── JogoVelhaApplication.java
├── controller
│   └── PartidaController.java
├── exception
│   ├── JogadaInvalidaException.java
│   ├── PartidaEncerradaException.java
│   ├── PartidaNaoEncontradaException.java
│   └── ApiExceptionHandler.java
├── model
│   ├── Jogador.java
│   ├── Partida.java
│   ├── Simbolo.java
│   └── StatusPartida.java
├── repository
│   └── PartidaRepository.java
└── service
    └── PartidaService.java
```

---

## 9. Contrato da API REST

### 9.1 Criar uma partida

```http
POST /partidas?nomeJogadorX=Ana&nomeJogadorO=Bruno
```

Os nomes devem ser recebidos no controller com `@RequestParam`:

```java
@PostMapping
public ResponseEntity<Partida> criar(
        @RequestParam String nomeJogadorX,
        @RequestParam String nomeJogadorO) {
    // chamar o service
}
```

Resposta esperada: `201 Created`, contendo a partida criada.

### 9.2 Listar partidas

```http
GET /partidas
```

Resposta esperada: `200 OK`.

### 9.3 Consultar uma partida

```http
GET /partidas/{id}
```

Resposta esperada: `200 OK`.

Se a partida não existir, retornar `404 Not Found`.

### 9.4 Realizar uma jogada

```http
POST /partidas/{id}/jogadas?simbolo=X&linha=0&coluna=1
```

Os dados da jogada devem ser recebidos com `@RequestParam`:

```java
@PostMapping("/{id}/jogadas")
public ResponseEntity<Partida> jogar(
        @PathVariable Long id,
        @RequestParam Simbolo simbolo,
        @RequestParam int linha,
        @RequestParam int coluna) {
    // chamar o service
}
```

Resposta esperada: `200 OK`, contendo o novo estado da partida.

### 9.5 Excluir uma partida

```http
DELETE /partidas/{id}
```

Resposta esperada: `204 No Content`.

---

## 10. Exemplo de resposta da API

Nesta atividade, os controllers podem retornar diretamente objetos do tipo `Partida`. O Spring Boot transforma esses objetos em JSON automaticamente.

```json
{
  "id": 1,
  "jogadorX": {
    "nome": "Ana",
    "simbolo": "X"
  },
  "jogadorO": {
    "nome": "Bruno",
    "simbolo": "O"
  },
  "tabuleiro": [
    ["X", null, "O"],
    [null, "X", null],
    [null, null, null]
  ],
  "turnoAtual": "O",
  "status": "EM_ANDAMENTO",
  "vencedor": null
}
```

---

## 11. Tratamento de erros

A API deve retornar erros em JSON, com mensagem clara e código HTTP adequado.

| Situação | Código HTTP |
|---|---:|
| Dados obrigatórios ausentes ou inválidos | `400 Bad Request` |
| Linha ou coluna fora do tabuleiro | `400 Bad Request` |
| Posição já ocupada | `409 Conflict` |
| Jogador tentou jogar fora do seu turno | `409 Conflict` |
| Tentativa de jogar em partida encerrada | `409 Conflict` |
| Partida não encontrada | `404 Not Found` |

Exemplo:

```json
{
  "status": 409,
  "erro": "Conflito",
  "mensagem": "A posição informada já está ocupada"
}
```

O tratamento deve ser centralizado em uma classe anotada com `@RestControllerAdvice`.

---

## 12. Configuração esperada do H2

Exemplo de `application.properties`:

```properties
spring.datasource.url=jdbc:h2:mem:jogovelhodb
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.hibernate.ddl-auto=update
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console
```

Console do H2:

```text
http://localhost:8080/h2-console
```

---

## 13. Fluxo de uma jogada

1. O controller recebe o identificador da partida, o símbolo, a linha e a coluna.
2. O service busca a partida no repository.
3. O sistema verifica se a partida está em andamento.
4. O sistema verifica se o símbolo informado corresponde ao turno atual.
5. O sistema valida os limites da linha e da coluna.
6. O sistema verifica se a posição está livre.
7. O símbolo é colocado no tabuleiro.
8. O sistema verifica se houve vitória.
9. Se não houve vitória, o sistema verifica se houve empate.
10. Se a partida continuar, o turno é alternado.
11. O novo estado é salvo no banco e devolvido ao cliente.

---

## 14. Testes mínimos

Devem ser implementados testes para verificar:

- criação de uma partida com dados válidos;
- rejeição de nome vazio;
- primeira jogada realizada por `X`;
- alternância correta dos turnos;
- rejeição de linha ou coluna inválida;
- rejeição de posição ocupada;
- rejeição de jogada fora do turno;
- vitória em uma linha;
- vitória em uma coluna;
- vitória na diagonal principal;
- vitória na diagonal secundária;
- empate;
- rejeição de jogada após o encerramento;
- consulta de partida inexistente.

---

## 15. Critérios de aceite

O projeto será considerado concluído quando:

1. iniciar sem erros por meio do Maven;
2. criar e armazenar partidas no H2;
3. expor todos os endpoints definidos nesta especificação;
4. impedir todas as jogadas inválidas descritas;
5. alternar os jogadores corretamente;
6. reconhecer vitórias nas oito combinações possíveis;
7. reconhecer uma situação de empate;
8. retornar códigos HTTP coerentes;
9. manter as regras de negócio fora do controller;
10. possuir testes automatizados nos endpoints;