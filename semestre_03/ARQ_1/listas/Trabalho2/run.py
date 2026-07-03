from os import getcwd
import subprocess

DIR_ATUAL = getcwd()
DIR_SAIDA = f'{DIR_ATUAL}/Resultados'
DIR_ALGORITMOS = f'{DIR_ATUAL}/Algoritmos'

CONFIG = f'{DIR_ATUAL}/config.py'
GEM_5 = '/home/guilorpes/faculdade/semestre_03/ARQ_1/listas/Trabalho2/gem5/build/X86/gem5.fast'

NOME_ARQUIVO_DADOS = 'dados.txt'

ALGORITMOS = [
    '3mm',
    'heat-3d',
    'fdtd-2d'
]

TAMANHO_ENTRADA = [
    'mini',
    'small'
]

TIPO_COMPILACAO = [
    '0',
    '3'
]

POLITICAS_SUBS = [
    'WEIGHTED_LRU',
    'FIFO',
    'LFU',
    'LRU',
    'MRU',
    'RANDOM'
]

# Apaga arquivo de dados extraidos (se existir) e cria novamente
subprocess.run([
    'rm',
    f'{DIR_SAIDA}/{NOME_ARQUIVO_DADOS}'
])

dados = open(f'{DIR_SAIDA}/{NOME_ARQUIVO_DADOS}', 'a')

# Executa GEM5 para cada configuração
for alg in ALGORITMOS:
    for tcomp in TIPO_COMPILACAO:
        for tam in TAMANHO_ENTRADA:
            for ps in POLITICAS_SUBS:
                nome_arq = f'{alg}_{tcomp}_{tam}_{ps}'
                subprocess.run([
                    GEM_5,
                    '-d',
                    f'{DIR_SAIDA}/{alg}/{nome_arq}',
                    CONFIG,
                    f'--binary={DIR_ALGORITMOS}/{alg}/{alg}_{tcomp}_{tam}',
                    f'--replacement_policy={ps}'
                ])

                
                # Extrai Dados
                hits = 0
                misses = 0
                segundos = 0.0
                with open(f'{DIR_SAIDA}/{alg}/{nome_arq}/stats.txt') as relatorio:
                    for num, linha in enumerate(relatorio, start=1):
                        if num == 6:
                            buffer = linha.split()
                            segundos = float(buffer[1])
                        elif num == 229:
                            buffer = linha.split()
                            hits = int(buffer[1])
                        elif num == 233:
                            buffer = linha.split()
                            misses = int(buffer[1])

                dados.write(f'{nome_arq.upper():<30} \n\
tempo de exec:{segundos:>4.4f}  hits:{hits:>8}  misses:{misses:>8}  media hits:{hits/(hits+misses):>8.4f}\n')
    dados.write('\n')

dados.close()