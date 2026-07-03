# Atividade prática: CRUD com Spring Boot, H2 e orientação a objetos

Esta atividade deve ser desenvolvida a partir do projeto da semana 15:

```text
aulas/SEMANA15/crud+completo
```

O projeto atual já possui uma API Spring Boot com banco H2, JPA e duas entidades principais:

- `Produto`
- `Orcamento`

A proposta desta lista é evoluir o projeto aos poucos, passando pelo CRUD completo e reforçando conceitos de orientação a objetos, como classe, objeto, encapsulamento, associação, enum, responsabilidade de classe e regras de negócio.

---

# 1. Como organizar o projeto

Antes de iniciar os exercícios, o aluno deve manter o projeto organizado em camadas.

A estrutura principal deve seguir este formato:

```text
src/main/java/com/example/crudproject
├── controller
├── model
├── repository
├── service
└── CrudprojectApplication.java
```

## Pacote `model`

Neste pacote ficam as classes que representam os objetos principais do sistema.

Exemplos:

```text
model
├── Produto.java
├── Orcamento.java
├── Cliente.java
└── StatusOrcamento.java
```

As classes deste pacote devem representar entidades do domínio do problema.

Exemplos de responsabilidades:

- guardar atributos;
- representar estados;
- possuir métodos de comportamento;
- receber anotações como `@Entity`, `@Id` e `@GeneratedValue` (pesquisar esse item).

## Pacote `repository`

Neste pacote ficam as interfaces responsáveis pelo acesso ao banco de dados.

Exemplos:

```text
repository
├── ProdutoRepository.java
├── OrcamentoRepository.java
└── ClienteRepository.java
```

Cada entidade normalmente possui um repository.

Exemplo:

```java
public interface ClienteRepository extends JpaRepository<Cliente, Long> {
}
```

## Pacote `service`

Neste pacote ficam as classes que concentram as regras de negócio.

Exemplos:

```text
service
├── ProdutoService.java
├── OrcamentoService.java
└── ClienteService.java
```

Você deve evitar colocar regra de negócio diretamente no controller.

Exemplos de regras que devem ficar no service:

- verificar se um objeto existe antes de atualizar;
- impedir preço negativo;
- aprovar ou rejeitar orçamento;
- buscar um registro por `id`;
- chamar o repository para salvar, listar, atualizar ou deletar.

## Pacote `controller`

Neste pacote ficam as classes que recebem as requisições HTTP.

Exemplos:

```text
controller
├── ProdutoController.java
├── OrcamentoController.java
└── ClienteController.java
```

Os controllers devem expor os endpoints da API.

Exemplos:

```text
GET    /produtos
POST   /produtos
GET    /produtos/{id}
PUT    /produtos/{id}
DELETE /produtos/{id}
```

O controller deve chamar o service, e o service deve chamar o repository.

Fluxo esperado:

```text
Requisição HTTP
→ Controller
→ Service
→ Repository
→ Banco H2
```

---

# 2. Regras gerais para resolver a lista

Para cada exercício, você deve seguir três etapas.

## Etapa 1: interpretação

Antes de escrever código, responder:

1. Quais classes aparecem no problema?
2. Quais atributos são necessários?
3. Qual pacote deve receber cada classe?
4. Quais endpoints serão necessários?
5. Existe alguma regra de negócio?
6. Essa regra deve ficar no controller, no service ou no model?
7. Existe algum relacionamento entre classes?
8. Existe algum estado que pode virar `enum`?

## Etapa 2: implementação

Implementar a solução respeitando as camadas:

- `model`: entidades e enums;
- `repository`: acesso ao banco;
- `service`: regras de negócio;
- `controller`: endpoints HTTP.

## Etapa 3: teste

Testar os endpoints usando Bruno, Postman, Insomnia ou outra ferramenta semelhante.

Também é possível acessar o console do H2, se ele estiver habilitado:

```text
http://localhost:8080/h2-console
```

Configuração esperada:

```text
JDBC URL: jdbc:h2:mem:testdb
User: sa
Password:
```

---

# 3. Lista de atividades

## Exercício 1: entender o projeto atual

### Objetivo

Identificar a função de cada camada no projeto da semana 15.

### O que fazer

Analise as classes:

- `Produto`
- `Orcamento`
- `ProdutoRepository`
- `OrcamentoRepository`
- `ProdutoService`
- `OrcamentoService`
- `ProdutoController`
- `OrcamentoController`

### O que responder

1. Qual classe representa uma entidade?
2. Qual classe recebe requisições HTTP?
3. Qual classe possui regras de negócio?
4. Qual interface conversa com o banco?
5. Qual endpoint cria um orçamento?
6. Qual endpoint lista produtos?

---

## Exercício 2: completar o CRUD de Produto

### Objetivo

Completar a entidade `Produto`, que atualmente possui apenas cadastro e listagem no controller.

### O que fazer

Criar os seguintes endpoints:

```text
GET    /produtos
POST   /produtos
GET    /produtos/{id}
PUT    /produtos/{id}
DELETE /produtos/{id}
```

### Regras

- O produto deve ter `nome` e `preco`.
- Não permitir produto com preço menor ou igual a zero.
- Ao atualizar, buscar o produto existente antes de salvar.

### Conceitos trabalhados

- CRUD completo;
- encapsulamento;
- alteração de estado de um objeto;
- responsabilidade do service.

---

## Exercício 3: criar a entidade Cliente

### Objetivo

Criar uma nova entidade do zero.

### O que fazer

Criar a classe `Cliente` no pacote `model`.

Ela deve possuir:

```text
id
nome
email
telefone
```

### Depois criar

```text
ClienteRepository
ClienteService
ClienteController
```

### Endpoints

```text
GET    /clientes
POST   /clientes
GET    /clientes/{id}
PUT    /clientes/{id}
DELETE /clientes/{id}
```

### Conceitos trabalhados

- criação de classe;
- atributos;
- objetos enviados por JSON;
- organização em camadas.

---

## Exercício 4: adicionar validações no cadastro de Cliente

### Objetivo

Adicionar regras de negócio no service.

### Regras

- O nome do cliente não pode ser vazio.
- O email do cliente não pode ser vazio.
- O telefone pode ser opcional.

### Onde implementar

As validações devem ficar no `ClienteService`.

### Conceitos trabalhados

- regra de negócio;
- validação;
- responsabilidade de classe.

---

## Exercício 5: buscar Cliente por email

### Objetivo

Criar uma consulta personalizada usando Spring Data JPA.

### O que fazer

No `ClienteRepository`, criar um método para buscar cliente por email.

Exemplo:

```java
Optional<Cliente> findByEmail(String email);
```

Depois, criar um endpoint:

```text
GET /clientes/email/{email}
```

### Conceitos trabalhados

- interfaces;
- métodos declarativos;
- busca personalizada;
- uso de `Optional`.

---

## Exercício 6: melhorar o status de Orcamento com enum

### Objetivo

Substituir o status em texto por um `enum`.

### O que fazer

Criar o enum `StatusOrcamento`:

```java
public enum StatusOrcamento {
    PENDENTE,
    APROVADO,
    REJEITADO
}
```

Alterar a classe `Orcamento` para usar:

```java
private StatusOrcamento status = StatusOrcamento.PENDENTE;
```

### Conceitos trabalhados

- enum;
- controle de estados;
- redução de erro por texto livre.

---

## Exercício 7: criar comportamentos na classe Orcamento

### Objetivo

Fazer a entidade `Orcamento` ter comportamento próprio.

### O que fazer

Na classe `Orcamento`, criar métodos:

```java
public void aprovar() {
    this.status = StatusOrcamento.APROVADO;
}

public void rejeitar() {
    this.status = StatusOrcamento.REJEITADO;
}
```

Depois, alterar o `OrcamentoService` para chamar:

```java
orcamento.aprovar();
```

em vez de:

```java
orcamento.setStatus("Aprovado");
```

### Conceitos trabalhados

- objeto com comportamento;
- encapsulamento;
- métodos de domínio.

---

## Exercício 8: criar endpoint para rejeitar orçamento

### Objetivo

Adicionar uma nova ação de negócio.

### O que fazer

Criar o endpoint:

```text
PUT /orcamento/{id}/rejeitar
```

### Regras

- Buscar o orçamento pelo `id`.
- Alterar o status para `REJEITADO`.
- Salvar o orçamento.

### Conceitos trabalhados

- métodos específicos além do CRUD;
- ação de negócio;
- reutilização da busca por `id`.

---

## Exercício 9: relacionar Orcamento com Cliente

### Objetivo

Criar uma associação entre objetos.

### O que fazer

Alterar `Orcamento` para possuir um cliente.

Exemplo:

```java
@ManyToOne
private Cliente cliente;
```

### Regras

- Um orçamento deve pertencer a um cliente.
- Ao criar um orçamento, deve ser possível informar o cliente.

### Conceitos trabalhados

- associação;
- relacionamento entre entidades;
- objetos conectados no banco de dados.

---

## Exercício 10: relacionar Orcamento com Produto

### Objetivo

Relacionar orçamento e produto.

### Primeira versão

Um orçamento possui um produto:

```java
@ManyToOne
private Produto produto;
```

### Segunda versão

Depois, evoluir para um orçamento possuir vários produtos:

```java
@ManyToMany
private List<Produto> produtos;
```

### Conceitos trabalhados

- associação;
- listas de objetos;
- relacionamento entre entidades;
- evolução de modelo.

---

## Exercício 11: calcular o valor total do orçamento

### Objetivo

Fazer o valor do orçamento ser calculado a partir dos produtos.

### O que fazer

Criar um método na classe `Orcamento`:

```java
public double calcularValorTotal() {
    // somar os preços dos produtos
}
```

### Regras

- O valor total não deve ser digitado manualmente.
- O valor deve vir da soma dos produtos.

### Conceitos trabalhados

- método com retorno;
- comportamento dentro da entidade;
- cálculo a partir do estado do objeto.

---

## Exercício 12: criar consultas por status

### Objetivo

Buscar orçamentos de acordo com o status.

### O que fazer

No `OrcamentoRepository`, criar:

```java
List<Orcamento> findByStatus(StatusOrcamento status);
```

Criar endpoint:

```text
GET /orcamento/status/{status}
```

Exemplos:

```text
GET /orcamento/status/PENDENTE
GET /orcamento/status/APROVADO
GET /orcamento/status/REJEITADO
```

### Conceitos trabalhados

- enum em consultas;
- filtro;
- repository personalizado.

---

## Exercício 13: melhorar as respostas HTTP

### Objetivo

Usar respostas HTTP mais adequadas.

### O que fazer

Alterar alguns métodos dos controllers para usar `ResponseEntity`.

Exemplos de status:

```text
201 Created
200 OK
204 No Content
404 Not Found
400 Bad Request
```

### Conceitos trabalhados

- protocolo HTTP;
- resposta da API;
- separação entre erro de regra e erro de servidor.

---

## Exercício 14: criar uma exceção de validação

### Objetivo

Criar uma classe específica para erros de regra de negócio.

### O que fazer

Criar um pacote:

```text
exception
```

Criar a classe:

```java
public class ValidacaoException extends RuntimeException {
    public ValidacaoException(String mensagem) {
        super(mensagem);
    }
}
```

Usar essa exceção nos services quando uma regra for violada.

### Conceitos trabalhados

- herança;
- exceções;
- classes especializadas.

---

## Exercício 15: desafio final

### Objetivo

Construir uma API completa usando os conceitos da lista.

### Requisitos

O sistema deve possuir:

- CRUD completo de `Produto`;
- CRUD completo de `Cliente`;
- CRUD completo de `Orcamento`;
- relacionamento entre `Orcamento` e `Cliente`;
- relacionamento entre `Orcamento` e `Produto`;
- status do orçamento usando `enum`;
- ações para aprovar e rejeitar orçamento;
- cálculo do valor total do orçamento;
- consultas por email do cliente;
- consultas por status do orçamento.

### Conceitos trabalhados

- classe;
- objeto;
- encapsulamento;
- associação;
- enum;
- herança;
- exceção;
- service;
- repository;
- controller;
- API REST;
- persistência com H2.

---

# 4. Entrega esperada

Ao final da lista, você deve entregar:

1. O projeto Spring Boot funcionando.
2. Todas as classes organizadas nos pacotes corretos.
3. CRUD completo para as entidades solicitadas.
4. Regras de negócio implementadas nos services.
5. Entidades com comportamentos próprios quando fizer sentido.
6. Testes manuais dos endpoints realizados em Bruno, Postman ou Insomnia.