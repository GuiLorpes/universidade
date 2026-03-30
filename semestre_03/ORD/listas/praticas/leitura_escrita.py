# Código para a leitura de um arquivo já existente.

def leitura(nome_arq: str) -> None:
    try:
        with open(nome_arq, 'r') as arq:
            c = arq.read(-1)
            print(c)
    except:
        print(f"Não foi possivel encontrar o arquivo {nome_arq}!")

# Código para a escrita de um arquivo já existente, ou de um arquivo a ser criado.

def escrita(nome_arq: str, texto: str) -> None:
    with open(nome_arq,'w+') as arq:
        arq.write(texto)

# Main :)

def __main__() -> None:
    print("Bem-vindo ao leitor/escritor de arquivos!")
    nome_arq = str(input("Insira o nome do seu arquivo: "))
    c = 0
    while c != 3 and c < 4:
        print("Qual operação você deseja realizar?")
        print("1 - Leitura; 2 - Escrita 3- Sair")
        c = int(input())
        if c == 1:
            leitura(nome_arq)
        if c == 2:
            texto = str(input("O que você deseja escrever no seu arquivo?\n"))
            escrita(nome_arq, texto)
    return None

if __name__ == "__main__":
    __main__()
