from __future__ import annotations
import os
import sys
from dataclasses import dataclass
from struct import pack, unpack, calcsize

# Variaveis globais para o struct

FORMATO_LISTAINV = '3i'                         # Três inteiros de 4 bytes 
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


def criaListaOffsetChaves() -> list[tuple[int,int,str,str]]:
    '''
    Lê games.dat, pega o id, o genero e a publicadora, e verifica o offset do 
    registro e os retorna em uma tupla ((offset, id, genero, publicadora)), faz
    isso para todos os registros e os coloca em uma lista
    '''
    chaves: list[tuple[int,int,str,str]] = []
    with open('games.dat', 'rb') as arq:
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
                chave = (offset, int(registro[0]), registro[3], registro[4])
                chaves.append(chave)
            offset += tamRegistro + 2
            bufferTamReg = arq.read(2)
    return chaves


def criaListasIDGenPubInv(chaves: list[tuple[int,int,str,str]]) -> \
    tuple[list[tuple[int, int]], list[tuple[str, int]], list[tuple[str, int]], \
    list[list[int]]]:
    '''
    Usando as *chaves*, cria 4 listas, a lista com os IDs e seus offsets em 
    games.dat, a lista com os generos e sua primeira ocorrencia na lista 
    invertida, a lista com as publicadoras e sua primeira ocorrencia na lista 
    invertida, e a lista invertida
    '''
    # Cria uma lista para inserir os ids e seus offsets
    listaIDs: list[tuple[int, int]] = []
    # Cria a lista invertida vazia para ser organizada
    listaInvertida: list[list[int]] = []
    # Cria uma lista com todos os generos no registro
    listaGeneros = []
    # Cria uma lista com todas as publicadoras no registro
    listaPublicadoras = []
    for offset, id, gen, pub in chaves:
        listaIDs.append((id, offset)) 
        listaInvertida.append([id, -1, -1])
        if gen not in listaGeneros:
            listaGeneros.append(gen)
        if pub not in listaPublicadoras:
            listaPublicadoras.append(pub)
    listaIDs.sort()
    listaGeneros.sort()
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
    return listaIDs, generosPrimeiro, publicadorasPrimeiro, listaInvertida 

    # Imagino que não seja a forma mais efetiva para arrumar a lista invertida, 
    # mas funciona bem


def constroiIndices(chaves: list[tuple[int,int,str,str]]) -> None:
    '''
    Com base no *nomeArq* cria 4 arquivos novos, primario.ind, genero.ind, 
    publicadora.ind e listaInvertida.lst, onde cada um dos .ind são ordenados 
    de acordo com as chaves primária, secundária de gênero e secundária de 
    publicadora.
    '''
    listaIDs, generosPrimeiro, publicadorasPrimeiro, \
        listaInvertida = criaListasIDGenPubInv(chaves)

    # Cria arquivo com indice primário
    with open("primario.ind", "wb") as chavePrimaria:
        # Escreve o cabeçalho com 4 bytes
        cabecalho = len(listaIDs).to_bytes(4, 'little')
        chavePrimaria.write(cabecalho)
        for id, offset in listaIDs:
            chavePrimaria.write(id.to_bytes(4, 'little'))
            chavePrimaria.write(offset.to_bytes(4, 'little'))
    
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
            

def buscaID(id:int) -> int:
    ''' 
    Procura pelo *id* no arquivo primario.ind e retorna o offset do id no 
    games.dat
    '''
    with open("primario.ind", "rb") as indices:
        # offset nos indices = i * 8 + 4
        idOffset = -1
        i_min = 0
        i_max = int.from_bytes(indices.read(4), 'little') - 1
        achou = False
        while i_min <= i_max and achou == False:
            i_meio = (i_max + i_min) // 2
            offset = i_meio * 8 + 4
            indices.seek(offset, os.SEEK_SET)
            vMedio = int.from_bytes(indices.read(4), 'little') 
            if id == vMedio:
                idOffset = int.from_bytes(indices.read(4), 'little') 
                achou = True
            elif id < vMedio:
                i_max = i_meio - 1
            else:
                i_min = i_meio + 1
        return idOffset

def buscaPrimaria(id: str) -> str:
    '''
    Procura pelo item com *id*, e retorna seus campos separados por '|' em uma 
    string, caso não encontre o item, retorna uma string vazia
    Ex:
    >>> buscaPrimaria(459)
        "459|Fortnite|2017|Sandbox|Epic Games|PC|" 
    '''
    item = ''
    with open("games.dat", "rb") as arq:
        # offset nos indices = i * 8 + 4
        offset = buscaID(int(id))
        if offset == -1:
            return ''
        arq.seek(offset, os.SEEK_SET)
        tamReg = int.from_bytes(arq.read(2), 'little')
        item = arq.read(tamReg).decode()
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
            open("listaInvertida.lst", "rb") as lstInv:
            # Inicio primeiro como -1
            primeiro = -1
            tamReg = int.from_bytes(generos.read(2), 'little')
            buffer = generos.read(tamReg).split(b'|')
            # Pega o genero e o id da lista
            g = buffer[0].decode()
            primeiraAparicao = int.from_bytes(buffer[1], 'little')
            # Procura na lista até encontrar o genero
            while g != genero and tamReg:
                tamReg = int.from_bytes(generos.read(2), 'little')
                buffer = generos.read(tamReg).split(b'|')
                g = buffer[0].decode()
                primeiraAparicao = int.from_bytes(buffer[1], 'little')
            # Verifica se g é igual ao genero
            if g == genero:
                primeiro = int(primeiraAparicao)
                # Vai na lista invertida a primeira ocorrencia e pega o proximo
                lstInv.seek(primeiro * SIZEOF_LISTINV + 4, os.SEEK_SET)
                id, proxG, _ = unpack(FORMATO_LISTAINV, \
                                        lstInv.read(SIZEOF_LISTINV))
                offsetID = buscaID(id)
                listaOffsets.append(offsetID)
                # Enquanto o proximo não for -1, vai procurando os offsets
                while proxG != -1:
                    lstInv.seek(proxG * SIZEOF_LISTINV + 4, \
                                os.SEEK_SET)
                    id, proxG, _ = unpack(FORMATO_LISTAINV, \
                                            lstInv.read(SIZEOF_LISTINV))
                    offsetID = buscaID(id)
                    listaOffsets.append(offsetID)
            else:
                return []
        with open("games.dat", "rb") as games:
            listaDoGenero = []
            for offset in listaOffsets:                
                games.seek(offset, os.SEEK_SET)
                tamReg = int.from_bytes(games.read(2), 'little')
                item = games.read(tamReg).decode()
                listaDoGenero.append(item)
            return listaDoGenero
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return[]


def buscaSecPub(publicadora:str) -> list[str]:
    '''
    Procura por itens da mesma *publicadora* e os retorna numa lista, caso não 
    exista retorna lista vazia.
    '''
    listaOffsets = []
    try:
        with open("publicadora.ind", "rb") as publicadoras, \
            open("listaInvertida.lst", "rb") as lstInv:
            # Inicio primeiro como -1
            primeiro = -1
            tamReg = int.from_bytes(publicadoras.read(2), 'little')
            buffer = publicadoras.read(tamReg).split(b'|')
            # Pega a publicadora e o id da lista
            p = buffer[0].decode()
            primeiraAparicao = int.from_bytes(buffer[1], 'little')
            # Procura na lista até encontrar a publicadora
            while p != publicadora and tamReg:
                tamReg = int.from_bytes(publicadoras.read(2), 'little')
                buffer = publicadoras.read(tamReg).split(b'|')
                p = buffer[0].decode()
                primeiraAparicao = int.from_bytes(buffer[1], 'little')
            # Verifica se p é igual a publicadora
            if p == publicadora:
                primeiro = int(primeiraAparicao)
                # Vai na lista invertida a primeira ocorrencia e pega o proximo
                lstInv.seek(primeiro * SIZEOF_LISTINV + 4, os.SEEK_SET)
                id, _, proxP = unpack(FORMATO_LISTAINV, \
                                        lstInv.read(SIZEOF_LISTINV))
                offsetID = buscaID(id)
                listaOffsets.append(offsetID)
                # Enquanto o proximo não for -1, vai procurando os offsets
                while proxP != -1:
                    lstInv.seek(proxP * SIZEOF_LISTINV + 4, \
                                os.SEEK_SET)
                    id, _, proxP = unpack(FORMATO_LISTAINV, \
                                            lstInv.read(SIZEOF_LISTINV))
                    offsetID = buscaID(id)
                    listaOffsets.append(offsetID)
            else:
                return []
        with open("games.dat", "rb") as games:
            listaDaPublicadora = []
            for offset in listaOffsets:                
                games.seek(offset, os.SEEK_SET)
                tamReg = int.from_bytes(games.read(2), 'little')
                item = games.read(tamReg).decode()
                listaDaPublicadora.append(item)
            return listaDaPublicadora
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return[]


def insereRegistro(registro: str) -> bool:
    try:
        campos = registro.split('|')
        # Verifica se encontra um id igual
        # Se encontrou, não insere
        if buscaID(int(campos[0])) != -1:
            print("ID já existe!")
            return False
        with open("games.dat", "r+b") as arq:
            arq.seek(0, os.SEEK_END)
            tamBytes = len(registro).to_bytes(2, 'little')
            arq.write(tamBytes)
            arq.write(registro.encode())

        chaves = criaListaOffsetChaves()
        constroiIndices(chaves)
        print("Registro inserido com sucesso!")
        return True
            
    except OSError as e:
        print(f"Erro: {e}")
        return False


def removeRegistro(id: str) -> bool:
    ''' 
    Procura pelo registro do *id* e remove aquele registro, colocando um b'*' 
    após o registro de tamanho.
    '''
    try:
        offsetID = buscaID(int(id))
        if offsetID == -1:
            print("ID não existe!")
            return False
        with open("games.dat", "r+b") as arq:
            # Soma mais dois do registro de tamanho que não será necessário
            arq.seek(offsetID + 2)
            arq.write(b'*')
        chaves = criaListaOffsetChaves()
        constroiIndices(chaves)
        print("Registro removido com sucesso!")
        return True
    except OSError as e:
        print(f"Erro: {e}")
        return False
            

def compactacao() -> None:
    ''' Retira os registros começando por b'*' de games.dat. '''
    try:
        with open('games.dat', 'r+b') as games, \
            open('novo_games.dat', 'wb') as novo:
            bufferTamReg = games.read(2)
            tamReg = int.from_bytes(bufferTamReg, 'little')
            while bufferTamReg:
                primeiro = games.read(1)
                if primeiro == b'*':
                    games.seek(tamReg - 1, os.SEEK_CUR)
                else:
                    restante = games.read(tamReg - 1)
                    novo.write(bufferTamReg + primeiro + restante)
                bufferTamReg = games.read(2)
                tamReg = int.from_bytes(bufferTamReg, 'little')
        os.replace('novo_games.dat', 'games.dat')
        chaves = criaListaOffsetChaves()
        constroiIndices(chaves)
    except FileNotFoundError as e:
        print(f"Erro: {e}")


def imprimeResultado(comando: str, argumento:str, resultado: list[str]) -> None:
    tamMax:int = 0
    naoAchou = (len(resultado) == 1 and resultado[0] == '')
    if naoAchou:
        tamMax = 23 + len(argumento)
    else:
        for r in resultado:
            if len(r) > tamMax:
                tamMax = len(r)
    print('=' * tamMax )
    match comando:
        case 'bp':
            print(f"Busca pelo item de ID: {argumento}\n")
            if naoAchou:
                print("ID não encontrado!")
                print('=' * tamMax + '\n')
                return
        case 'bs1':
            print(f"Busca por itens de genero: {argumento}\n")
        case 'bs2':
            print(f"Busca por itens da publicadora: {argumento}\n")
    for item in resultado:
        print(item)
    print('=' * tamMax + '\n')


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
                    case 'bp':
                        rPrimario = buscaPrimaria(argumento)
                        imprimeResultado(comando, argumento, [rPrimario])
                    case 'bs1':
                        rSecGen = buscaSecGenero(argumento)
                        imprimeResultado(comando, argumento, rSecGen)
                    case 'bs2':
                        rSecPub = buscaSecPub(argumento)
                        imprimeResultado(comando, argumento, rSecPub)
                    case 'i':
                        s = "Insere registro: " + argumento
                        print("=" * len(s))
                        print(s + "\n")
                        insereRegistro(argumento)
                        print("=" * len(s) + "\n")
                    case 'r':
                        s = "Remove registro de ID: " + argumento
                        print("=" * 30)
                        print(s + "\n")
                        removeRegistro(argumento)
                        print("=" * 30 + "\n")
                        # Queria que os '=' ficassem do tamanho bonitinho, mas 
                        # nn tem como fazer aqui :(
                    case _:
                        print(f"Operação inválida!")
    except ValueError as e:
        print(f"Erro: {e}")
    except FileNotFoundError as e:
        print(f'Erro: {e}')

def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(f"Erro! Uso: {sys.argv[0]} <operador>")
    match sys.argv[1]:
        case '-b':
            chaves = criaListaOffsetChaves()
            constroiIndices(chaves)
        case '-e':
            if len(sys.argv) != 3:
                sys.exit(f"Erro! Uso: {sys.argv[0]} <-e> <operações>")
            else:
                realizaOperacoes(sys.argv[2])

        


if __name__ == "__main__":
    main()
