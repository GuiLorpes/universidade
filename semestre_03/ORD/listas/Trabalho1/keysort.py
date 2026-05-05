from __future__ import annotations
import os
import io
import sys
from dataclasses import dataclass
from struct import pack, unpack, calcsize

# Variaveis globais para o struct

FORMATO_ELEMLISTA = '2i'    # dois inteiros de 4 bytes
FORMATO_CAB = 'i'        # um inteiro de 4 bytes
FORMATO_TAMREG = 'h'        # um inteiro de 2 bytes
SIZEOF_ELEMLISTA = calcsize(FORMATO_ELEMLISTA)      # 8 bytes
SIZEOF_CAB = calcsize(FORMATO_CAB)            # 4 bytes
SIZEOF_TAMREG = calcsize(FORMATO_TAMREG)            # 2 bytes


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
    generosPrimeiro: list[tuple[int | str, int]] = []

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
        generosPrimeiro.append((genero.id, genero.prox.pos))
    print(generosPrimeiro)
        
    # Cria uma lista com as publicadoras com a primeira ocorrencia de cada
    publicadorasPrimeiro: list[tuple[int | str, int]] = []
    
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
        publicadorasPrimeiro.append((publicadora.id, publicadora.prox.pos))
    print(publicadorasPrimeiro)
    
    
    # # Cria arquivo com indice primário
    # with open("primario.ind", "wb") as chavePrimaria:
    #     # Escreve o cabeçalho com 4 bytes
    #     cabecalho = pack(len(listaIDs))
    
    # # Cria arquivo com indice secundário de genero 
    # with open("genero.ind", "wb") as chaveSec1:
    #     for g in generosPrimeiro:
    #         chaveSec1.write(g[0].encode() + b'|')
    #         chaveSec1.write(g[1].to_bytes(4, 'little') + b'|')

    # # Cria arquivo com indice secundário de publicadora
    # with open("publicadora.ind", "wb") as chaveSec2:
    #     listaPublicadoras = []
    #     for r in registro:
    #         if r[3] not in listaPublicadoras:
    #             listaPublicadoras.append(r[3])
    #     listaPublicadoras.sort()
    #     for p in listaPublicadoras:
    #         chaveSec2.write(p.encode() + b'|')

    # # Cria arquivo com a lista invertida
    # with open("listaInvertida.lst", "wb") as lstInvertida:
    #     listaInvertida = criaListaInvertida(registro)
    #     for i in listaInvertida:
    #         # tem que usar o struct aqui, ainda não vimos
    #         id = i[0].to_bytes(4, 'little')
    #         proxGen = i[1].to_bytes(4, 'little')
    #         proxPub = i[2].to_bytes(4, 'little')
    #         lstInvertida.write(id + proxGen + proxPub + b'|')


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
    with open("games.dat", "rb") as bp, open("primario.ind", "rb") as indices:
        # offset nos indices = i * 9 + 4
        i_min = 0
        i_max = int.from_bytes(indices.read(4), 'little') - 1
        while i_min <= i_max:
            i_meio = (i_max + i_min) // 2
            offset = i_meio * 9 + 4
            indices.seek(offset, os.SEEK_SET)
            vMedio = int.from_bytes(indices.read(4), 'little') 
            if int(id) == vMedio:
                bpOffset = int.from_bytes(indices.read(4), 'little') 
                bp.seek(bpOffset, os.SEEK_SET)
                tamReg = int.from_bytes(bp.read(2), 'little')
                item = bp.read(tamReg).decode()
                return item
            elif int(id) < vMedio:
                i_max = i_meio - 1
            else:
                i_min = i_meio + 1
    return item

# Buscas secundárias vou precisar do struct :(


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

        


if __name__ == "__main__":
    main()
