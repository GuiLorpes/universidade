import io

def buscaID() -> None:
    try:
        with open('pessoasGOT.dat', 'rb') as arq:
            chave = input("Insira o ID a ser buscado: ")
            achou = False
            reg = leia_reg(arq)
            while reg and not achou:
                id = reg.split(sep='|')[0]
                if id == chave:
                    achou = True
                else:
                    reg = leia_reg(arq)
            if achou:
                campos = reg.split('|')
                i = 1
                for c in campos:
                    if c:
                        print(f'Campo {i}: {c}')
                    i += 1
            else:
                print('ID não encontrado!')
    except OSError as e:
        print(f'Erro: {e}')

def leia_reg(arq: io.BufferedReader) -> str:
    tambytes = arq.read(2)
    tam = int.from_bytes(tambytes, 'little')
    if tam > 0:
        buffer = arq.read(tam)
        return buffer.decode()
    return ''



def buscaSobrenome() -> None:
    try:
        with open('pessoasGOT.dat', 'rb') as arq:
            sobrenome = input("Insira o sobrenome a ser buscado: ")
            achou = False
            reg = leia_reg(arq)
            while reg:
                id = reg.split(sep='|')[1]
                if id == sobrenome:
                    achou = True
                    campos = reg.split('|')
                    i = 1
                    for c in campos:
                        if c:
                            print(f'Campo {i}: {c}')
                        i += 1
                    print()
                reg = leia_reg(arq)
            if not achou:
                print('Sobrenome não encontrado!')
        print()
    except OSError as e:
        print(f'Erro: {e}')

def main() -> None:
    print('Deseja realizar sua procura por:')
    print('1 - ID  |  2 - Sobrenome  |  0 - Sair')
    case = int(input())
    while case != 0 and case < 3:
        if case == 1:
             buscaID()
        if case == 2:
            buscaSobrenome()
        print('Deseja realizar sua procura por')
        print('1 - ID  |  2 - Sobrenome  |  0 - Sair')
        case = int(input())
    print('Adeus!')

if __name__ == '__main__':
    main()