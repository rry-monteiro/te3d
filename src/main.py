from Piece import Piece
from Box import Box
from Layer import Layer
from ursina import Ursina
from ursina import EditorCamera
import random

XYZ: int = 10
# TIPOS: list = ["I", "O", "T", "S", "Z", "L", "J"]
TIPOS: list = ["O"]
piece = None
ocupados: set = set()
_camadas = {y: Layer(y=y, xyz=XYZ) for y in range(-XYZ * 2 + 1, 1)}


def main() -> None:
    app = Ursina("te3d")  # gerando app
    _ec = EditorCamera(rotation_speed=300, rotation_smoothing=10)  # habilitando camera
    _box = Box(XYZ)  # ligando a caixa
    spawn()  # chamando peça
    app.run()  # dando start no app


# invoca a peça
def spawn() -> None:
    global piece  # usa a peça de fora, sem criar
    tipo: int = random.choice(TIPOS)  # esoclhe o tipo aleatorio
    piece = Piece(tipo=tipo, xyz=XYZ, ocupados=ocupados, on_lock=on_lock)


# chamada quando a peça for travada
def on_lock() -> None:
    posicoes = piece._get_positions()

    ocupados.update(posicoes)

    # coloca cada cubo na sua camada de acordo com y
    for cubo, (_, y, _) in zip(piece.cubos, posicoes):
        cubo.world_parent = _camadas[y]

    # filtra quais camadas foram alteradas
    ys_ocupados = {y for _, y, _ in posicoes}

    # verifica cada camada modificada e diz se ta cheia
    for y in ys_ocupados:
        if _camadas[y].is_full():
            print("CAMADA COMPLETA:", y)
    spawn()


if __name__ == "__main__":
    main()
