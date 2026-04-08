import os

arq = open('teste_bytes.txt', 'w+b')
texto = 'Uau olha so que legal'
arq.write(texto.encode())
arq.seek(0)
print(arq.read())

arq.seek(16, os.SEEK_SET)
texto = 'bosta'
arq.write(texto.encode())

arq.seek(0)
print(arq.read(-1))
arq.close()

