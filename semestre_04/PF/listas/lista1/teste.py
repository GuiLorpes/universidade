lista: list[int] = [4, 6, 1, 7]

def soma_indices_impares(n: int) -> int:
    
    soma = 0
    if n % 2 == 0:
        lista.pop()
        lista.append(n)
        for i in lista:
            soma += i
        return soma
    else:
        lista.append(2 * n)
        if n <= len(lista):
            lista.pop(n)
        for i in lista:
            soma += i
        return soma

print(soma_indices_impares(1) + soma_indices_impares(2))
print(soma_indices_impares(2) + soma_indices_impares(1))