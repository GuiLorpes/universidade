# Código para a leitura de um arquivo já existente
nomeArq = str(input("Insira o nome do seu arquivo: "))
try:
    with open(nomeArq, 'r') as arq:
        c = arq.read(1)
        while c:
            print(c)
            c = arq.read(1)
except:
    print(f"Não foi possivel encontrar o arquivo {nomeArq}!")
finally:
    print("Operação encerrada")
