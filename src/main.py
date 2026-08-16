from Piece import Piece
from Box import Box
from ursina import Ursina
from ursina import EditorCamera
import random

XYZ = 16
TIPOS = ["I", "O", "T", "S", "Z", "L", "J"]
piece = None


def main() -> None:
    app = Ursina("te3d")  # gerando app
    _ec = EditorCamera(rotation_speed=300, rotation_smoothing=10) # habilitando camera
    _box = Box(XYZ) # ligando a caixa
    spawn() # chamando peça
    app.run()

def spawn():
    global piece
    tipo = random.choice(TIPOS)  # esoclhe o tipo aleatorio
    piece = Piece(tipo, XYZ)

def new():
    spawn()


if __name__ == "__main__":
    main()
