import gleam/int
import gleam/string
import sgleam/check

pub fn hello(name: String) -> String {
  "Hello " <> name <> "!"
}

pub fn hello_examples() {
  check.eq(hello("World"), "Hello World!")
}

/// Produz True se uma pessoa com *idade* é isento da
/// tarifa de transporte público, isto é, tem menos
/// de 18 anos ou 65 ou mais. Produz False caso contrário.
pub fn isento_tarifa(idade: Int) -> Bool {
  idade <= 18 || idade >= 65
}

pub fn isento_tarifa_examples() {
  check.eq(isento_tarifa(17), True)
  check.eq(isento_tarifa(18), True)
  check.eq(isento_tarifa(50), False)
  check.eq(isento_tarifa(65), True)
  check.eq(isento_tarifa(70), True)
}

/// Conta a quantidade de dígitos de *n*.
/// Se *n* é 0, então devolve zero.
/// Se *n* é menor que zero, então devolve a quantidade
/// de dígitos do valor absoluto de *n*.
pub fn quantidade_digitos(n: Int) -> Int {
  case n == 0 {
    True -> 0
    False ->
      case n < 0 {
        True -> string.length(int.to_string(n)) - 1
        False -> string.length(int.to_string(n))
      }
  }
}

pub fn quantidade_digitos_examples() {
  check.eq(quantidade_digitos(123), 3)
  check.eq(quantidade_digitos(0), 0)
  check.eq(quantidade_digitos(-1519), 4)
}

/// Produz True se uma pessoa com *idade* é supercentenária,
/// isto é, tem 110 anos ou mais, produz False caso contrário.
pub fn supercentenario(idade: Int) -> Bool {
  idade >= 110
}

pub fn supercentenario_examples() {
  check.eq(supercentenario(101), False)
  check.eq(supercentenario(110), True)
  // Mudei esse exemplo
  check.eq(supercentenario(112), True)
}

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

/// Aumenta *valor* em *porcentagem* %
pub fn aumenta(valor: Float, porcentagem: Float) -> Float {
  valor *. { 1.0 +. porcentagem /. 100.0 }
}

pub fn aumenta_examples() {
  check.eq(aumenta(20.0, 50.0), 30.0)
  check.eq(aumenta(48.7, 15.8), 56.3946)
  check.eq(aumenta(32.5, 112.4), 69.03)
  check.eq(aumenta(40.9, -2.4), 39.9184)
  check.eq(aumenta(67.0, 0.0), 67.0)
}


// 20

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


// 21

type Alinhamento = String
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
fn ajusta_string(s: String, num_chars: Int, alinhamento: Alinhamento) -> String {
  case string.length(s) == num_chars {
    True -> s
    False ->
      case string.length(s) > num_chars {
        True -> string.slice(s, 0, num_chars - 3) <> "..."
        False -> {
          let num_espacos = num_chars - string.length(s)
          case alinhamento {
            "direita" -> string.repeat(" ", num_espacos) <> s
            "esquerda" -> s <> string.repeat(" ", num_espacos)
            _ -> {
            let num_espacos_inicio = num_espacos / 2
            let num_espacos_fim = num_espacos - num_espacos_inicio
            string.repeat(" ", num_espacos_inicio)
            <> s
            <> string.repeat(" ", num_espacos_fim)
            }
          }
        }
      }
  }
}

pub fn ajusta_string_examples() {
  // check.eq(ajusta_string("casa verde", 2, "esquerda"), "..") é pra dar erro
  check.eq(ajusta_string("casa verde", 3, "esquerda"), "...")
}


// 22

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


// 23

/// Verifica se *s* possui um "-" no meio dela
pub fn verifica_traco(s: String) {
  string.slice(s, (string.length(s) / 2), (string.length(s) / 2) + 1) == "-"
}