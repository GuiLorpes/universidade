import io
import os
import sys




def buscaSecundaria1(genero: str) -> list[str]:
    '''
    Procura por itens do *genero*, e retorna todos em uma lista de string 
    separados por '|', caso não encontre, retorna uma lista vazia
    Ex: 
    >>> buscaSecundaria1("Hack and Slash")
        [100|God of War|2005|Hack and Slash|Sony|PlayStation 2|,
127|Devil May Cry 3: Dante's Awakening|2005|Hack and Slash|Capcom|PlayStation 2|,
238|NieR: Automata|2017|Hack and Slash|Square Enix|PlayStation 4|,
728|Bayonetta 2|2014|Hack and Slash|Nintendo|Nintendo Switch|,
964|Diablo II|2000|Hack and Slash|Blizzard|PC|,
    '''
    itens: list[str] = []
    try:
        with open("genero.ind", "rb") as entrada:
            tamReg = int.from_bytes(entrada.read(2), 'little')
            while tamReg > 0:
                registro = (entrada.read(tamReg)).decode()
                campos = registro.split('|')
                if campos[3] == genero:
                    itens.append(registro)
                tamReg = int.from_bytes(entrada.read(2), 'little')
            if len(itens) == 0:
                print(f"Nenhum registro de {genero} foi encontrado")
        return itens
    except FileNotFoundError as e:
        print(f"Erro: {e}")
    return itens


def buscaSecundaria2(publicadora: str) -> list[str]:
    '''
    Procura por itens do *genero*, e retorna todos em uma lista de string 
    separados por '|', caso não encontre, retorna uma lista vazia
    Ex: 
    >>> buscaSecundaria2("CD Projekt RED")
        [163|Cyberpunk 2077|2020|Action RPG|CD Projekt RED|PC|,
875|The Witcher III: Wild Hunt|2015|Action RPG|CD Projekt RED|PC|,
894|The Witcher 2: Assassins of Kings|2011|Action RPG|CD Projekt RED|PC|]
    '''
    itens: list[str] = []
    try:
        with open("publicadora.ind", "rb") as entrada:
            tamReg = int.from_bytes(entrada.read(2), 'little')
            while tamReg > 0:
                registro = (entrada.read(tamReg)).decode()
                campos = registro.split('|')
                if campos[4] == publicadora:
                    itens.append(registro)
                tamReg = int.from_bytes(entrada.read(2), 'little')
            if len(itens) == 0:
                print(f"Nenhum registro de {publicadora} foi encontrado")
        return itens
    except FileNotFoundError as e:
        print(f"Erro: {e}")
    return itens


def main() -> None:
    if len(sys.argv) > 3:
        print(f"Erro! Uso: {sys.argv[0]} <-bp ou -bs1 ou -bs2> <chave>")
        print("bp -> Busca por chave primária\nbs1 -> Busca por chave "\
              "secundária 1\nbs2 -> Busca por chave secundária 2")
        return
    match sys.argv[1]:
        case "-bp":
            print(buscaPrimaria(sys.argv[2]))
        case "-bs1": 
            for r in buscaSecundaria1(sys.argv[2]):
                print(r)
        case "-bs2":
            for r in buscaSecundaria2(sys.argv[2]):
                print(r)
        case _:
            print(f"Erro! Uso: {sys.argv[0]} <-bp ou -bs1 ou -bs2> <chave>")
            print("bp -> Busca por chave primária\nbs1 -> Busca por chave "\
              "secundária 1\nbs2 -> Busca por chave secundária 2")
        
if __name__ == "__main__":
    main()