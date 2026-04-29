# Lista de Exercícios – Herança, Array e ArrayList

## Objetivo
Desenvolver a compreensão e a aplicação prática de:
- reutilização de código por meio de **herança**;
- armazenamento e manipulação de coleções com **array**;
- uso de coleções dinâmicas com **ArrayList**.

---

## Exercício 1 – Pessoa e Aluno
Crie uma classe `Pessoa` com os atributos:
- `nome`
- `idade`

Depois, crie uma classe `Aluno` que herda de `Pessoa` e acrescente:
- `matricula`
- `curso`

Implemente métodos para:
- cadastrar os dados;
- exibir os dados completos.

---

## Exercício 2 – Pessoa e Professor
Crie uma classe `Professor` que também herda de `Pessoa` e possua:
- `disciplina`
- `salario`

Implemente um método `exibirProfessor()`.

---

## Exercício 3 – Veículo, Carro e Moto
Crie uma classe `Veiculo` com:
- `marca`
- `modelo`

Depois crie:
- `Carro`, com atributo `quantidadePortas`
- `Moto`, com atributo `cilindradas`

Implemente um método para exibir os dados de cada veículo.

---

## Exercício 4 – Funcionário e Gerente
Crie uma classe `Funcionario` com:
- `nome`
- `salario`

Crie uma subclasse `Gerente` com:
- `setor`

Adicione um método que mostre os dados do gerente.

---

## Exercício 5 – Vetor de números
Crie um programa que:
- leia 5 números inteiros;
- armazene em um `array`;
- exiba todos os valores;
- mostre a soma deles.

---

## Exercício 6 – Array de alunos
Usando a classe `Aluno`, crie um `array` para armazenar 3 alunos.

Depois:
- cadastre os dados dos 3 objetos;
- exiba todos os alunos cadastrados.

---

## Exercício 7 – Array de veículos
Crie um `array` de 4 posições para armazenar objetos da classe `Carro`.

Para cada carro:
- informe marca;
- modelo;
- quantidade de portas.

Depois exiba todos.

---

## Exercício 8 – Array com herança
Crie um `array` do tipo `Pessoa` e armazene nele:
- 2 objetos `Aluno`
- 2 objetos `Professor`

Depois percorra o array e exiba os dados.

---

## Exercício 9 – Lista de nomes
Crie um programa que use `ArrayList<String>` para:
- adicionar 5 nomes;
- exibir todos os nomes;
- mostrar a quantidade total cadastrada.

---

## Exercício 10 – Lista de produtos
Crie uma classe `Produto` com:
- `nome`
- `preco`

Use `ArrayList<Produto>` para:
- cadastrar 5 produtos;
- exibir os dados;
- mostrar o produto mais caro.

---

## Exercício 11 – Lista de professores
Crie uma `ArrayList<Professor>`.

O programa deve:
- cadastrar professores;
- exibir todos;
- permitir buscar um professor pelo nome.

---

## Exercício 12 – Remoção em ArrayList
Usando uma `ArrayList<Aluno>`, implemente:
- cadastro de alunos;
- listagem de alunos;
- remoção de um aluno pela matrícula.

---

## Exercício 13 – Cadastro de pessoas
Crie:
- classe `Pessoa`
- subclasse `Aluno`
- subclasse `Professor`

Depois faça duas versões do cadastro:
1. usando `array`
2. usando `ArrayList`

Em ambas:
- armazene objetos de `Aluno` e `Professor`;
- exiba todos os cadastrados.

---

## Exercício 14 – Sistema de biblioteca
Crie a classe `Livro` com:
- `titulo`
- `autor`

Crie a subclasse `LivroDidatico` com:
- `disciplina`

Implemente:
- um `array` com 3 livros;
- uma `ArrayList` para adicionar quantos livros quiser.

Exiba os dados em ambas as estruturas.

---

## Exercício 15 – Sistema de funcionários
Crie:
- classe `Funcionario`
- subclasse `Gerente`
- subclasse `Estagiario`

Depois:
- armazene alguns em `array`;
- armazene outros em `ArrayList`;
- exiba separadamente os dados.

---

## Exercício 16 – Folha de pagamento
Crie:
- `Funcionario`
- `Gerente`
- `Vendedor`

Cada classe deve ter seus próprios atributos, mas todas devem herdar de `Funcionario`.

Armazene os funcionários em uma `ArrayList<Funcionario>` e exiba:
- nome;
- cargo;
- salário.

---

## Exercício 17 – Agenda de contatos
Crie:
- `Contato`
- `ContatoPessoal`
- `ContatoProfissional`

Use `ArrayList<Contato>` para cadastrar contatos dos dois tipos.

Exiba:
- todos os contatos;
- apenas os contatos profissionais.

---

## Exercício 18 – Controle de animais
Crie:
- `Animal`
- `Cachorro`
- `Gato`
- `Passaro`

Armazene os animais em um `array` e depois em uma `ArrayList`.

Exiba os dados dos objetos armazenados nas duas estruturas.

---

## Exercício 19 – Catálogo de mídia
Crie a classe `Midia` com:
- `titulo`
- `ano`

Crie subclasses:
- `Filme`
- `Musica`
- `Podcast`

Armazene tudo em `ArrayList<Midia>`.

O programa deve:
- cadastrar mídias;
- listar todas;
- listar apenas filmes;
- contar quantos itens existem de cada tipo.

---

## Exercício 20 – Sistema escolar
Crie:
- `Pessoa`
- `Aluno`
- `Professor`
- `Coordenador`

Use `ArrayList<Pessoa>` para armazenar todos.

Implemente:
- cadastro;
- listagem geral;
- listagem por tipo;
- busca por nome.

---

## Exercício 21 – Loja virtual
Crie:
- `Produto`
- `ProdutoFisico`
- `ProdutoDigital`

Armazene os produtos em uma `ArrayList<Produto>`.

Implemente:
- cadastro;
- exibição;
- cálculo do valor total de todos os produtos;
- separação entre físicos e digitais.

---

## Exercício 22 – Comparando array e ArrayList
Escreva uma explicação prática respondendo:
- quando usar `array`;
- quando usar `ArrayList`;
- quais são as vantagens e limitações de cada um.

---

## Exercício 23 – Refatoração
Escolha um exercício que foi feito com `array` e refaça usando `ArrayList`.

Depois explique:
- o que mudou no código;
- o que ficou mais fácil;
- o que deixou de ser necessário controlar manualmente.

---

## Exercício 24 – Sistema livre
Crie um pequeno sistema com:
- uma superclasse;
- pelo menos 2 subclasses;
- armazenamento em `ArrayList`;
- busca de objetos;
- remoção de objetos;
- exibição geral.

Sugestões:
- sistema de biblioteca;
- sistema de veículos;
- sistema de pets;
- sistema de funcionários.

---

## Exercício 25 – Conceitos
Responda:

a) O que é herança?  
b) Qual a diferença entre classe base e subclasse?  
c) O que é um `array`?  
d) O que é um `ArrayList`?  
e) Qual a principal diferença entre `array` e `ArrayList`?  
f) Por que uma `ArrayList<Pessoa>` pode armazenar `Aluno` e `Professor`?

---