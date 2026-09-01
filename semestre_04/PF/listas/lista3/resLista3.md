# Resolução Lista 3

## Praticando 

15. Implemente a função de acordo com a especificação a seguir. Corrija a especificação se necessário.
   ```gleam
    // Especificação original:
    /// Produz True se uma pessoa com *idade* é isento da
    /// tarifa de transporte público, isto é, tem menos
    /// de 18 anos ou 65 ou mais. Produz False caso contrário.
    pub fn isento_tarifa(idade: Int) -> Bool {
    False
    }
    pub fn isento_tarifa_examples() {
      check.eq(isento_tarifa(17), True)
      check.eq(isento_tarifa(18), True)
      check.eq(isento_tarifa(50), False)
      check.eq(isento_tarifa(65), True)
      check.eq(isento_tarifa(70), True)
    }

    // Especificação nova + implementação:
    /// Produz True se uma pessoa com *idade* é isento da
    /// tarifa de transporte público, isto é, tem 18 anos ou menos,
    /// ou 65 ou mais. Produz False caso contrário.
    pub fn isento_tarifa(idade: Int) -> Bool { idade <= 18 || idade >= 65 }
    pub fn isento_tarifa_examples() {
      check.eq(isento_tarifa(17), True)
      check.eq(isento_tarifa(18), True)
      check.eq(isento_tarifa(50), False)
      check.eq(isento_tarifa(65), True)
      check.eq(isento_tarifa(70), True)
    }
   ```

16. Implemente a função de acordo com a especificação a seguir. Corrija a especificação se necessário.
   ``` gleam
   // Especificação original:
   /// Conta a quantidade de dígitos de *n*.
   /// Se *n* é 0, então devolve zero.
   /// Se *n* é menor que zero, então devolve a quantidade
   /// de dígitos do valor absoluto de *n*.
   pub fn quantidade_digitos(n: Int) -> Int {
   0
   }
   pub fn quantidade_digitos_examples() {
   check.eq(quantidade_digitos(123), 3)
   check.eq(quantidade_digitos(0), 1)
   check.eq(quantidade_digitos(-1519), 4)
   }

   // Especificação nova + implementação:
   /// Conta a quantidade de dígitos de *n*.
   /// Se *n* é 0, então devolve zero.
   /// Se *n* é menor que zero, então devolve a quantidade
   /// de dígitos do valor absoluto de *n*.
   pub fn quantidade_digitos(n: Int) -> Int {
     case n == 0 {
       True -> 0
       False ->  case n < 0 {
         True -> string.length(int.to_string(n)) - 1
         False -> string.length(int.to_string(n))
       }
     }
   }

   pub fn quantidade_digitos_examples() {
     check.eq(quantidade_digitos(123), 3)
     check.eq(quantidade_digitos(0), 0) // Mudei esse exemplo
     check.eq(quantidade_digitos(-1519), 4)
   }
   ```

17. 
   ```gleam
   // Especificação original:
   /// Produz True se uma pessoa com *idade* é supercentenária,
   /// isto é, tem 110 anos ou mais, produz False caso contrário.
   pub fn supercentenario(idade: Int) -> Bool {
     False
   }
   pub fn supercentenario_examples() {
     check.eq(supercentenario(101), False)
     check.eq(supercentenario(110), False)
     check.eq(supercentenario(112), True)
   }

   // Especificação nova + implementação:
   /// Produz True se uma pessoa com *idade* é supercentenária,
   /// isto é, tem 110 anos ou mais, produz False caso contrário.
   pub fn supercentenario(idade: Int) -> Bool { idade >= 110 }
   pub fn supercentenario_examples() {
     check.eq(supercentenario(101), False)
     check.eq(supercentenario(110), True) // Mudei esse exemplo
     check.eq(supercentenario(112), True)
   }
   ```

18.
   ```gleam
   // Especificação original:
   /// Transforma a string *data* que está no formato "dia/mes/ano"
   /// para o formato "ano/mes/dia".
   ///
   /// Requer que o dia e o mês tenham dois dígitos e que
   /// o ano tenha quatro dígitos.
   pub fn dma_para_amd(data: String) -> String {
     data
   }
   pub fn dma_para_amd_examples() {
     check.eq(dma_para_amd("19/07/2023"), "2023/07/19")
     check.eq(dma_para_amd("01/01/1980"), "1980/01/01")
     check.eq(dma_para_amd("02/02/2002"), "2002/02/20")
   }

   // Especificação nova + implementação
   /// Transforma a string *data* que está no formato "dia/mes/ano"
   /// para o formato "ano/mes/dia".
   ///
   /// Requer que o dia e o mês tenham dois dígitos e que
   /// o ano tenha quatro dígitos.
   pub fn dma_para_amd(data: String) -> String {
     let dd = string.slice(data, 0, 2)
     let mm = string.slice(data, 3, 2)
     let aaaa = string.slice(data, 6, 4)
     aaaa <> "/" <> mm <> "/" <> dd
   }

   pub fn dma_para_amd_examples() {
     check.eq(dma_para_amd("19/07/2023"), "2023/07/19")
     check.eq(dma_para_amd("01/01/1980"), "1980/01/01")
     check.eq(dma_para_amd("02/02/2002"), "2002/02/02")
   }
   ```

19. Escreva a especificação para a seguinte implementação de função. Avalie se a sua especificação está boa, verificando se ela sozinha é suficiente para um desenvolvedor fazer uma implementação da função.
   ```gleam
   pub fn aumenta(valor: Float, porcentagem: Float) -> Float {
     valor *. { 1.0 +. porcentagem /. 100.0 }
   }
   ```
   
   ```gleam
   /// Aumenta *valor* em *porcentagem* %, porém se *porcentagem* < 0, diminui
   pub fn aumenta(valor: Float, porcentagem: Float) -> Float {
     valor *. { 1.0 +. porcentagem /. 100.0 }
   }
   
   pub fn aumenta_examples() {
     check.eq(aumenta(20.0, 50.0), 30.0)
     check.eq(aumenta(48.7, 15.8), 56.3946)
     check.eq(aumenta(32.5, 112.4), 69.03)
     check.eq(aumenta(40.9, -2.4), 39.9184)
     check.eq(aumenta(67.0, 0.0), 0)
   }
   ```

20. Escreva a especificação para a seguinte implementação de função. Avalie se a sua especificação está boa, verificando se ela sozinha é suficiente para um desenvolvedor fazer uma implementação da função.
   ```gleam
   pub fn tamanho_nome(nome: String) -> String {
     case string.length(nome) <= 4 {
       True -> "curto"
       False ->
         case string.length(nome) <= 10 {
           True -> "médio"
           False -> "longo"
         }
     }
   }
   ```

   ```gleam
   /// Verifica o tamanho de *nome*, se um *nome* tiver menos que, ou 4 caractéres 
   /// é "curto", se tiver mais que 4 e for menor ou igual a 10 é "médio", e acima 
   /// de 10 é "longo"
   pub fn tamanho_nome(nome: String) -> String {
     case string.length(nome) <= 4 {
       True -> "curto"
       False ->
         case string.length(nome) <= 10 {
           True -> "médio"
           False -> "longo"
         }
     }
   }

   pub fn tamanho_nome_examples() {
     check.eq(tamanho_nome("José"), "curto")
     check.eq(tamanho_nome("Guilherme"), "médio")
     check.eq(tamanho_nome("Anaximandro"), "longo")
   }
   ```

21. A ajusta_string, projetada neste capítulo, promete produzir uma string com exatamente num_chars caracteres, e o seu propósito não registra nenhuma restrição. O que ela produz quando s é "casa verde" e num_chars é 2? A promessa foi cumprida? Acrescente ao propósito a restrição que falta e diga se a função é total ou parcial.
   ```
   - Ao usar ajusta_string("casa verde", 2, "esquerda"), ao invés de gerar "..", que era o esperado, gera "...", o que quebra a promessa da função. Para que o propósito fique correto, devemos adicionar a restrição que *num_chars* deve ser maior ou igual a 3. A função é parcial por justamente não produzir valores esperados para todos os valores de entrada.
   ```
   ```gleam
   /// Produz uma nova string a partir de *s* que tem exatamente *num_chars*
   /// caracteres e é alinhada de acordo com o *alinhamento*.
   ///
   /// Se *s* tem exatamente *num_chars* caracteres, então produz *s*.
   ///
   /// Se *s* tem mais do que *num_chars* caracteres, então *s* é truncada e "..."
   /// é adicionado ao final para sinalizar que a string foi abreviada.
   ///
   /// Se *s* tem menos do que *num_chars* caracteres, então espaços são
   /// adicionados no início se *alinhamento* é "direita", no fim se *alinhamento*
   /// é "esquerda", ou no início e fim se *alinhamento* é "centro". Nesse último
   /// caso, se a quantidade de espaços adicionados for ímpar, então no fim será
   /// adicionado 1 espaço a mais do que no início.
   /// 
   /// *num_chars* precisa ser maior ou igual a 3
   ```

22. Projete uma função que adicione um ponto final a uma frase se ela não acabar com um.
   ```gleam
   /// Retorna uma string a partir de *s*, onde se ela tiver um ponto final, retorna 
   /// ela mesma, caso contrário retorna *s* <> "."
   pub fn adiciona_ponto(s: String) {
     case string.last(s) == Ok(".") {
       True -> s
       False -> s <> "."
     }
   }

   pub fn adiciona_ponto_examples() {
     check.eq(adiciona_ponto("Ponto"), "Ponto.")
     check.eq(adiciona_ponto("Ponto."), "Ponto.")
   }
   ```

23. Projete uma função que determine se uma palavra tem um traço ("-") no meio, como por exemplo, "lero-lero". Não use nenhum condicional na implementação.


24. Projete uma função que encontre o máximo entre três números dados.


25. Projete uma função que receba como parâmetro uma string e um número natural n e substitua os primeiros n caracteres da string por n letras "x".


## Resolvendo problemas

26. Você está fazendo um programa e precisa verificar se um texto digitado pelo usuário está de acordo com algumas regras. A regra “sem espaços extras” requer que o texto não comece e não termine com espaços. Projete uma função que verifique se um texto qualquer está de acordo com a regra “sem espaços extras”.


27. Cada cidadão de um país, cuja moeda chama-se dinheiro, tem que pagar imposto sobre a sua renda. Cidadãos que recebem até 1000 dinheiros pagam 5% de imposto. Cidadãos que recebem entre 1000 e 5000 dinheiros pagam 5% de imposto sobre 1000 dinheiros e 10% sobre o que passar de 1000. Cidadãos que recebem mais de 5000 dinheiros pagam 5% de imposto sobre 1000 dinheiros, 10% de imposto sobre 4000 dinheiros e 20% sobre o que passar de 5000. Projete uma função que calcule o imposto que um cidadão deve pagar dada a sua renda.


28. Uma palavra duplicada é formada pela ocorrência de duas partes iguais, separadas ou não por hífen. Por exemplo, as palavras xixi, mimi, lero-lero e mata-mata são palavras duplicadas. Projete uma função que verifique se uma palavra é duplicada.


29. Um construtor precisa calcular a quantidade de azulejos necessários para azulejar uma determinada parede. Cada azulejo é quadrado e tem 20cm de lado. Ajude o construtor e defina uma função que receba como entrada o comprimento e a altura em metros de uma parede e calcule a quantidade de azulejos inteiros necessários para azulejar a parede. Considere que o construtor nunca perde um azulejo e que recortes de azulejos não são reaproveitados.


30. Rotacionar uma string n posições à direita significa mover os últimos n caracteres da string para as primeiras n posições da string. Por exemplo, rotacionar a string "marcelio" 5 posições à direita produz a string "celiomar". Projete uma função que receba como entrada uma string e um número n e produza uma nova string rotacionando a string de entrada n posições à direita.


31. No período de 2015 a 2016 todos os números de telefones celulares no Brasil passaram a ter nove dígitos. Na época, os números de telefones que tinham apenas oito dígitos foram alterados, adicionando-se o 9 na frente do número. Embora oficialmente todos os número de celulares tenham nove dígitos, na agenda de muitas pessoas ainda é comum encontrar números registrados com apenas oito dígitos. Projete uma função que adicione o nono dígito em um dado número de telefone celular caso ele ainda não tenha o nono dígito. Considere que os números de entrada são dados com o DDD entre parênteses e com um hífen separando os últimos quatro dígitos. Exemplos de entradas: (44) 9787-1241, (51) 95872-9989, (41) 8876-1562. A saída deve ter o mesmo formato, mas garantindo que o número do telefone tenha 9 dígitos.


## Desafios

32. Muitos letreiros exibem mensagens que têm mais caracteres do que eles podem exibir, para isso, eles exibem apenas uma porção da mensagem que é alterada com o passar do tempo. Por exemplo, em um letreiro de 20 caracteres, a mensagem "Promoção de sorvetes, pague 2 leve 3!" é exibida como "Promoção de sorvetes" no momento 0, como "romoção de sorvetes," no momento 1, como "omoção de sorvetes, " no momento 2, e assim por diante até que no momento 17 é exibido "tes, pague 2 leve 3!". O momento sempre aumenta, e após chegar no final da mensagem ela começa a ser exibida novamente, nesse caso, no momento 18 é exibido "es, pague 2 leve 3! " e no momento 19 é exibido "s, pague 2 leve 3! P", onde o P é o início da mensagem. Projete uma função que determine os caracteres de uma mensagem que devem ser exibidos em um determinado momento em um letreiro que pode exibir um determinado número de caracteres. Assuma que o número de caracteres
da mensagem é maior do que o do letreiro. 


33. Um número inteiro positivo é palíndromo se quando lido da direita para a esquerda ou da esquerda para a direita é idêntico. Ex: 9119, 1221, 5665, 7337. Projete uma função que verifique se um dado número inteiro de 4 dígitos é palíndromo, considere que o valor de entrada é o próprio número e não os quatro dígitos que compõem o número. É possível modificar a sua função de maneira que ela funcione para qualquer número de entrada e não apenas para números de 4 dígitos?
