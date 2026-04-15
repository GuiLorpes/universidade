import io
import os

FILE_NAME = 'pessoasGOTfixo.dat'
SIZE_OF_REG = 64
SIZE_OF_CAB = 4
    
def edita_campos(nomeArq: str, rrn: int) -> None:
    try:
        with open(nomeArq, 'r+b') as arq:
            buffer = ''
            cab = arq.read(SIZE_OF_CAB)
            total_reg = int.from_bytes(cab, 'little')
            campos = ['ID', 'Sobrenome', 'Nome', 'Castelo', 'Cidade', 
                        'Região']
            
            for c in campos:
                s = input(f'{c}: ')
                if c == 'ID':
                    i = 1
                    achou = False
                    while i <= total_reg and not achou:
                        offset = i * SIZE_OF_REG + SIZE_OF_CAB
                        arq.seek(offset, os.SEEK_SET)
                        aux = arq.read(SIZE_OF_REG).decode()
                        auxlista = aux.split('|')
                        if s == str(auxlista[0]):
                            if i == rrn:
                                achou = True
                            else:    
                                achou = True
                                print('ID já existe!')
                                s = input('Insira outro ID\n')
                        else:
                            i += 1
                buffer += (s + '|')
            registro = buffer.encode()
            offset = rrn * SIZE_OF_REG + SIZE_OF_CAB
            arq.seek(0, os.SEEK_SET)
            arq.seek(offset, os.SEEK_SET)
            arq.write(registro.ljust(64, b'\0'))

    except FileNotFoundError as e:
        print(f'Erro: {e}')

def escreve_campos(arq: io.BufferedRandom) -> str:
    buffer = ''
    cab = arq.read(SIZE_OF_CAB)
    total_reg = int.from_bytes(cab, 'little')
    campos = ['ID', 'Sobrenome', 'Nome', 'Castelo', 'Cidade', 
                'Região']
    
    for c in campos:
        s = input(f'{c}: ')
        if c == 'ID':
            i = 1
            achou = False
            while i <= total_reg and not achou:
                offset = i * SIZE_OF_REG + SIZE_OF_CAB
                arq.seek(offset, os.SEEK_SET)
                aux = arq.read(SIZE_OF_REG).decode()
                auxlista = aux.split('|')
                if s == str(auxlista[0]):
                    achou = True
                    print('ID já existe!')
                    s = input('Insira outro ID\n')
                else:
                    i += 1
        buffer += (s + '|')
    return buffer

def escreve_arq(nomeArq: str) -> None:
    try:
        if not os.path.isfile(nomeArq):
            with open(nomeArq, 'r+b') as arq:
                total_reg = 0
                cab = total_reg.to_bytes(4, 'little')
                arq.write(cab)
                escreve_arq(nomeArq)
        else:
            with open(nomeArq, 'r+b') as arq:
                # Escreve os campos
                campos = escreve_campos(arq).encode()

                # Encontra o numero de registros
                arq.seek(0, os.SEEK_SET)
                cab = arq.read(SIZE_OF_CAB)
                total_reg = int.from_bytes(cab, 'little')

                # Faz o offset com esse numero de registros
                offset = total_reg * SIZE_OF_REG + SIZE_OF_CAB
                arq.seek(0, os.SEEK_SET)

                # Encontra a posição que deve inserir o novo registro e o insere
                arq.seek(offset, os.SEEK_SET)
                arq.write(campos.ljust(64, b'\0'))

                # Atualiza o numero de registros
                total_reg += 1         
                arq.seek(0, os.SEEK_SET)    
                cab = total_reg.to_bytes(4, 'little')
                arq.write(cab)
                
    except OSError as e:
        print(f'Erro: {e}')


def busca_rrn(nomeArq: str) -> None:
    try:
        with open(nomeArq, 'rb') as arq:
            cab = arq.read(SIZE_OF_CAB)
            total_reg = int.from_bytes(cab, 'little')
            print(f'Insira o RRN a ser procurado: ')
            rrn = int(input())
            if rrn >= total_reg:
                raise ValueError('RRN inválido')
            offset = rrn * SIZE_OF_REG + SIZE_OF_CAB
            arq.seek(offset, os.SEEK_SET)
            buffer = arq.read(SIZE_OF_REG)
            campos = buffer.decode()
            i = 1
            for c in campos.split('|')[:-1]:
                if c:
                    print(f'Campo {i}: {c}')
                i += 1
            print()
            print('Deseja modificar as informações deste registro?')
            case = int(input('1 - Sim | 2 Não\n'))
            if case == 1:
                edita_campos(nomeArq, rrn)
            else:
                return None
    except FileNotFoundError as e:
        print(f'Erro: {e}')



def main() -> None:
    nomeArq = input('Insira o nome do arquivo que deseja acessar: \n')
    print('Que ação deseja realizar?')
    print('1 - Escrever no arquivo  |  2 - Procurar no arquivo  |  3 - Quantia \
de registros | 0 - Sair')
    case = int(input())
    while case != 0 and case < 4:
        if case == 1:
            print(f'Escreve um novo registro em {nomeArq}')
            escreve_arq(nomeArq)
        if case == 2:
            print(f'Procure por um registro')
            busca_rrn(nomeArq)
        if case == 3:
            arq = open(nomeArq, 'rb')
            cab = arq.read(SIZE_OF_CAB)
            registros = int.from_bytes(cab, 'little')
            print(f'Você possui {registros} registros')
            arq.close()
            
        print('Que ação deseja realizar?')
        print('1 - Escrever no arquivo  |  2 - Procurar no arquivo  |  3 - Quantia \
de registros | 0 - Sair')
        case = int(input())
    print('Adeus!\n')
    

if __name__ == '__main__':
    main()
