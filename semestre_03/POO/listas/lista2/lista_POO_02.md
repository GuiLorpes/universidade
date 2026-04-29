# Lista 02 – OO com Relacionamento 1:1

- `Resultados devem ser registrados no Github de cada aluno`

## Objetivo
Praticar a modelagem e a implementação de classes com **relacionamento um para um**, compreendendo como um objeto pode estar associado diretamente a outro objeto único.

## Relembrando o conceito
Um relacionamento **1:1** ocorre quando:
- um objeto de uma classe se relaciona com **exatamente um** objeto de outra classe;
- e o inverso também pode ser verdadeiro, dependendo da regra do problema.

Exemplos:
- uma `Pessoa` possui um `CPF`;
- um `Aluno` possui uma `Carteirinha`;
- um `Carro` possui um `Motor`.

---

# Exercícios

## Exercício 1 – Pessoa e CPF
Crie um sistema com as classes:

- `Pessoa`
- `CPF`

### Regras
- Uma pessoa possui um único CPF.
- Um CPF pertence a uma única pessoa.

### Classe `CPF`
Atributos sugeridos:
- `numero`
- `situacao`

### Classe `Pessoa`
Atributos sugeridos:
- `nome`
- `idade`
- `cpf` do tipo `CPF`

### Solicita-se
- implementar encapsulamento;
- criar construtores;
- criar métodos `exibirDados()` nas duas classes;
- no programa principal, criar uma pessoa com seu CPF e exibir tudo.

---

## Exercício 2 – Aluno e Carteirinha
Crie as classes:

- `Aluno`
- `Carteirinha`

### Regras
- Cada aluno possui uma única carteirinha.
- Cada carteirinha pertence a um único aluno.

### Classe `Carteirinha`
Atributos sugeridos:
- `numero`
- `dataEmissao`

### Classe `Aluno`
Atributos sugeridos:
- `nome`
- `curso`
- `carteirinha` do tipo `Carteirinha`

### Solicita-se
- criar getters e setters;
- criar método para exibir os dados do aluno e de sua carteirinha;
- testar no programa principal.

---

## Exercício 3 – Carro e Motor
Crie as classes:

- `Carro`
- `Motor`

### Regras
- Um carro possui um único motor.
- Um motor está associado a um único carro.

### Classe `Motor`
Atributos sugeridos:
- `tipo`
- `potencia`
- `numeroSerie`

### Classe `Carro`
Atributos sugeridos:
- `marca`
- `modelo`
- `motor` do tipo `Motor`

### Solicita-se
- criar método `ligarCarro()`;
- criar método `exibirFichaTecnica()` em `Carro`;
- exibir também as informações do motor.

---

## Exercício 4 – Computador e PlacaMae
Crie as classes:

- `Computador`
- `PlacaMae`

### Regras
- Um computador possui uma única placa-mãe.
- Uma placa-mãe pertence a um único computador.

### Classe `PlacaMae`
Atributos sugeridos:
- `modelo`
- `chipset`

### Classe `Computador`
Atributos sugeridos:
- `marca`
- `processador`
- `placaMae` do tipo `PlacaMae`

### Solicita-se
- implementar um método `exibirConfiguracao()`;
- instanciar um computador e sua placa-mãe;
- mostrar os dados no programa principal.

---

## Exercício 5 – Livro e ISBN
Crie as classes:

- `Livro`
- `ISBN`

### Regras
- Cada livro possui um único ISBN.
- Cada ISBN identifica um único livro.

### Classe `ISBN`
Atributos sugeridos:
- `codigo`
- `editora`

### Classe `Livro`
Atributos sugeridos:
- `titulo`
- `autor`
- `isbn` do tipo `ISBN`

### Solicita-se
- criar método para exibir os dados completos do livro;
- mostrar claramente a associação 1:1.

---

## Exercício 6 – Funcionário e Crachá
Crie as classes:

- `Funcionario`
- `Cracha`

### Regras
- Cada funcionário possui um crachá único.
- Cada crachá pertence a apenas um funcionário.

### Classe `Cracha`
Atributos sugeridos:
- `codigo`
- `dataValidade`

### Classe `Funcionario`
Atributos sugeridos:
- `nome`
- `cargo`
- `cracha` do tipo `Cracha`

### Solicita-se
- criar método `exibirFuncionario()`;
- incluir os dados do crachá na exibição;
- testar com dois funcionários diferentes.

---

## Exercício 7 – Paciente e Prontuário
Crie as classes:

- `Paciente`
- `Prontuario`

### Regras
- Cada paciente possui um único prontuário.
- Cada prontuário pertence a um único paciente.

### Classe `Prontuario`
Atributos sugeridos:
- `numeroRegistro`
- `tipoSanguineo`
- `alergias`

### Classe `Paciente`
Atributos sugeridos:
- `nome`
- `idade`
- `prontuario` do tipo `Prontuario`

### Solicita-se
- criar método `exibirPaciente()`;
- exibir também os dados do prontuário.

---

## Exercício 8 – Casa e Endereço
Crie as classes:

- `Casa`
- `Endereco`

### Regras
- Cada casa possui um único endereço.
- Cada endereço está associado a uma única casa no contexto do exercício.

### Classe `Endereco`
Atributos sugeridos:
- `rua`
- `numero`
- `bairro`
- `cidade`

### Classe `Casa`
Atributos sugeridos:
- `cor`
- `quantidadeQuartos`
- `endereco` do tipo `Endereco`

### Solicita-se
- criar método `exibirCasa()`;
- mostrar os dados da casa e do endereço.

---

## Exercício 9 – Empresa e CNPJ
Crie as classes:

- `Empresa`
- `CNPJ`

### Regras
- Cada empresa possui um único CNPJ.
- Cada CNPJ identifica uma única empresa.

### Classe `CNPJ`
Atributos sugeridos:
- `numero`
- `situacaoCadastral`

### Classe `Empresa`
Atributos sugeridos:
- `razaoSocial`
- `nomeFantasia`
- `cnpj` do tipo `CNPJ`

### Solicita-se
- implementar encapsulamento;
- criar método `exibirEmpresa()`.

---

## Exercício 10 – Usuário e Perfil
Crie as classes:

- `Usuario`
- `Perfil`

### Regras
- Cada usuário possui um único perfil.
- Cada perfil pertence a um único usuário.

### Classe `Perfil`
Atributos sugeridos:
- `bio`
- `foto`
- `visibilidade`

### Classe `Usuario`
Atributos sugeridos:
- `login`
- `email`
- `perfil` do tipo `Perfil`

### Solicita-se
- criar método `exibirUsuario()`;
- exibir também os dados do perfil.

---

# Atenção para identificar

- qual é a classe principal;
- qual é a classe associada;
- onde está o atributo que representa o relacionamento;
- como um objeto acessa os dados do outro;
- como exibir os dados das duas classes integradas.

---

# Exemplo curto porem incompleto de estrutura esperada
No caso `Pessoa` e `CPF`, a ideia seria algo como:

```java
public class CPF {
    private String numero;
    private String situacao;
}
```

```java
public class Pessoa {
    private String nome;
    private int idade;
    private CPF cpf;
}
```

```java

public class Main {
    public static void main(String[] args) {
        
        CPF cpfJoao = new CPF('123...');
        Pessoa joao = new Pessoa('Joao', cpfJoao);

        joao.getCpf();

    }
}

```

Aqui, o relacionamento 1:1 aparece porque `Pessoa` possui um único atributo `cpf`, do tipo `CPF`.
