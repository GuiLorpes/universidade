from __future__ import annotations
from dataclasses import dataclass
import io
import os

class Pagina:
    numChaves: int
    chaves: list[int | None] | None
    filhas: list[Pagina | None] | None

    def __init__(self, ordem: int):
        self.numChaves = 0
        self.chaves = None
        self.filhas = None

    def buscaElemento(self, elemento: int) -> bool:
        '''
        Percorre *self* até encontrar o *elemento*, caso não encontra nessa 
        página, verifica na página filha da esquerda ou na filha da direita
        '''
        if self.chaves is None:
            return False
        i = 0
        while i < len(self.chaves) and self.chaves[i] is not None and \
            elemento > self.chaves[i]:
            i += 1
        if self.chaves[i] is None: 
            return False
        elif elemento == self.chaves[i]: 
            return True
        elif elemento < self.chaves[i]: 
            return self.filhas[i].buscaElemento(elemento)
        elif i == len(self.chaves): 
            return self.filhas[i+1].buscaElemento(elemento)
        return False

    def insereElemento(self, i: int) -> None:
        '''
        
        '''