from __future__ import annotations
from dataclasses import dataclass
import io
import os
import sys
from struct import pack, unpack, calcsize

## Variáveis Globais ##

ORDEM = 5
ARQUIVO = "games.dat"
ARVORE = "arvoreB.dat"

# Variáveis Struct #

FORMATO_CAB = 'i'         # RRN do topo da árvore B 
FORMATO_ELEM = '2is'      # Valor de 8 bytes para id e offset + '|' 
FORMATO_FILHA = 'is'      # Valor de 4 bytes + '|'
SIZE_OF_CAB = calcsize(FORMATO_CAB)
SIZE_OF_ELEM = calcsize(FORMATO_ELEM)
SIZE_OF_FILHA = calcsize(FORMATO_FILHA)
SIZE_OF_PAGINA = SIZE_OF_ELEM * (ORDEM -1) + SIZE_OF_FILHA * ORDEM


@dataclass
class Elemento:
    id: int
    offset: int


@dataclass
class Pagina:
    chaves: list[Elemento]     # Lista com os elementos da página
    filhas: list[int]          # Uma lista com o rrn das páginas filhas 
    rrn: int                   # RRN da página atual
    def __init__(self):
        self.chaves = []
        self.filhas = [None] * ORDEM

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
            tamRegistro = int.from_bytes(arq.read(2), 'little')
            while tamRegistro > 0:
                registro =  (arq.read(tamRegistro).decode()).split('|')
                chave = (offset, int(registro[0]))
                chaves.append(chave)
                offset += tamRegistro + 2
                tamRegistro = int.from_bytes(arq.read(2), 'little') 
    except FileNotFoundError as e:
        print(f"Erro: {e}")
    return chaves


def buscaElemento(id: int, rrn: int | None) -> tuple[bool, int]:
    ''' 
    Procura por *id* em *ARVORE*, caso encontre retorna True e seu offset, caso 
    contrário, retorna False e -1
    '''
    try:
        with open(ARVORE, 'rb+') as arvore:
            # Primeira chamada da função
            if rrn is None:
                rrn = unpack(FORMATO_CAB, arvore.read(SIZE_OF_CAB))[0]
            # Segunda chamada da função
            if rrn is -1:
                return False, -1
                
            offsetRaiz = rrn * SIZE_OF_PAGINA
            arvore.seek(offsetRaiz, os.SEEK_SET)
            i = 0
            while i < (ORDEM - 1):
                idArvore, offset, _ = unpack(FORMATO_ELEM, arvore.read(SIZE_OF_ELEM))
                if id == idArvore:
                    return True, offset
                if id < idArvore or idArvore == -1:
                    filha = (ORDEM - i - 2) * SIZE_OF_ELEM + i * SIZE_OF_FILHA 
                    arvore.seek(filha, os.SEEK_CUR)
                    rrnFilha = unpack(FORMATO_FILHA, arvore.read(SIZE_OF_FILHA))[0]
                    return buscaElemento(id, rrnFilha)
                i += 1
            if i == ORDEM - 1:
                filha = i * SIZE_OF_FILHA
                arvore.seek(filha, os.SEEK_CUR)
                rrnFilha = unpack(FORMATO_FILHA, arvore.read(SIZE_OF_FILHA))[0]
                return buscaElemento(id, rrnFilha)
            return False, -1
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return False, -1
    
    
def insereElemento(e: Elemento) -> tuple[bool, Pagina]:
    '''
    Insere o elemento *e* na *ARVORE*, caso o id do elemento *e* já exista na 
    *ARVORE*, *e* será descartado 
    '''
    return True, Pagina()


def isFolha(p: Pagina) -> bool:
    ''' Verifica se *p* é uma folha (não possui filhas) '''
    if p is None:
        return True
    for filha in p.filhas:
        if filha is not None:
            return False
    return True


def exibeArvore() -> None:
    try:
        with open(ARVORE, 'rb') as arvore:
            print("Arvore")
    except FileNotFoundError as e:
        print(f"Erro: {e}")

def realizaOperacoes(nomeArq: str) -> None:
    try:
        with open(nomeArq, 'r') as arq, open(ARVORE, 'r+b'):
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
                        
                        # imprimeResultado(comando, argumento)
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
    buscaElemento(1)
    # if len(sys.argv) < 2:
    #     sys.exit(f"Erro! Uso: {sys.argv[0]} <operador>")
    # match sys.argv[1]:
    #     case '-b':
    #         chaves = criaListaOffsetID()
    #         for offset, id in chaves:
    #             e = Elemento(id, offset)


    #         # constroiIndices(chaves)
    #     case '-e':
    #         if len(sys.argv) != 3:
    #             sys.exit(f"Erro! Uso: {sys.argv[0]} <-e> <operações>")
    #         else:
    #             realizaOperacoes(sys.argv[2])
    # 
    #      case -p:
    #          exibeArvore() 


if __name__ == "__main__":
    main()