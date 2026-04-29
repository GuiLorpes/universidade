# Lista 01

- `Resultados devem ser registrados no Github de cada aluno`

## Exercício 1 – Pessoa

- Crie uma classe chamada `Pessoa` com os atributos:
  - `nome`
  - `idade`
- Implemente:
  - métodos `get` e `set` para todos os atributos;
  - um método `exibirDados()` que mostre os dados da pessoa.
- No programa principal:
  - crie um objeto da classe;
  - atribua valores aos atributos;
  - exiba os dados.

## Exercício 2 – Produto

- Crie uma classe chamada `Produto` com os atributos:
  - `nome`
  - `preco`
- Implemente:
  - getters e setters;
  - um método `mostrarInformacoes()` para exibir nome e preço.
- No programa principal:
  - crie dois objetos;
  - apresente as informações dos dois produtos.

## Exercício 3 – Aluno

- Crie uma classe chamada `Aluno` com os atributos:
  - `nome`
  - `matricula`
  - `nota1`
  - `nota2`
- Implemente:
  - getters e setters;
  - um método `calcularMedia()`;
  - um método `verificarSituacao()` que informe se o aluno está aprovado ou reprovado.
- Considere:
  - aprovado se média maior ou igual a `7,0`.

## Exercício 4 – Retângulo

- Crie uma classe chamada `Retangulo` com os atributos:
  - `base`
  - `altura`
- Implemente:
  - getters e setters;
  - método `calcularArea()`;
  - método `calcularPerimetro()`.

## Exercício 5 – Conta Bancária

- Crie uma classe chamada `ContaBancaria` com os atributos:
  - `numero`
  - `titular`
  - `saldo`
- Implemente:
  - getters e setters;
  - método `depositar(valor)`;
  - método `sacar(valor)`;
  - método `consultarSaldo()`.
- Regra:
  - o saque só deve ocorrer se houver saldo suficiente.

## Exercício 6 – Carro

- Crie uma classe chamada `Carro` com os atributos:
  - `marca`
  - `modelo`
  - `velocidade`
- Implemente:
  - getters e setters;
  - método `acelerar()`;
  - método `frear()`;
  - método `mostrarVelocidade()`.
- Regra:
  - a velocidade não pode ficar negativa.

## Exercício 7 – Funcionário

- Crie uma classe chamada `Funcionario` com os atributos:
  - `nome`
  - `cargo`
  - `salario`
- Implemente:
  - getters e setters;
  - método `aumentarSalario(percentual)`;
  - método `exibirFuncionario()`.

## Exercício 8 – Livro

- Crie uma classe chamada `Livro` com os atributos:
  - `titulo`
  - `autor`
  - `emprestado`
- Implemente:
  - getters e setters;
  - método `emprestarLivro()`;
  - método `devolverLivro()`;
  - método `verificarDisponibilidade()`.
- Regra:
  - um livro emprestado não pode ser emprestado novamente sem antes ser devolvido.

## Exercício 9 – Celular

- Crie uma classe chamada `Celular` com os atributos:
  - `marca`
  - `modelo`
  - `nivelBateria`
- Implemente:
  - getters e setters;
  - método `carregar(valor)`;
  - método `usar(valor)`.
- Regras:
  - a bateria não pode ultrapassar `100`;
  - a bateria não pode ficar abaixo de `0`.

## Exercício 10 – Filme

- Crie uma classe chamada `Filme` com os atributos:
  - `titulo`
  - `genero`
  - `duracao`
  - `avaliacao`
- Implemente:
  - getters e setters;
  - método `exibirFichaTecnica()`;
  - método `alterarAvaliacao(novaAvaliacao)`.
- Regra:
  - a avaliação deve permanecer entre `0` e `10`.

## Exercício 11 – Paciente

- Crie uma classe chamada `Paciente` com os atributos:
  - `nome`
  - `peso`
  - `altura`
- Implemente:
  - getters e setters;
  - método `calcularIMC()`;
  - método `classificarIMC()`.

## Exercício 12 – Reserva de Hotel

- Crie uma classe chamada `ReservaHotel` com os atributos:
  - `nomeHospede`
  - `quantidadeDiarias`
  - `valorDiaria`
- Implemente:
  - getters e setters;
  - método `calcularTotal()`;
  - método `exibirReserva()`.

## Exercício 13 – Jogador

- Crie uma classe chamada `Jogador` com os atributos:
  - `nome`
  - `pontuacao`
  - `nivel`
- Implemente:
  - getters e setters;
  - método `adicionarPontos(valor)`;
  - método `subirNivel()`.
- Regra sugerida:
  - a cada `100` pontos, o jogador sobe um nível.

## Exercício 14 – Contato

- Crie uma classe chamada `Contato` com os atributos:
  - `nome`
  - `telefone`
  - `email`
- Implemente:
  - getters e setters;
  - método `exibirContato()`;
  - método `alterarTelefone(novoTelefone)`.

## Exercício 15 – Biblioteca Simplificada

- Crie uma classe chamada `LivroBiblioteca` com os atributos:
  - `titulo`
  - `autor`
  - `codigo`
  - `disponivel`
- Implemente:
  - getters e setters;
  - método `emprestar()`;
  - método `devolver()`;
  - método `exibirInformacoes()`.
- No programa principal:
  - crie pelo menos `3` livros;
  - simule empréstimos e devoluções;
  - mostre o estado final de cada objeto.

