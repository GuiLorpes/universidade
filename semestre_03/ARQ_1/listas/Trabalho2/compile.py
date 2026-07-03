from os import getcwd
import subprocess

DIR_ATUAL = getcwd()
DIR_ALGORITMOS = f'{DIR_ATUAL}/Algoritmos'

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

for alg in ALGORITMOS:
    for tcomp in TIPO_COMPILACAO:
        for tam in TAMANHO_ENTRADA:
            subprocess.run([
                'gcc',
                f'{DIR_ALGORITMOS}/{alg}/{alg}.c',
                '-static',
                '-DPOLYBENCH_TIME',
                f'-O{tcomp}',
                f'-D{tam.upper()}_DATASET',
                '-I',
                f'{DIR_ALGORITMOS}',
                f'{DIR_ALGORITMOS}/polybench.c',
                '-o',
                f'{DIR_ALGORITMOS}/{alg}/{alg}_{tcomp}_{tam}',
                '-lm'
            ])