from __future__ import annotations
from dataclasses import dataclass
import io
import os

ORDEM = 5

@dataclass
class Elemento:
    id: int
    offset: int


@dataclass
class Pagina:
    chaves: list[Elemento] 
    filhas: list[Arvore]
    rrn: int
    def __init__(self):
        self.chaves = []
        self.filhas = [Arvore] * ORDEM

Arvore = Pagina | None

def criaListaOffsetID(nomeArq: str) -> list[tuple[int,int]]:
    '''
    Lê games.dat, pega o id e verifica o offset do registro e os retorna em uma 
    tupla ((offset, id)), faz isso para todos os registros e os coloca em uma 
    lista
    '''
    chaves: list[tuple[int,int]] = []
    with open(nomeArq, 'rb') as arq:
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

    # O(n)
    return chaves

def buscaElemento(p: Arvore, e: Elemento) -> bool:
    '''
    Procura em *p* por *e*, caso não encontre, procura em suas filhas
    Retorna True se encontrou o elemento e False caso contrário
    '''
    if p is None:
        return False

    i = 0
    while i < len(p.chaves) and p.chaves[i].id < e.id:
        i += 1
    
    if i < len(p.chaves) and p.chaves[i].id == e:
        return True

    else:
        return buscaElemento(p.filhas[i], e)

def insereElemento(p: Arvore, e: Elemento) -> bool:
    '''
    Insere *elemento* na árvore *p*, *elemento* não pode ser igual a nenhuma 
    chave de *p*, caso foi possivel inserir o elemento, retorna True, caso 
    contrário False 
    '''
    if buscaElemento(p, e):
        print(f"O elemento {e.id} já está na árvore!")
        return False

    if p is None:
        p = Pagina()
        p.chaves.append(e)
        return True

    if len(p.chaves) < ORDEM - 1:
        p.chaves.append(e)
        return True

    i = 0
    while i < len(p.chaves) and p.chaves[i].id > e.id:
        i += 1
    if i == len(p.chaves):
        return insereElemento(p.filhas[i], e)


    return False


def eh_folha(p: Pagina) -> bool:
    ''' Verifica se *p* é uma folha, ou seja, se *p* não possui filhas '''
    for pagina in p.filhas:
        if pagina is not None:
            return False
    return True


def exibeArvore(p: Arvore) -> None:
    print("Arvore")


def main() -> None:
    print("Insira o nome do arquivo que deseja usar:")
    nomeArq = input()
    arvore = nomeArq.split('.')[0] + 'ARVORE.dat'




if __name__ == "__main__":
    main()