from __future__ import annotations
from dataclasses import dataclass
import io
import os
import sys

ORDEM = 5
ARQUIVO = "games.dat"
ARVORE = "arvoreGames.dat"


@dataclass
class Elemento:
    id: int
    offset: int


@dataclass
class Pagina:
    chaves: list[Elemento]     # Lista com os elementos da página
    filhas: list[Arvore]          # Uma lista com RRN de cada filho no arquivo 
    rrn: int                   # RRN da página atual
    def __init__(self):
        self.chaves = []
        self.filhas = [None] * ORDEM

Arvore = Pagina | None

def criaListaOffsetID() -> list[tuple[int,int]]:
    '''
    Lê games.dat, pega o id e verifica o offset do registro e os retorna em uma 
    tupla ((offset, id)), faz isso para todos os registros e os coloca em uma 
    lista
    '''
    chaves: list[tuple[int,int]] = []
    try:
        with open(ARQUIVO, 'rb') as arq:
            offset = 0
            bufferTamReg = arq.read(2)
            
            while bufferTamReg:
                tamRegistro = int.from_bytes(bufferTamReg, 'little')
                atual = arq.tell()
                primeiro_byte = arq.read(1)
                # Verifica se o primeiro byte do registro é '*' para indicar que 
                # foi removido
                if primeiro_byte == b'*': 
                    # Foi removido, vai pro proximo registro
                    arq.seek(tamRegistro - 1, os.SEEK_CUR)
                else:
                    # Não foi removido então volta pra posição inicial 
                    arq.seek(atual, os.SEEK_SET)
                    registro = arq.read(tamRegistro).decode().split('|')
                    chave = (offset, int(registro[0]))
                    chaves.append(chave)
                offset += tamRegistro + 2
                bufferTamReg = arq.read(2)

    except FileNotFoundError as e:
        print(f"Erro: {e}")
    return chaves


def buscaElemento(p: Arvore, e: Elemento) -> tuple[bool, int, int]:
    ''' 
    Procura por *e* em *p*, caso encontre retorna True, o RRN e o indice dele, 
    caso contrário, retorna False, -1, -1 
    '''
    # Se a árvore for vazia, não encontrou o elemento
    if p is None:
        return False, -1, -1


    i = 0
    # Procura pelo elemento na página
    while i < len(p.chaves) and p.chaves[i].id < e.id:
        i += 1

    # Encontrou o elemento
    if i < len(p.chaves) and p.chaves[i].id == e:
        return True, p.rrn, i
    
    # Não encontrou o elemento, procura na árvore filha
    else:
        return buscaElemento(p.filhas[i], e)


def insereElemento()








def isFolha(p: Arvore) -> bool:
    ''' Verifica se *p* é uma folha (não possui filhas) '''
    for filha in p.filhas:
        if filha != -1:
            return False
    return True


def exibeArvore(p: Arvore) -> None:
    print("Arvore")


def realizaOperacoes(nomeArq: str) -> None:
    try:
        with open(nomeArq, 'r') as arq:
            for linha in arq:
                linha = linha.strip()
                if not linha or linha.startswith('#'):
                    continue
                operacao = linha.split(' ', 1)
                if len(operacao) < 2:
                    print(f"Erro: linha incorreta - {linha}")
                    continue
                comando = operacao[0]
                argumento = operacao[1]
                match comando:
                    case 'b':
                        # imprimeResultado(comando, argumento, [rPrimario])
                        break

                    case 'i':
                        # s = "Insere registro: " + argumento
                        # print("=" * len(s))
                        # print(s + "\n")
                        # insereRegistro(argumento)
                        # print("=" * len(s) + "\n")
                        break

                    case _:
                        print(f"Operação inválida!")

    except FileNotFoundError as e:
        print(f'Erro: {e}')


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(f"Erro! Uso: {sys.argv[0]} <operador>")
    match sys.argv[1]:
        case '-b':
            chaves = criaListaOffsetID()
            # constroiIndices(chaves)
        case '-e':
            if len(sys.argv) != 3:
                sys.exit(f"Erro! Uso: {sys.argv[0]} <-e> <operações>")
            else:
                realizaOperacoes(sys.argv[2])


if __name__ == "__main__":
    main()