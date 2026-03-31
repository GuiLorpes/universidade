import os
import io

# Programa 1

def escreve_campos(nomeArq: str) -> None:
    try:
        with open(nomeArq, 'w') as saida:
            sobrenome = str(input("INSIRA O SOBRENOME OU PRESSIONE <ENTER> PARA \
SAIR\n"))
            while sobrenome != '':
                nome = str(input('QUAL SEU NOME?\n'))
                endereco = str(input('QUAL O SEU ENDEREÇO?\n'))
                cidade = str(input('QUAL A SUA CIDADE?\n'))
                estado = str(input('QUAL O SEU ESTADO?\n'))
                cep = str(input('QUAL O SEU CEP?\n'))
                infos = [sobrenome, nome, endereco, cidade, estado, cep]
                for i in infos:
                    saida.write(i)
                    saida.write('|')
                sobrenome = str(input("INSIRA O SOBRENOME OU PRESSIONE <ENTER> \
PARA SAIR\n"))
    except OSError as e:
        print(f'ERRO MAIN: {e}\n')
    finally:
        print("PROGRAMA FINALIZADO\n")

def le_campos(nomeArq: str) -> None:
    try:
        with open(nomeArq, 'r') as entrada:
            campo = leia_campo(entrada)
            i = 1
            while campo != '':
                print(f'CAMPO {i}: {campo}')
                i += 1
                campo = leia_campo(entrada)
    except FileNotFoundError as e:
        print(f'ERRO MAIN: {e}\n')
    finally:
        print('PROGRAMA FINALIZADO\n')

def leia_campo(arq: io.TextIOWrapper) -> str:
    campo:str = ''
    try:
        c = arq.read(1)
        while c and c != '|':
            campo += c
            c = arq.read(1)
        return campo
    except OSError as e:
        print(f'ERRO leia_campo: {e}\n')
        return ''

def main() -> None:
    nomeArq = str(input('QUAL O NOME DO SEU ARQUIVO?\n'))
    print('QUE OPERAÇÃO DESEJA REALIZAR?\n')
    c = 0
    while c < 3:    
        c = int(input('1 -> ESCREVER NO ARQUIVO\n2 -> LER O ARQUIVO\n3 -> SAIR\n'))
        if c == 1:
            escreve_campos(nomeArq)
        if c == 2:
            le_campos(nomeArq)
    print('ATÉ A PRÓXIMA\n')
if __name__ == '__main__':
    main()