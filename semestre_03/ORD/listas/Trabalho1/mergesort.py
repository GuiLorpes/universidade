import os
import io
import sys


def mergesort(registros: list[list[str]], chave: int) -> None:
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
    
def organizaRegistros(nomeArq: str) -> None:
    ''' 
    Cria um arquivo a partir de *nomeArq* com registros de tamanho variado 
    ordenado pelo RRN, e o ordena de acordo com as chaves pedidas
    '''

    try:
        # Cria a lista com os registros para ordenar depois
        registros: list[list[str]] = []
        # Abre o arquivo como original para pegar todos os registros
        with open(nomeArq, 'rb') as original: 
            tamRegistro = int.from_bytes(original.read(2), 'little') 
            while tamRegistro > 0:
                # Cria a lista do registro iniciado com o tamanho dele 
                registro = [str(tamRegistro)]

                buffer = original.read(tamRegistro)

                # Adiciona os campos restantes na lista do registro
                registro += (buffer.decode()).split('|')

                # Adiciona o registro na lista com os outros registros
                registros.append(registro)
                tamRegistro = int.from_bytes(original.read(2), 'little') 

        # Ordena o registro usando a chave primaria 
        # Escreve em um novo arquivo
        with open("primario.ind", "wb") as chavePrimaria:
            mergesort(registros, 1)
            for r in registros:
                campos = ''
                tam = int(r[0])
                chavePrimaria.write(tam.to_bytes(2,'little'))
                for campo in r[1:-1]:
                    campos += campo + '|'
                buffer = campos.encode()
                chavePrimaria.write(buffer)

        # Ordena o registro ussando a chave secundaria 1 
        # Escreve em um novo arquivo
        with open("genero.ind", "wb") as chaveSec1:
            mergesort(registros, 4)
            for r in registros:
                campos = ''
                tam = int(r[0])
                chaveSec1.write(tam.to_bytes(2,'little'))
                for campo in r[1:-1]:
                    campos += campo + '|'
                buffer = campos.encode()
                chaveSec1.write(buffer)

        # Ordena o registro ussando a chave secundaria 2 
        # Escreve em um novo arquivo
        with open("publicadora.ind", "wb") as chaveSec2:
            mergesort(registros, 5)
            for r in registros:
                campos = ''
                tam = int(r[0])
                chaveSec2.write(tam.to_bytes(2,'little'))
                for campo in r[1:-1]:
                    campos += campo + '|'
                buffer = campos.encode()
                chaveSec2.write(buffer)

    except FileNotFoundError as e:
        print(f"Erro: {e}")


def main() -> None:
    if len(sys.argv) > 2:
        sys.exit(f"Erro! Uso: {sys.argv[0]} <nome_do_arquivo>")
    if not os.path.isfile(sys.argv[1]):
        raise FileNotFoundError('Insira um arquivo válido')
    else:
        organizaRegistros(sys.argv[1])


if __name__ == "__main__":
    main()