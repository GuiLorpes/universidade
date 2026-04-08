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
        print(f'ERRO escreve_campos: {e}\n')
    finally:
        print("PROGRAMA FINALIZADO\n")

# Programa 2

def le_campos(nomeArq: str) -> None:
    try:
        with open(nomeArq, 'r') as entrada:
            campos = ['SOBRENOME', 'NOME', 'ENDEREÇO', 'CIDADE', 
                      'ESTADO', 'CEP']
            campo = leia_campo(entrada)
            i = 0
            while campo != '':
                print(f'{campos[i]}: {campo}')
                i += 1
                campo = leia_campo(entrada)
    except FileNotFoundError as e:
        print(f'ERRO le_campos: {e}\n')
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
    programa = 0
    while programa < 3:    
        programa = int(input('1 -> ESCREVER NO ARQUIVO\n2 -> LER O ARQUIVO\n3 -> SAIR\n'))
        if programa == 1:
            escreve_campos(nomeArq)
        if programa == 2:
            le_campos(nomeArq)
    print('ATÉ A PRÓXIMA\n')
if __name__ == '__main__':
    main()