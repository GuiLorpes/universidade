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

# Arvore
FORMATO_CAB = 'i'         # RRN do topo da árvore B 
FORMATO_ELEM = '2is'      # Valor de 8 bytes para id e offset + '|' 
FORMATO_FILHA = 'is'      # Valor de 4 bytes + '|'
SIZE_OF_CAB = calcsize(FORMATO_CAB)
SIZE_OF_ELEM = calcsize(FORMATO_ELEM)
SIZE_OF_FILHA = calcsize(FORMATO_FILHA)
SIZE_OF_PAGINA = SIZE_OF_ELEM * (ORDEM -1) + SIZE_OF_FILHA * ORDEM

# Games.dat
FORMATO_TAMREG = 'h'     # Valor de 2 bytes
FORMATO_REG = 's'        # String
SIZE_OF_TAMREG = calcsize(FORMATO_TAMREG)


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

def criaListaOffsetID() -> list[Elemento]:
    '''
    Lê games.dat, pega o id e verifica o offset do registro e os retorna em uma 
    tupla ((offset, id)), faz isso para todos os registros e os coloca em uma 
    lista
    '''
    chaves: list[Elemento] = []
    try:
        with open(ARQUIVO, 'rb') as arq:
            offset = 0
            tamBytes = arq.read(SIZE_OF_TAMREG)
            while len(tamBytes) == SIZE_OF_TAMREG:
                tamRegistro = unpack(FORMATO_TAMREG, tamBytes)[0]
                registro = (arq.read(tamRegistro).decode()).split('|')
                chave = Elemento(int(registro[0]), offset)
                chaves.append(chave)
                offset += tamRegistro + 2
                tamBytes = arq.read(SIZE_OF_TAMREG)
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
            if rrn == -1:
                return False, -1
                
            offsetRaiz = SIZE_OF_CAB + (rrn * SIZE_OF_PAGINA)
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


def novoRRN(arvore: io.BufferedRandom) -> int:
    fim = arvore.seek(0, os.SEEK_END)
    return (fim - 4) // SIZE_OF_PAGINA


def dividePagina(p: Pagina) -> tuple[Pagina, Elemento, Pagina]:
    ''' 
    Divide *p* e retorna a primeira metade da página, o elemento a ser promovido 
    e a nova página
    '''
    pagEsq = Pagina()
    pagDir = Pagina()
    
    meio = len(p.chaves) // 2

    promovido = p.chaves[meio]

    pagEsq.chaves = p.chaves[:meio]
    pagDir.chaves = p.chaves[meio+1:]

    pagEsq.rrn = p.rrn
    pagDir.rrn = -1

    pagEsq.filhas = p.filhas[:meio+1]
    pagDir.filhas = p.filhas[meio+1:]
    while len(pagEsq.filhas) < ORDEM:
        pagEsq.filhas.append(-1)
    while len(pagDir.filhas) < ORDEM:
        pagDir.filhas.append(-1)
    
    return pagEsq, promovido, pagDir


def lePagina(arvore: io.BufferedRandom, rrn: int) -> Pagina:
    ''' Lê os valores da página no *rrn* em *arvore* '''
    offset = SIZE_OF_CAB + (rrn * SIZE_OF_PAGINA)
    arvore.seek(offset, os.SEEK_SET)
    p = Pagina()
    # Lista com os elementos
    chaves: list[Elemento] = []
    filhas: list[int] = []

    ## Lista de elementos
    for i in range(ORDEM - 1) :
        idArvore, offset, _ = unpack(FORMATO_ELEM, 
                                        arvore.read(SIZE_OF_ELEM))
        if idArvore != -1:
            elemento = Elemento(idArvore, offset)
            chaves.append(elemento)
        
    ## Lista das filhas
    for i in range(ORDEM):
        rrnFilha = unpack(FORMATO_FILHA, 
                            arvore.read(SIZE_OF_FILHA))[0]
        filhas.append(rrnFilha)

    p.chaves = chaves
    p.filhas = filhas
    p.rrn = rrn

    return p


def gravaPagina(arvore: io.BufferedRandom, p: Pagina) -> None:
    ''' Grava *p* na *arvore* em seu respectivo rrn '''
    offset = 4 + (p.rrn * SIZE_OF_PAGINA)
    arvore.seek(offset,os.SEEK_SET)
    while len(p.chaves) < ORDEM - 1:
        p.chaves.append(Elemento(-1,-1))
    while len(p.filhas) < ORDEM:
        p.filhas.append(-1)
    for i in range (ORDEM - 1):
        arvore.write(pack(FORMATO_ELEM, p.chaves[i].id, \
                            p.chaves[i].offset, b'|'))
    for i in range (ORDEM):
        arvore.write(pack(FORMATO_FILHA, p.filhas[i], b'|'))


def insereNaPagina(arvore: io.BufferedRandom,e: Elemento, rrn: int) -> \
    tuple[Elemento, int] | None:
    '''
    Insere *e* na página presente no *rrn* em *arvore*, caso houver promoção, 
    retorna o elemento a ser promovido e seu rrn, caso nenhum elemento ser 
    promovido retorna None
    '''
    p = lePagina(arvore, rrn)

    ## Está na folha (não teve promoção (ainda))
    if isFolha(p):
        p.chaves.append(e)
        p.chaves.sort(key=lambda elem: elem.id)

        if len(p.chaves) <= ORDEM - 1:
            gravaPagina(arvore, p)
            return None
        
        pagEsq, promovido, pagDir = dividePagina(p)

        pagDir.rrn = novoRRN(arvore)
        gravaPagina(arvore, pagEsq)
        gravaPagina(arvore, pagDir)

        return promovido, pagDir.rrn
    
    ## Ainda não está na folha
    indiceFilha = 0
    while indiceFilha < len(p.chaves) and e.id > p.chaves[indiceFilha].id:
        indiceFilha += 1

    rrnFilha = p.filhas[indiceFilha]
    promocao = insereNaPagina(arvore, e, rrnFilha)
    
    if promocao is None:
        return None

    promovido, rrnDir = promocao 
    p.chaves.insert(indiceFilha, promovido)  
    p.filhas.insert(indiceFilha + 1, rrnDir)

    if len(p.chaves) <= ORDEM - 1:
        gravaPagina(arvore, p)
        return None
    
    pagEsq, promovido, pagDir = dividePagina(p)

    pagDir.rrn = novoRRN(arvore)
    gravaPagina(arvore, pagEsq)
    gravaPagina(arvore, pagDir)

    return promovido, pagDir.rrn

    
def insereElemento(e: Elemento) -> bool:
    '''
    Insere o elemento *e* na *ARVORE*, caso o id do elemento *e* já exista na 
    *ARVORE*, *e* será descartado 
    '''
    try :
        with open(ARVORE, 'r+b') as arvore, open(ARQUIVO, 'ab') as arq:
            if buscaElemento(e.id, None)[0]:
                return False
            
            rrnRaiz = unpack(FORMATO_CAB, arvore.read(SIZE_OF_CAB))[0]
            
            promocao = insereNaPagina(arvore, e, rrnRaiz)


            if promocao is not None:
                promovido, rrnDir = promocao

                novaRaiz = Pagina()
                novaRaiz.rrn = novoRRN(arvore)
                novaRaiz.chaves = [promovido]
                novaRaiz.filhas = [rrnRaiz, rrnDir]

                gravaPagina(arvore, novaRaiz)

                arvore.seek(0, os.SEEK_SET)
                arvore.write(pack(FORMATO_CAB, novaRaiz.rrn))
            return True
            
    except FileNotFoundError as e:
        print(f"Erro: {e}") 
    return False


def criaArvore(chaves: list[Elemento]) -> None:
    with open(ARVORE, 'wb') as arvore:
        rrn = 0
        arvore.write(pack(FORMATO_CAB, rrn))
        for _ in range (ORDEM - 1):
            arvore.write(pack(FORMATO_ELEM, -1,-1, b'|'))
        for _ in range (ORDEM):
            arvore.write(pack(FORMATO_FILHA, -1, b'|'))

    for e in chaves:
        insereElemento(e)
            

def isFolha(p: Pagina) -> bool:
    ''' Verifica se *p* é uma folha (não possui filhas) '''
    for filha in p.filhas:
        if filha != -1:
            return False
    return True


def exibeArvore() -> None:
    try:
        with open(ARVORE, 'rb') as arvore:
            raiz = unpack(FORMATO_CAB, arvore.read(SIZE_OF_CAB))[0]
            fim = arvore.seek(0, os.SEEK_END)
            totalRRN = (fim - 4) // SIZE_OF_PAGINA

            for rrn in range(totalRRN):
                arvore.seek(SIZE_OF_CAB + (rrn * SIZE_OF_PAGINA))
                if rrn == raiz:
                    print("* ------- * RAIZ * ------- *")

                chaves: list[int] = []
                offsets: list[int] = []
                filhas: list[int] = []

                for _ in range(ORDEM - 1) :
                    chave, offset, _ = unpack(FORMATO_ELEM, 
                                                    arvore.read(SIZE_OF_ELEM))
                    chaves.append(chave)
                    offsets.append(offset)
                for _ in range(ORDEM):
                    rrnFilha = unpack(FORMATO_FILHA, 
                                        arvore.read(SIZE_OF_FILHA))[0]
                    filhas.append(rrnFilha)
                
                print(f"Página: {rrn}: ")
                stringChaves = 'Chaves = | '
                stringOffset = 'Offsets = | '
                stringFilhas = 'Filhas = | '
                for c in chaves:
                    stringChaves += str(c) + ' | '
                for o in offsets:
                    stringOffset += str(o) + ' | '
                for f in filhas:
                    stringFilhas += str(f) + ' | '
                
                print(stringChaves + '\n' + stringOffset + '\n' + stringFilhas)
                if rrn == raiz:
                    print("* ------------------------ *")
                print()
                

    except FileNotFoundError as e:
        print(f"Erro: {e}")


def realizaOperacoes(nomeArq: str) -> None:
    try:
        with open(nomeArq, 'r') as op, open(ARQUIVO, 'r+b') as arq:
            for linha in op:
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
                        achou, offset = buscaElemento(int(argumento), None)
                        if not achou:
                            print("=" * (23 + len(argumento)))
                            print(f"Busca pelo item de ID: {argumento}\n")
                            print("ID não encontrado!")
                            print('=' * (23 + len(argumento)) + '\n')
                        else:
                            arq.seek(offset, os.SEEK_SET)
                            tamReg = unpack(FORMATO_TAMREG, 
                                                arq.read(SIZE_OF_TAMREG))[0]
                            reg = arq.read(tamReg).decode()
                            print("=" * len(reg))
                            print(f"Busca pelo item de ID: {argumento}\n")
                            print(reg)
                            print('=' * len(reg) + '\n')

                    case 'i':
                        s = "Insere registro: " + argumento
                        id = int(argumento.split('|')[0])
                        print("=" * len(s))
                        print(s + "\n")
                        arq.seek(0, os.SEEK_END)
                        offset = arq.tell()
                        arq.write(pack(FORMATO_TAMREG, len(argumento)))
                        arq.write(argumento.encode())
                        e = Elemento(id, offset)
                        if insereElemento(e):
                            print("Registro inserido com sucesso!")
                        else:
                            print("ID já existe!")
                        print("=" * len(s) + "\n")

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
            criaArvore(chaves)
        case '-e':
            if len(sys.argv) != 3:
                sys.exit(f"Erro! Uso: {sys.argv[0]} <-e> <operações>")
            else:
                realizaOperacoes(sys.argv[2])

        case '-p':
            exibeArvore() 


if __name__ == "__main__":
    main()