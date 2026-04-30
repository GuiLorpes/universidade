import os
import io
import sys


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


def criaListaInvertida(chaves: list[tuple[int,int,str,str]]) -> list[list[int]]:
    '''
    Cria uma lista invertida, a partir de *nomeArq*, com o ID do item atual, e 
    o ID do próximo item do mesmo gênero, e o ID do proximo item da mesma 
    publicadora 
    '''
    listaInvertida: list[list[int]] = []
    for c in chaves:
        listaInvertida.append([c[1], -1, -1])
    i = 0   # Indice para a lista invertida
    j = i+1   # Indice para as chaves

    # Procura o próximo do gênero
    while i < len(listaInvertida):
        achou = False
        while j < len(chaves) and not achou:
            achou = chaves[i][2] == chaves[j][2]
            if achou:
                listaInvertida[i][1] = j
            j += 1
        if not achou:
            listaInvertida[i][1] = -1
        i += 1
        j = i + 1
    
    i = 0
    j = i + 1
    # Procura o proximo da publicadora
    while i < len(listaInvertida):
        achou = False
        while j < len(chaves) and not achou:
            achou = chaves[i][3] == chaves[j][3]
            if achou:
                listaInvertida[i][2] = j
            j += 1
        if not achou:
            listaInvertida[i][2] = -1
        i += 1
        j = i + 1

    return listaInvertida


def organizaRegistros(nomeArq: str, registro: list[tuple[int,int,str,str]]) \
    -> None:
    '''
    Com base no *nomeArq* cria 4 arquivos novos, primario.ind, genero.ind, 
    publicadora.ind e listaInvertida.lst, onde cada um dos .ind são ordenados 
    de acordo com as chaves primária, secundária de gênero e secundária de 
    publicadora. 
    Os *registros* estarão com o offset de cada um dos elementos, e serão 
    ordenadas de acordo com cada uma das chaves e serão escritos em seus 
    respectivos arquivos
    '''

    # Cria arquivo com indice primário
    with open(nomeArq, "rb") as reg, open("primario.ind", "wb") as chavePrimaria:
        indices: list[str] = []
        mergesort(registro, 1)
        for offset, *_ in registro:
            reg.seek(offset, os.SEEK_SET)
            tamReg = reg.read(2)
            buffer = reg.read(int.from_bytes(tamReg,'little'))

            chavePrimaria.write(tamReg + buffer)

    # Cria arquivo com indice secundário de genero 
    with open("genero.ind", "wb") as chaveSec1:
        generos:list[str] = []
        mergesort(registro, 2)
        for r in registro:
            i = 0
            achou = False
            while i < len(generos) and not achou:
                achou = r[2] == generos[i]
                if not achou:
                    i += 1
            if not achou:
                generos.append(r[2])
        print(generos)
            
    # Cria arquivo com indice secundário de publicadora
    with open("publicadora.ind", "wb") as chaveSec2:
        publicadora: list[str] = []
        mergesort(registro, 3)
        for r in registro:
            i = 0
            achou = False
            while i < len(publicadora) and not achou:
                achou = r[3] == publicadora[i]
                if not achou:
                    i += 1
            if not achou:
                publicadora.append(r[3])
        print(publicadora)
            

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
    

def main() -> None:
    if len(sys.argv) > 2:
        sys.exit(f"Erro! Uso: {sys.argv[0]} <nome_do_arquivo>")
    if not os.path.isfile(sys.argv[1]):
        raise FileNotFoundError('Insira um arquivo válido')
    else:
        chaves = criaListaOffsetChaves(sys.argv[1])
        print(chaves)
        print(criaListaInvertida(chaves))
        organizaRegistros(sys.argv[1], chaves)


if __name__ == "__main__":
    main()
