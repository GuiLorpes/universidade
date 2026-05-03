import os
import io
import sys


def insereRegistro(registro: str) -> None:
    try:
        # Verifica se encontra um id igual
        with open("primario.ind", "rb") as ids:
            campos = registro.split('|')
            id = int.to_bytes(ids.read(4),'little')
            i = 0
            while id > 0 and id != int(campos[0]):
                # offset é 
                offset = (i * 4)
                id.seek(offset)
            # Se encontrou, não insere
            
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