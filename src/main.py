from Piece import Piece
from Box import Box
from ursina import Ursina
from ursina import EditorCamera
import random

XYZ: int = 10
TIPOS: list = ["I", "O", "T", "S", "Z", "L", "J"]
piece = None
ocupados: set = set()


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
    for ox, oy, oz in piece.mut_offsets:
        position = piece.position
        x, y, z = position.x + ox, position.y + oy, position.z + oz
        ocupados.add((x, y, z))
    spawn()


if __name__ == "__main__":
    main()
