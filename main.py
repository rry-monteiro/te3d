from Piece import Piece
from Box import Box
from ursina import Ursina
from ursina import EditorCamera


def input(key):
    match key:
        case "space":
             print("space")
def main():
    
    # gerando o app
    app = Ursina("te3d")

    # habilitando camera
    _ec = EditorCamera(
        rotation_speed=300,
        rotation_smoothing=10,
    )
        
    # gerando a caixa de limites
    box = Box(16)
    box.build()

    piece = Piece("Z")
    piece.build()

    # rodando app
    app.run()
    return


if __name__ == "__main__":
    main()
