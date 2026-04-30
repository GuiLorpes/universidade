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


def criaListaInvertida(nomeArq:str) -> None:
    '''
    Cria uma lista invertida, a partir de *nomeArq*, com o ID do item atual, e 
    o ID do próximo item do mesmo gênero, e o ID do proximo item da mesma 
    publicadora 
    '''
    chaves = criaListaOffsetChaves(nomeArq)
    listaInvertida: list[tuple[int, int, int]] = []
    for c in chaves:
        listaInvertida.append((c[1], -1, -1))
    

                  
    


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
        mergesort(registro, 1)
        for offset, *_ in registro:
            reg.seek(offset, os.SEEK_SET)
            tamReg = reg.read(2)
            buffer = reg.read(int.from_bytes(tamReg,'little'))

            chavePrimaria.write(tamReg + buffer)

    # Cria arquivo com indice secundário de genero 
    with open(nomeArq, "rb") as reg, open("genero.ind", "wb") as chaveSec1:
        mergesort(registro, 2)
        for offset, *_ in registro:
            reg.seek(offset, os.SEEK_SET)
            tamReg = reg.read(2)
            buffer = reg.read(int.from_bytes(tamReg,'little'))

            chaveSec1.write(tamReg + buffer)

    # Cria arquivo com indice secundário de publicadora
    with open(nomeArq, "rb") as reg, open("publicadora.ind", "wb") as chaveSec2:
        mergesort(registro, 3)
        for offset, *_ in registro:
            reg.seek(offset, os.SEEK_SET)
            tamReg = reg.read(2)
            buffer = reg.read(int.from_bytes(tamReg,'little'))

            chaveSec2.write(tamReg + buffer)
            

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
        organizaRegistros(sys.argv[1], chaves)


if __name__ == "__main__":
    main()
