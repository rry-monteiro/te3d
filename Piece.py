import ursina
from typing import Literal


class Piece(ursina.Entity):
    def __init__(self, tipo: Literal["I", "O", "T", "S", "Z", "L", "J"]):
        super().__init__()
        self.map_tetraminos = {
            # <<<
            "I": {
                "offsets": [(0, 0, 0), (0, 1, 0), (0, 2, 0), (0, 3, 0)],
                "color": ursina.color.cyan,
            },
            "O": {
                "offsets": [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0)],
                "color": ursina.color.yellow,
            },
            "T": {
                "offsets": [(0, 0, 0), (0, 1, 0), (-1, 1, 0), (1, 1, 0)],
                "color": ursina.color.violet,
            },
            "S": {
                "offsets": [(0, 0, 0), (0, 1, 0), (-1, 0, 0), (1, 1, 0)],
                "color": ursina.color.green,
            },
            "Z": {
                "offsets": [(0, 0, 0), (0, 1, 0), (-1, 1, 0), (1, 0, 0)],
                "color": ursina.color.red,
            },
            "L": {
                "offsets": [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 2, 0)],
                "color": ursina.color.orange,
            },
            "J": {
                "offsets": [(0, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 2, 0)],
                "color": ursina.color.blue,
            },
            # >>>
        }

        # tipo de peça definida por letra
        self.tipo = tipo
        # shader padrão
        self.shader = ursina.shaders.lit_with_shadows_shader
        # offsets mutaveis
        self.mut_offsets = list(self.map_tetraminos[tipo]["offsets"])
        # referencias dos cubos
        self.cubos = []

    # constroi a peça
    def build(self):
        for offset in self.map_tetraminos[self.tipo]["offsets"]:
            cubo = ursina.Entity(
                model="cube",
                name="tetris",
                texture="brick",
                position=offset,
                color=self.map_tetraminos[self.tipo]["color"],
                shader=self.shader,
                parent=self,
            )
            self.cubos.append(cubo)

    """
    rotação matemática das peças, move os cubos para posições diferentes, dando a impressão de rotação
    Regras (rotação 90° horário, regra da mão direita):
        X: (x, y, z) -> (x, -z,  y)
        Y: (x, y, z) -> ( z,  y, -x)
        Z: (x, y, z) -> (-y,  x,  z)
    """
    def rotate(self, axis):
        novos_offsets = []
        for x, y, z in self.mut_offsets:
            if axis == "x":
                # Gira no plano YZ: Y vira Z (invertido), Z vira Y
                nx, ny, nz = x, -z, y
            elif axis == "y":
                # Gira no plano XZ: X vira Z, Z vira X (invertido)
                nx, ny, nz = z, y, -x
            elif axis == "z":
                # Gira no plano XY: X vira Y (invertido), Y vira X
                nx, ny, nz = -y, x, z

            novos_offsets.append((nx, ny, nz))

        # TODO: aqui futuramente vai a verificação de colisão
        # if not self._is_valid(novos_offsets):
        #     return  # não gira se colidir com algo

        self.mut_offsets = novos_offsets
        for cubo, offset in zip(self.cubos, self.mut_offsets):
            cubo.position = offset

    # recebe chaves do teclado e realiza ações
    def input(self, key):
        match key:
            case "w":
                self.position += (0, 1, 0)  # +y
            case "s":
                self.position += (0, -1, 0)  # -y
            case "d":
                self.position += (1, 0, 0)  # +x
            case "a":
                self.position += (-1, 0, 0)  # -x
            case "h":
                self.rotate("y")
            case "j":
                self.rotate("x")
            case "k":
                self.rotate("z")
