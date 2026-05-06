# 1. Implementando requisitos

Para cada requisito, o aluno deve responder primeiro:

## Etapa 1 – Interpretação
1. Quais classes aparecem no problema?
2. Quais atributos são necessários?
3. Existe alguma regra de negócio?
4. Existe algum `enum`?
5. Qual método representa a ação principal?
6. O que deve acontecer quando a regra for satisfeita?
7. O que deve acontecer quando a regra não for satisfeita?

## Etapa 2 – Pseudocódigo
Descrever em poucas linhas o comportamento esperado.

## Etapa 3 – Implementação
Só depois escrever o código em Java.

---

# 1. Lista de exercícios para praticar interpretação e implementação

## Exercício 1
### Requisito
**O sistema deve permitir que um produto seja cadastrado apenas por um usuário do tipo ADMIN.**

### O que o aluno deve identificar
- classes possíveis;
- necessidade de `enum`;
- regra de autorização;
- método de cadastro.

---

## Exercício 2
### Requisito
**O sistema deve permitir que um comentário seja publicado apenas por um usuário do tipo PADRAO.**

### O que o aluno deve identificar
- estrutura semelhante ao exemplo da tarefa;
- mudança do domínio;
- adaptação da regra para outro objeto.

---

## Exercício 3
### Requisito
**O sistema deve permitir que um visitante visualize notícias, mas não permita que ele cadastre notícias.**

---

## Exercício 4
### Requisito
**O sistema deve permitir que um aluno reserve um livro apenas se seu status estiver ATIVO.**

---

## Exercício 5
### Requisito
**O sistema deve permitir que uma tarefa seja concluída apenas se ela estiver com status EM_ANDAMENTO.**

---

## Exercício 6
### Requisito
**O sistema deve permitir que um professor lance notas apenas para turmas do seu próprio curso.**

---

## Exercício 7
### Requisito
**O sistema deve permitir que um usuário remova uma atividade apenas se ele for o responsável por ela.**

---

## Exercício 8
### Requisito
**O sistema deve permitir que um pedido seja cancelado apenas se seu status for PENDENTE.**

---

## Exercício 9
### Requisito
**O sistema deve permitir que um gerente aprove solicitações, mas usuários do tipo PADRAO apenas criem solicitações.**

---

## Exercício 10
### Requisito
**O sistema deve permitir que um usuário do tipo ADMIN crie usuários do tipo PADRAO, mas não permita criar outros administradores.**

---