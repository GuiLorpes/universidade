arq = open('teste_aula.txt', 'w+')
print(arq.readline(20))

texto: str = "Querido Kyle: você tem uma bunda tão boa. Eu poderia dormir por \
dias naquelas bochechas empinadas, deixa eu te falar. Eu queria morar com você \
e usar sua bunda como um chapéu por toda a eternidade"


arq.write(texto)
arq.close()

arq = open('teste_aula.txt', 'r')
print(arq.read(-1))
