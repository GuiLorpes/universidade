import os
import io
from dataclasses import dataclass

class Memoria:
    ''' Memoria com ou o opcode e endereço, ou o valor do dado '''
    memoria: list[tuple[tuple[int, int|None], tuple[int, int|None] | None]]

    def __init__(self):
        self.memoria = [None] * 256

class BancoRegistradores:
    ''' Registradores que vão ter as informações '''
    AC: int;
    MQ: int
    PC: int
    MBR: int
    IR: int
    MAR: int
    IBR: int

    def __init__(self):
        self.AC = 0
        self.MQ = 0
        self.PC = 0
        self.MBR = 0
        self.IR = 0
        self.MAR = 0
        self.IBR = 0

'''
leArquivoColocaNaMemoria(nomeArq:str, m: Memoria):
    verifica se o arquivo existe
        se existir abre o arquivo
            le uma linha inteira 
            verificar se tem "#" na entrada
            {
            entrada = readlines(1)
            if "#" in entrada:
            }
            se a entrada tiver uma "#", verificar se é uma linha só de comentário
            {
            if "#" in entrada:
                buffer = entrada.split("#")
                if buffer[0]: 
                    continue
                else:
                    entrada = buffer[0]
            }
            se a linha tiver informações alem do comentário, buffer[0] será 
            diferente de vazio e será colocado na entrada, caso contrario, só ]
            pula pra próxima linha 
'''

def leArquivoColocaNaMemoria(nomeArq:str, m: Memoria):
    try:
        with open(nomeArq, 'r') as arq:
            entrada = arq.readline()
            dado: int
            informacoes: list[tuple[int, int|None]] = [None] * 2
            infoQtd = 0
            while entrada:
                info = ''
                if "#" in entrada:
                    buffer = entrada.split("#")
                    if buffer[0]:
                        info = buffer[0]
                    else:
                        entrada = arq.readline()
                        continue
                else:
                    info = entrada
                if info.isdigit():
                    dado = int(info)
                    i = 0
                    while i < 160: # Primeira instrução é sempre o endereço 160
                        if m.memoria[i] is not None: # se já tiver algum dado no m[i] pula ele
                            i += 1
                    if i < 160 and m.memoria[i] is None:
                        m.memoria[i] = tuple[tuple[dado, None], None]

                    else: 
                        print("Memória para dados cheia")



    except FileNotFoundError as e:
        print(f"Erro: {e}")
def main() -> None:
    dasdsa

if __name__ == "__main__":
    main()