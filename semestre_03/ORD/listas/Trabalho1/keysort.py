from __future__ import annotations
import os
import io
import sys
from dataclasses import dataclass
from struct import pack, unpack, calcsize

# Variaveis globais para o struct

FORMATO_LISTAINV = 'isisis'                     # três inteiros de 4 bytes 
                                                # separados por 2 bytes de '|'
SIZEOF_LISTINV = calcsize(FORMATO_LISTAINV)     # 15 bytes


# Essas duas classes são classes auxiliares para a fila invertida
@dataclass
class Node:
    anterior: Node
    id: int | str
    pos: int
    prox: Node
    def __init__(self, id: int | str, pos: int):
        self.anterior = None # type: ignore
        self.id = id
        self.pos = pos
        self.prox = None # type: ignore

def insere_depois(p: Node, novo: Node):
    '''Insere *novo* após *p* no encademaneto.'''
    novo.anterior = p
    novo.prox = p.prox
    p.prox.anterior = novo
    p.prox = novo

class Lista:
    sentinela: Node
    def __init__(self, tipo: int | str):
        self.sentinela = Node(tipo, -1)
        self.sentinela.anterior = self.sentinela
        self.sentinela.prox = self.sentinela
    def vazio(self) -> bool:
        return self.sentinela.prox is self.sentinela
    def insereOrdenado(self, novo: Node):
        if self.vazio():
            insere_depois(self.sentinela, novo)
        else:
            q = self.sentinela.prox
            while q is not self.sentinela and q.id < novo.id:
                q = q.prox
            insere_depois(q.anterior, novo)
    def listaIDeProx(self) -> list[tuple[int |str , int]]:
        ''' Retorna uma lista de tuplas com o id e a proxima posição '''
        lista: list[tuple[int | str, int]] = []
        q = self.sentinela
        while q.prox.pos != -1:
            lista.append((q.id, q.prox.pos))
            q = q.prox
        return lista

# Fim das classes auxiliares


def criaListaOffsetChaves(nomeArq: str) -> list[tuple[int,int,str,str]]:
    '''
    Lê *nomeArq*, pega o id, o genero e a publicadora, e verifica o offset do 
    registro e os retorna em uma tupla ((offset, id, genero, publicadora)), faz
    isso para todos os registros e os coloca em uma lista
    '''
    chaves: list[tuple[int,int,str,str]] = []
    with open(nomeArq, 'rb') as arq:
        offset = 0
        tamRegistro = int.from_bytes(arq.read(2), 'little')
        while tamRegistro > 0:
            registro =  (arq.read(tamRegistro).decode()).split('|')
            chave = (offset, int(registro[0]), registro[3], registro[4])
            chaves.append(chave)
            offset += tamRegistro + 2
            tamRegistro = int.from_bytes(arq.read(2), 'little') 
    return chaves


def constroiIndices(chaves: list[tuple[int,int,str,str]]) -> None:
    '''
    Com base no *nomeArq* cria 4 arquivos novos, primario.ind, genero.ind, 
    publicadora.ind e listaInvertida.lst, onde cada um dos .ind são ordenados 
    de acordo com as chaves primária, secundária de gênero e secundária de 
    publicadora. 
    Os *registros* estarão com o offset de cada um dos elementos, e serão 
    ordenadas de acordo com cada uma das chaves e serão escritos em seus 
    respectivos arquivos
    '''
    # Cria o arquivo com todos os IDs e seus offsets em "games.dat"
    listaIDs: list[tuple[int, int]] = []
    for r in chaves:
        listaIDs.append((r[1], r[0]))
    listaIDs.sort()
    
    # Cria a lista invertida vazia para ser organizada
    listaInvertida: list[list[int]] = []
    for r in chaves:
        listaInvertida.append([r[1], -1, -1])

    # Cria a lista com todos os generos no registro
    listaGeneros = []
    for r in chaves:
        if r[2] not in listaGeneros:
            listaGeneros.append(r[2])
    listaGeneros.sort()
    
    # Cria a lista com todas as publicadoras no registro
    listaPublicadoras = []
    for r in chaves:
        if r[3] not in listaPublicadoras:
            listaPublicadoras.append(r[3])
    listaPublicadoras.sort()

    # Cria uma lista com os generos com a primeira ocorrencia de cada
    generosPrimeiro: list[tuple[str, int]] = []

    # Organiza os generos primeiro 
    # Encontrar todos de um genero para atualizar na lista
    for g in listaGeneros:
        nodeGenero = Lista(g)
        # Acha o primeiro registro do genero
        # Os generos já foram inseridos a partir dos registros, então não 
        # precisa verificar se i < len(registros), já que é certeza que o 
        # genero vai ter pelo menos um elemento dele!
        i = 0
        while chaves[i][2] != g:
            i += 1
        nodeGenero.insereOrdenado(Node(chaves[i][1], i))
        # nodeGenero sempre aponta para o inicio do nó 
        j = i + 1
        while j < len(chaves):
            if chaves[j][2] == g:
                novoNode = Node(chaves[j][1], j)
                nodeGenero.insereOrdenado(novoNode)
            j += 1
        doGenero = nodeGenero.listaIDeProx()[1:]
        for item in doGenero:
            i = 0
            # Novamente, com certeza vai ter um listaInvertida[i] com id igual 
            # ao do r, então não é necessário fazer a verificação se ele existe
            while listaInvertida[i][0] != item[0]:
                i += 1
            listaInvertida[i][1] = item[1]
        genero = nodeGenero.sentinela
        generosPrimeiro.append((str(genero.id), genero.prox.pos))
    print(generosPrimeiro)
        
    # Cria uma lista com as publicadoras com a primeira ocorrencia de cada
    publicadorasPrimeiro: list[tuple[str, int]] = []
    
    # Organiza as publicadoras
    for p in listaPublicadoras:
        nodePublicadora = Lista(p)
        i = 0
        while chaves[i][3] != p:
            i += 1
        nodePublicadora.insereOrdenado(Node(chaves[i][1], i))
        j = i + 1
        while j < len(chaves):
            if chaves[j][3] == p:
                novoNode = Node(chaves[j][1], j)
                nodePublicadora.insereOrdenado(novoNode)
            j += 1
        daPublicadora = nodePublicadora.listaIDeProx()[1:]
        for item in daPublicadora:
            i = 0
            while listaInvertida[i][0] != item[0]:
                i += 1
            listaInvertida[i][2] = item[1]
        publicadora = nodePublicadora.sentinela     
        publicadorasPrimeiro.append((str(publicadora.id), publicadora.prox.pos))
    print(publicadorasPrimeiro)
    
    print(listaInvertida)

    # Cria arquivo com indice primário
    with open("primario.ind", "wb") as chavePrimaria:
        # Escreve o cabeçalho com 4 bytes
        cabecalho = len(listaIDs).to_bytes(4, 'little')
        chavePrimaria.write(cabecalho)
        for chave in listaIDs:
            chavePrimaria.write(chave[0].to_bytes(4, 'little'))
            chavePrimaria.write(chave[1].to_bytes(4, 'little'))
    
    # Cria arquivo com indice secundário de genero 
    with open("genero.ind", "wb") as chaveSec1:
        for g, pos in generosPrimeiro:
            # tamanho do registro = len(palavra) + bytes do offset + 2 '|'
            tamreg = len(g) + 4 + 2
            chaveSec1.write(tamreg.to_bytes(2, 'little'))
            chaveSec1.write(g.encode() + b'|')
            chaveSec1.write(pos.to_bytes(4, 'little'))
            chaveSec1.write(b'|')

    # Cria arquivo com indice secundário de publicadora
    with open("publicadora.ind", "wb") as chaveSec2:
        for p, pos in publicadorasPrimeiro:
            tamreg = len(p) + 4 + 2
            chaveSec2.write(tamreg.to_bytes(2, 'little'))
            chaveSec2.write(p.encode() + b'|')
            chaveSec2.write(pos.to_bytes(4, 'little'))
            chaveSec2.write(b'|')

    # Cria arquivo com a lista invertida
    with open("listaInvertida.lst", "wb") as lstInvertida:
        tamreg = len(listaInvertida)
        lstInvertida.write(tamreg.to_bytes(4, 'little'))
        for id, proxG, proxP in listaInvertida:
            lstInvertida.write(pack(FORMATO_LISTAINV, id, proxG, proxP))
            
            


def mergesort(registros: list[tuple[int,int,str,str]], chave: int) -> None:
    ''' Ordena uma lista de registros de acordo com a chave inserida '''

    # Caso base (1 elemento)
    tamanhoRegistros = len(registros)
    if tamanhoRegistros <= 1:
        return
    
    # Divide a lista em duas
    meio = tamanhoRegistros // 2
    esq = registros[:meio]
    dir = registros[meio:]

    # Organiza as duas metades
    mergesort(esq, chave)
    mergesort(dir, chave)

    i = 0   # Elementos da esquerda
    j = 0   # Elementos da direita 
    k = 0   # Elementos do registro

    # Junta as duas metades
    while i < len(esq) and j < len(dir):

        # Se esq[i] < dir[j], adiciona troca registro[k] por esq[i]
        if esq[i][chave] <= dir[j][chave]:
            registros[k] = esq[i]
            i += 1

        # Se esq[i] > dir[j], adiciona troca registro[k] por dir[j]
        else: # esq[i][chave] >= dir[j][chave]
            registros[k] = dir[j]
            j += 1
        k += 1

    # Adiciona os elementos restantes da esquerda
    while i < len(esq):
        registros[k] = esq[i]
        i += 1
        k += 1

    # Adiciona os elementos restantes da direita
    while j < len(dir):
        registros[k] = dir[j]
        j += 1
        k += 1
    

def buscaPrimaria(id: str) -> str:
    '''
    Procura pelo item com *id*, e retorna seus campos separados por '|' em uma 
    string, caso não encontre o item, retorna uma string vazia
    Ex:
    >>> buscaPrimaria(459)
        "459|Fortnite|2017|Sandbox|Epic Games|PC|" 
    '''
    item = ''
    with open("games.dat", "rb") as arq, open("primario.ind", "rb") as indices:
        # offset nos indices = i * 8 + 4
        i_min = 0
        i_max = int.from_bytes(indices.read(4), 'little') - 1
        while i_min <= i_max:
            i_meio = (i_max + i_min) // 2
            offset = i_meio * 8 + 4
            indices.seek(offset, os.SEEK_SET)
            vMedio = int.from_bytes(indices.read(4), 'little') 
            if int(id) == vMedio:
                bpOffset = int.from_bytes(indices.read(4), 'little') 
                arq.seek(bpOffset, os.SEEK_SET)
                tamReg = int.from_bytes(arq.read(2), 'little')
                item = arq.read(tamReg).decode()
                return item
            elif int(id) < vMedio:
                i_max = i_meio - 1
            else:
                i_min = i_meio + 1
    return item

# Buscas secundárias

# Busca secundária de gênero

def buscaSecGenero(genero:str) -> list[str]:
    '''
    Procura por itens do mesmo *genero* e os retorna numa lista, caso não 
    exista retorna lista vazia.
    '''
    listaOffsets = []
    try:
        with open("genero.ind", "rb") as generos, \
            open("listaInvertida.lst", "rb") as lstInv, \
            open("primario.ind","rb") as id:
            primeiro = -1
            tamReg = generos.read(2)
            buffer = generos.read(int.from_bytes(tamReg, 'little')).decode()
            g = buffer.split('|')
            while g[0] != genero and tamReg:
                tamReg = generos.read(2)
                buffer = generos.read(int.from_bytes(tamReg, 'little')).decode()
                g = buffer.split('|')
            if g[0] == genero:
                primeiro = int(g[1])
                tamLista = int.from_bytes(lstInv.read(4), 'little')
                lstInv.seek(primeiro * SIZEOF_LISTINV + 4, os.SEEK_SET)
                listaInvertida = unpack(FORMATO_LISTAINV, \
                                        lstInv.read(SIZEOF_LISTINV))
                while listaInvertida[1] != -1:
                    offset = listaInvertida[1] * 8 + 4
                    # Precisa do + 4 para ler o offset do Id
                    id.seek(offset + 4, os.SEEK_SET)
                    offsetID = int.from_bytes(id.read(4), 'little')
                    listaOffsets.append(offsetID)
                    lstInv.seek(listaInvertida[1] * SIZEOF_LISTINV + 4, \
                                os.SEEK_SET)
                    listaInvertida = unpack(FORMATO_LISTAINV, \
                                            lstInv.read(SIZEOF_LISTINV))
            elif primeiro == -1:
                return []
        with open("games.dat", "rb") as games:
            
        return []
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return[]



def insereRegistro(registro: str) -> None:
    try:
        campos = registro.split('|')
        # Verifica se encontra um id igual
        # Se encontrou, não insere
        if buscaPrimaria(campos[0]) != '':
            print("ID já existe!")
            return
        with open("games.dat", "r+b") as arq:
            arq.seek(0, os.SEEK_END)
            tamBytes = len(registro).to_bytes(2, 'little')
            arq.write(tamBytes)
            arq.write(registro.encode())

        chaves = criaListaOffsetChaves("games.dat")
        constroiIndices(chaves)
        print("Registro inserido com sucesso!")
            
    except OSError as e:
        print(f"Erro: {e}")


def realizaOperacoes(nomeArq: str) -> None:
    try:
        with open(nomeArq, 'rb') as operacoes:
            raise NotImplementedError
        
        
    # case 'i':
    #         if len(sys.argv) != 4:
    #             sys.exit(f"Erro! Uso: {sys.argv[0]} <nome_do_arquivo> <-i> "\
    #                      "<registro>")
    #         else:
    #             insereRegistro(sys.argv[3])
    except FileNotFoundError as e:
        print(f'Erro: {e}')

def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(f"Erro! Uso: {sys.argv[0]} <nome_do_arquivo> <operador>")
    if not os.path.isfile(sys.argv[1]):
        raise FileNotFoundError('Insira um arquivo válido')
    
    match sys.argv[2]:
        case '-b':
            chaves = criaListaOffsetChaves(sys.argv[1])
            constroiIndices(chaves)
        case '-e':
            if len(sys.argv) != 4:
                sys.exit(f"Erro! Uso: {sys.argv[0]} <nome_do_arquivo> <-e> "\
                         "<operações>")
            else:
                realizaOperacoes(sys.argv[3])
            raise NotImplementedError
        case 'b1':
            print(buscaPrimaria(sys.argv[3]))

        


if __name__ == "__main__":
    main()
