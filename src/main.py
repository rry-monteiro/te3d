import random
import sys

from ursina import EditorCamera, Ursina, destroy

from Box import Box
from Layer import Layer
from Piece import Piece

XYZ: int = 8
TIPOS: list = ["I", "O", "T", "S", "Z", "L", "J"]
piece = None
ocupados: set = set()
camadas = {y: Layer(y=y, xyz=XYZ) for y in range(-XYZ * 2 + 1, 1)}


def main() -> None:
    app = Ursina("te3d")  # gerando app
    _ec = EditorCamera(rotation_speed=300, rotation_smoothing=10)  # habilitando camera
    _box = Box(XYZ)  # ligando a caixa
    spawn()  # chamando peça
    app.run()  # dando start no app


# invoca a peça
def spawn() -> None:
    global piece  # usa a peça de fora, sem criar
    tipo = random.choice(TIPOS)  # esoclhe o tipo aleatorio
    piece = Piece(tipo=tipo, xyz=XYZ, ocupados=ocupados, on_lock=on_lock)


# atualiza os ocupados, move as peças pra baixo
def organize():
    # <<<
    assert piece is not None
    posicoes = piece.get_positions()  # pega as posções da peça atual
    ocupados.update(posicoes)  # coloca elas no set

    for p in posicoes:
        if p[1] == -1:
            game_over()

    # coloca cada cubo na sua camada de acordo com y
    for cubo, (_, y, _) in zip(piece.cubos, posicoes):
        cubo.world_parent = camadas[y]

    ys_ocupados = {
        y for _, y, _ in posicoes
    }  # pega todas as camadas que foram ocupadas pela peça que chegou
    ys_cheias = {
        y for y in ys_ocupados if camadas[y].is_full()
    }  # pega todas as camadas que ficaram cheias

    # não completou nenhuma camada
    if not ys_cheias:
        return

    # itera nas camadas cheias e as limpa
    for y in ys_cheias:
        camadas[y].clear()

    # remove os ocupados
    ocupados.difference_update({pos for pos in ocupados if pos[1] in ys_cheias})

    camadas_num = -XYZ * 2 + 1
    # itera em todas as camadas pra descer quem precisa
    for y in sorted(camadas):
        # essa camada foi apagada, então ignora
        if y in ys_cheias:
            continue

        # se a camada não está onde deveria, seguimos
        if y != camadas_num:
            for cubo in list(camadas[y].children):
                # salva z e x
                x = round(cubo.world_x)
                z = round(cubo.world_z)
                # discarta a posição nos ocupados
                ocupados.discard((x, y, z))
                # muda de pai
                cubo.world_parent = camadas[camadas_num]
                # desce pra 0 agora que o pai ta certo
                cubo.y = 0
                # registra a nova posição nos ocupados
                ocupados.add((x, camadas_num, z))
        # proxima camada né bb
        camadas_num += 1
    # >>>


# fecha tudo e finaliza o jogo
def game_over() -> None:
    sys.exit()


# chamada quando a peça for travada
def on_lock() -> None:
    # chama a organização dos ocupados
    organize()

    # detroy a entity da peça
    destroy(piece)

    # chama a proxima peça (loop)
    spawn()


if __name__ == "__main__":
    main()
