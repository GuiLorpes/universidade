import sys


# Exercicio 1
def escreveTxt(texto: str) -> None:
    with open("exercicios.txt", 'a') as arq:
        arq.write(texto + "\n")


# Exercicio 2
def arqTam_bytes_e_linhas(nomeArq: str) -> None:
    try:
        with open(nomeArq, 'rb') as arq:
            buffer = arq.read(-1)
            tamanhoBytes = len(buffer)
        with open(nomeArq, 'r') as arq:
            linhas = len(arq.readlines(-1))
            
        print(f"O arquivo '{nomeArq}' possui um tamanho de {tamanhoBytes} "\
        "bytes")
        print(f"O arquivo '{nomeArq}' possui {linhas} linhas")
    except FileNotFoundError as e:
        print(f"Erro: {e}")


# Exercicio 3
def removeEspacosExtra(nomeArq: str) -> None:
    try:
        arqVelho = open(nomeArq, 'r')
        arqNovo = open('NOVO' + nomeArq, 'w')
        c = arqVelho.read(1)
        while c:
            if c == ' ':
                prox = arqVelho.read(1)
                while prox == ' ':
                    prox = arqVelho.read(1)
                arqNovo.write(c)
                arqNovo.write(prox)
            else:
                arqNovo.write(c)
        arqVelho.close()
        arqNovo.close()
                       
    except FileNotFoundError as e:
        print(f"Erro: {e}")


# Exercicio 4
def lePython(arqPython: str) -> None:
    try:
        buffer = ''
        nomeTxt = 'fodase.txt'
        # nomeTxt = arqPython[:-2] + 'txt'
        with open(arqPython, 'r') as arqPy:
            c = arqPy.read(1)
            while c:
                if c == '#':
                    while c != '\n':
                        c = arqPy.read(1)
                    if c == '\n':
                        buffer += c
                        c = arqPy.read(1)
                else:
                    buffer += c
                    c = arqPy.read(1)
        with open(nomeTxt, 'w') as arqTxt:
            arqTxt.write(buffer)
        print(f"Arquivo {arqPython} copiado para o arquivo {nomeTxt}")
    except FileNotFoundError as e:
        print(f"Erro: {e}")


# Exercicio 5
def quebraLinux(nomeArq: str) -> None:
    ''' 
    Transforma um arquivo de texto do Windows com a quebra '\r''\n', para a 
    quebra do Linux '\n'    
    '''
    try:
        with open(nomeArq, 'rb') as arq:
            arqNovo = open('LINUX' + nomeArq, 'wb')
            c = arq.read(1)
            while c:
                if c == b'\r': 
                    prox = arq.read(1)
                    if prox == b'\n':
                        arqNovo.write(b'\n')
                    else:
                        arqNovo.write(c)
                        arqNovo.write(prox)
                else:
                    arqNovo.write(c)
                c = arq.read(1)
        print(f"Arquivo novo: LINUX{nomeArq}")

    except FileNotFoundError as e:
        print(f'Erro: {e}')


def quebraWindows(nomeArq: str) -> None:
    ''' 
    Transforma um arquivo de texto do Linux com a quebra '\n', para a quebra do 
    Windows '\r''\n' 
    '''
    try:
        with open(nomeArq, 'rb') as arq:
            arqNovo = open('WIN' + nomeArq, 'wb')
            c = arq.read(1)
            while c:
                if c == b'\n':
                    arqNovo.write(b'\r')
                    arqNovo.write(b'\n')
                else:
                    arqNovo.write(c)
                c = arq.read(1)
        print(f"Arquivo novo: WIN{nomeArq}")

    except FileNotFoundError as e:
        print(f'Erro: {e}')


# Exercicio 6
def escreveNumsBytes(numeros: list[int]):
    try:
        with open('numeros.dat', 'wb') as arq:
            for n in numeros:
                num = n.to_bytes(4, 'little')
                arq.write(num)            
    except OSError as e:
        print(f"Erro: {e}")


# Exercicio 7
def leNumBytes(nomeArq: str):
    try:
        with open(nomeArq, 'rb') as arq:
            numeros: list[int] = []
            for _ in range(10):
                num = arq.read(4)
                numeros.append(int.from_bytes(num, 'little'))
            print(numeros)
    except FileNotFoundError as e:
        print(f"Erro; {e}")


# Exercicio 8
def escreveStrings(palavras: list[str]) -> None:
    try:
        with open('palavras.txt', 'wb') as arq:
            for p in palavras:
                tamPalavra = len(p).to_bytes(2, 'little')
                arq.write(tamPalavra)
                arq.write(p.encode())
    except OSError as e:
        print(f"Erro; {e}")


# Exercicio 9
def leStrings() -> None:
    try:
        with open('palavras.txt', 'rb') as arq:
            tamPalavra = int.from_bytes(arq.read(2), 'little')
            while tamPalavra > 0:
                palavra = arq.read(tamPalavra)
                print(palavra.decode())
                tamPalavra = int.from_bytes(arq.read(2), 'little')

    except FileNotFoundError as e:
        print(f"Erro: {e}")


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(f"Uso: {sys.argv[0]} <exercicio>")

    arguments = sys.argv[1:];
    
    match arguments[0]:
        case '1':
            # Exercicio 1
            if len(sys.argv) != 2:
                sys.exit(f"Uso: {sys.argv[0]} <exercicio>")
            texto = input("Digite seu texto para ser inserido no arquivo "\
                        "'exercicios.txt'\n")
            escreveTxt(texto)

        case '2':
            # Exercicio 2
            if len(sys.argv) != 2:
                sys.exit(f"Uso: {sys.argv[0]} <exercicio>")
            nomeArq = input("Digite o nome do seu arquivo para verificar o "
                            "tamanho em bytes e a quantia de linhas\n")
            arqTam_bytes_e_linhas(nomeArq)
            
        case '3':
            # Exercicio 3
            if len(sys.argv) != 2:
                sys.exit(f"Uso: {sys.argv[0]} <exercicio>")
            nomeArq = input("Digite o nome do seu arquivo para remover os "
                            "espaços extras\n")
            removeEspacosExtra(nomeArq)
            
        case '4':
            # Exercicio 4
            if len(sys.argv) != 2:
                sys.exit(f"Uso: {sys.argv[0]} <exercicio>")
            arqPython = input("Insira o nome do arquivo python que deseja " \
                                "tranformar em txt:\n")
            lePython(arqPython)
            
        case '5':
            # Exercicio 5
            if len(sys.argv) != 4:
                sys.exit(f"Uso: {sys.argv[0]} <exercicio> <arquivo> <-w ou -l>")
            else:
                if sys.argv[3] == '-w':
                    quebraWindows(sys.argv[2])
                elif sys.argv[3] == '-l':
                    quebraLinux(sys.argv[2])
                else:
                    sys.exit(f"Uso: {sys.argv[0]} <exercicio> <arquivo> " \
                                "<-w ou -l>")
            
        case '6':
            # Exercicio 6
            if len(sys.argv) != 2:
                sys.exit(f"Uso: {sys.argv[0]} <exercicio>")
            numeros: list[int] = []
            print(f"Insira os 10 números:")
            for _ in range(10):
                numeros.append(int(input()))
            escreveNumsBytes(numeros)
            
        case '7':
            # Exercicio 7
            if len(sys.argv) != 2:
                sys.exit(f"Uso: {sys.argv[0]} <exercicio>")
            leNumBytes('numeros.dat')
            
        case '8':
            # Exercicio 8
            if len(sys.argv) != 2:
                sys.exit(f"Uso: {sys.argv[0]} <exercicio>")
            frase = input("Insira a sua frase:\n")
            palavras = frase.split(' ')
            escreveStrings(palavras)

        case '9':
            # Exercicio 9
            if len(sys.argv) != 2:
                sys.exit(f"Uso: {sys.argv[0]} <exercicio>")
            leStrings()

        case _:
            print("Valor inválido")

if __name__ == "__main__":
    main()
