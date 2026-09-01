# Resolução Lista 1

## Começando

1. O que é programação imperativa?
   ```
   - Paradigma de programação onde os programas são descritos com sentenças que modificam o estado do programa
   ```

2. O que é programação funcional?
   ```
   - Paradigma de programação onde os programas são descritos com aplicação e composição de funções, onde se evita a mudança de estados (mudança do valor das variáveis) e efeitos colaterais.
   ```

3. Por que compartilhar dados que podem mudar de estado é difícil? Dê um exemplo.
   ```
   - Pois em alguns casos, ao modificar um desses dados é possivel modificar todas as variáveis que compartilha desses dados, que pode atrapalhar o funcionamento do código, como em Python:

        >>> lst = [[]] * 3
        >>> lst
        [[],[],[]]
        >>> lst[1].append(2)
        >>> lst
        [[2],[2],[2]]
    ```


4. O que é efeito colateral?
   ```
   - Efeito colateral é qualquer efeito observável além do valor de saida da função, como mudança dos parametros e variáveis globas, exceções, entrada e saída, etc.
   ```

5. O Alberto disse que não tem interesse em aprender programação funcional em Gleam, pois "ninguém" usa Gleam na prática. Explique para o Alberto por que esse argumento não faz sentido.
   ```
   - Aprender programação funcional, em qualquer linguagem que seja é de extrema importância pois aprender paradigmas diferentes é extremamente importante. Com um vasto conhecimento sobre outras linguagens é possível resolver dos mais diversos problemas. Aprender programação funcional com Gleam ajuda a entrar na programação funcional com uma linguagem de fácil aprendizado, e que serve de porta de entrada para outras mais complexas. 
   ```


> Os exercícios de 6 a 9 são para prática, portanto não estarão aqui!

## Avançado

10. Defina uma função *f* em uma linguagem qualquer de maneira que o resultado de *f(1) + f(2)* seja diferente do resultado de *f(2) + f(1)*
   ```py
    lista: list[int] = [4, 6, 1, 7]
    def faz_algo(n: int) -> int:
        soma = 0
        if n % 2 == 0:
            lista.pop()
            lista.append(n)
            for i in lista:
                soma += i
            return soma
        else:
            lista.append(2 * n)
            if n <= len(lista):
                lista.pop(n)
            for i in lista:
                soma += i
            return soma
   ```

11. Que dificuldades os efeitos colaterais podem gerar no desenvolvimento de um programa?
   ```
   - Os efeitos colaterais podem afetar o desenvolvimento de um programa pois suas mudanças, quando não realizadas da forma que desejamos, pode atrapalhar achar e corrigir algum bug, pois o código não fica código localizado e afeta o tempo de desenvolvimento.
   ```
12. Que dificuldades a ausência de mudança de estado podem gerar no desenvolvimento de um programa?
   ```
   - Como muitas vezes usamos mudança de estados sem nem perceber, essa ausência pode complicar a implementação de um código
   ```