import os

arq = open('teste_bytes.txt', 'w+b')
texto = 'Uau olha só que legal'
arq.write(texto.encode())
print(arq.read())
arq.seek(16, os.SEEK_SET)
texto = ' bosta'
arq.write(texto.encode())
print(arq.read(-1))
arq.close()

