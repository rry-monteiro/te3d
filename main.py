from Piece import Piece
from Box import Box
from ursina import Ursina
from ursina import EditorCamera

XYZ = 17

def main():
    # gerando o app
    app = Ursina("te3d")

    # habilitando camera
    _ec = EditorCamera(
        rotation_speed=300,
        rotation_smoothing=10,
    )
        
    # gerando a caixa de limites
    app.run()

def input(key):
    match key:
        case 'space':
            play()

def play():
    box = Box(XYZ)
    box.build()
    piece = Piece("Z", box.xyz)
    piece.build()


if __name__ == "__main__":
    main()
