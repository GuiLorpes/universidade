import os
import io
import sys


def insereRegistro(registro: str) -> None:
    try:
        # Verifica se encontra um id igual
        with open("games.dat", "rb") as entrada:
            campos = registro.split('|')
            tamReg = int.from_bytes(entrada.read(2), 'little')
            achou = False
            while tamReg > 0 and not achou:
                registro = entrada.read(tamReg).decode()
                id = (registro.split('|'))[0]
                achou = campos[0] == id
                tamReg = int.from_bytes(entrada.read(2), 'little')
            # Se encontrou, não insere
            if achou:
                print(f"Já existe um registro de ID {campos[0]}!")
                return
        with open("games.dat", "ab") as arq:
            arq.seek(0, os.SEEK_END)
            tamBytes = len(registro).to_bytes(2, 'little')
            arq.write(tamBytes)
            arq.write(registro.encode())
            
    except OSError as e:
        print(f"Erro: {e}")


def main() -> None:
    if len(sys.argv) > 3:
        print(f"Erro!\nUso: {sys.argv[0]} <-i> <Registro>")
    else:
        match sys.argv[1]:
            case "-i":
                insereRegistro(sys.argv[2])
            case _:
                print(f"Flag inválida!\nUso: {sys.argv[0]} <-i> <Registro>")


if __name__ == "__main__":
    main()