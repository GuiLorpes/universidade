import os
import io

def escreve_registros(nomeArq: str) -> None:
    try:
        with open(nomeArq, 'wb') as saida:
            campo = str(input("INSIRA O SOBRENOME OU PRESSIONE <ENTER> PARA \
SAIR\n"))
            while campo: 
                buffer = ''
                buffer += campo + '|'
                nome = str(input('QUAL SEU NOME?\n'))
                endereco = str(input('QUAL O SEU ENDEREÇO?\n'))
                cidade = str(input('QUAL A SUA CIDADE?\n'))
                estado = str(input('QUAL O SEU ESTADO?\n'))
                cep = str(input('QUAL O SEU CEP?\n'))
                infos = [nome, endereco, cidade, estado, cep]
                for i in infos:
                    campo = i
                    buffer += campo + '|'
                buffbit = buffer.encode()
                tam = len(buffbit)
                tambit = tam.to_bytes(2, 'little')
                saida.write(tambit)
                saida.write(buffbit)
                campo = str(input("INSIRA O SOBRENOME OU PRESSIONE <ENTER> PARA \
SAIR\n"))

    except OSError as e:
        print(f'ERRO escreve_registros: {e}')
    finally:
        print('PROGRAMA FINALIZADO')

def le_registros(nomeArq: str) -> None:
    try:
        with open(nomeArq, 'rb') as entrada:
            buffer = leia_reg(entrada)
            i = 1
            while buffer:
                campos = buffer.split('|')
                j = 1
                for c in campos:
                    if c:
                        print(f'Campo {j}: {c}')
                        j += 1
                i += 1
                buffer = leia_reg(entrada)
            print("Leitura finalizada!")
    except FileNotFoundError as e:
        print(f'ERRO le_registros: {e}')
    finally:
        print('PROGRAMA FINALIZADO')


def leia_reg(arq: io.BufferedReader) -> str:
    tambytes = arq.read(2)
    if not tambytes:  # Verifica se chegou ao final do arquivo
        return ''
    tam = int.from_bytes(tambytes, 'little')
    if tam > 0:
        print(tam)
        buffer = arq.read(tam)
        return buffer.decode()
    return ''


def main() -> None:
    nomeArq = str(input('QUAL O NOME DO SEU ARQUIVO?\n'))
    print('QUE OPERAÇÃO DESEJA REALIZAR?\n')
    c = 0
    while c < 3:    
        c = int(input('1 -> ESCREVER NO ARQUIVO\n2 -> LER O ARQUIVO\n3 -> SAIR\n'))
        if c == 1:
            escreve_registros(nomeArq)
        if c == 2:
            le_registros(nomeArq)
    print('ATÉ A PRÓXIMA\n')
if __name__ == '__main__':
    main()
