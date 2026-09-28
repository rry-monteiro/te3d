import ursina
from typing import Literal


class Piece(ursina.Entity):
    def __init__(
        self,
        tipo: Literal["I", "O", "T", "S", "Z", "L", "J"],
        xyz: int,
        ocupados: set,
        on_lock=None,
    ):
        # <<<
        super().__init__()
        # limits da box
        self.limites = {
            # <<<
            "ymin": -xyz * 2 + 1,  # valor mínimo que a peça pode cair
            "xzmin": -(xyz / 2 - 1),  # valor mínimo que a peça pode andar para z e x
            "xzmax": xyz / 2,  # valor máximo que a peça pode andar para z e x
        }
        # >>>
        # mapa de tetraminos
        self.map_tetraminos = {
            # <<<
            "I": {
                "offsets": [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3)],
                "color": ursina.color.cyan,
            },
            "O": {
                "offsets": [(0, 0, 0), (0, 0, 1), (1, 0, 1), (1, 0, 0)],
                "color": ursina.color.yellow,
            },
            "T": {
                "offsets": [(0, 0, 0), (0, 0, 1), (-1, 0, 1), (1, 0, 1)],
                "color": ursina.color.violet,
            },
            "S": {
                "offsets": [(0, 0, 0), (0, 0, 1), (-1, 0, 0), (1, 0, 1)],
                "color": ursina.color.green,
            },
            "Z": {
                "offsets": [(0, 0, 0), (0, 0, 1), (-1, 0, 1), (1, 0, 0)],
                "color": ursina.color.red,
            },
            "L": {
                "offsets": [(0, 0, 0), (1, 0, 0), (0, 0, 1), (0, 0, 2)],
                "color": ursina.color.orange,
            },
            "J": {
                "offsets": [(0, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, 2)],
                "color": ursina.color.blue,
            },
        }
        # >>>
        # tipo de peça definida por letra
        self.tipo = tipo
        # shader padrão
        self.shader = ursina.shaders.lit_with_shadows_shader
        # offsets mutaveis
        self.mut_offsets = list(self.map_tetraminos[tipo]["offsets"])
        # referencias dos cubos
        self.cubos = []
        # set de lugares ja ocupados
        self.ocupados = ocupados
        # flag de peça travada
        self.esta_travada = False
        # função que é chamada quando a peça é ravada
        self.on_lock = on_lock
        # construção
        self._build()
        # inicia a queda
        self._init_queda()
        # >>>

    # constroi a peça
    def _build(self):
        # <<<
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
        # >>>

    # rotaciona a peça
    def _rotate(self, axis):
        # <<<
        """
        rotação matemática das peças, move os cubos para posições diferentes, dando a impressão de rotação
        regras (rotação 90° horário, regra da mão direita):
            X: (x, y, z) -> (x, -z,  y)
            Y: (x, y, z) -> ( z,  y, -x)
            Z: (x, y, z) -> (-y,  x,  z)
        """
        novos = []
        # salva quais serão os offsets novos depois das mudanças
        for x, y, z in self.mut_offsets:
            if axis == "x":
                novos.append((x, -z, y))
            elif axis == "y":
                novos.append((z, y, -x))
            elif axis == "z":
                novos.append((-y, x, z))

        # verifica se os offsets novos saem da box
        if not self._can_move(offsets=novos):
            return
        # salva a nova posição
        self.mut_offsets = novos
        # muda os cubos de lugar de acordo com os novos
        for i in range(len(self.cubos)):
            self.cubos[i].position = self.mut_offsets[i]
        # >>>

    # retorna uma lista de tuplas com as posições das peças da peça (ta confuso, mas retorna a posição da peça)
    def _get_positions(
        self, offsets=None, dx: float = 0, dy: float = 0, dz: float = 0
    ) -> list[tuple[float, float, float]]:
        return [
            # <<<
            (
                self.position.x + ox + dx,
                self.position.y + oy + dy,
                self.position.z + oz + dz,
            )
            for ox, oy, oz in (offsets if offsets else self.mut_offsets)
            # >>>
        ]

    # verifica se a peça pode se mover
    def _can_move(self, offsets=None, dx=0, dy=0, dz=0) -> bool:
        # <<<
        # pega as posições
        for x, y, z in self._get_positions(offsets=offsets, dx=dx, dy=dy, dz=dz):
            # verifica se ja ta ocupado
            if (x, y, z) in self.ocupados:
                return False
            # verifica se sai da caixa
            if x < self.limites["xzmin"] or x > self.limites["xzmax"]:
                return False
            if z < self.limites["xzmin"] or z > self.limites["xzmax"]:
                return False
            if y < self.limites["ymin"]:
                return False

        return True
        # >>>

    # tenta mover uma peça
    def _move(self, dx: float, dy: float, dz: float) -> bool:
        # <<<
        # verifica se não pode mover, se não puder, ja da return False
        if not self._can_move(dx=dx, dy=dy, dz=dz):
            return False
        # move a peça e retorna True
        self.position += (dx, dy, dz)
        return True
        # >>>

    # começa a queda
    def _init_queda(self) -> None:
        # <<<
        ursina.invoke(self._queda_unitaria, delay=0.5)
        # >>>

    # faz a peça cair de 1 em 1
    def _queda_unitaria(self) -> None:
        # <<<
        # se ja está travada, retorna
        if self.esta_travada:
            return

        # tenta mover
        move_ok = self._move(0, -1, 0)

        # se não moveu
        if not move_ok:
            # ta travada
            self.esta_travada = True
            # chama a função pra qunaod ela travar
            ursina.invoke(self.on_lock, delay=0.01)
            return
        # invoca novamente
        ursina.invoke(self._queda_unitaria, delay=0.5)
        # >>>

    # dropa a peça até o fim
    def _drop(self) -> None:
        # <<<
        # inicia uma distância com 0
        distancia_y = 0
        # loop que roda até _can_move retornar False
        # isso incrementa 1 na distância permitida, que depois é usada no _move
        while self._can_move(dx=0, dy=-(distancia_y + 1), dz=0):
            distancia_y += 1

        # movendo a peça pra ultima distância permitida
        self._move(0, -distancia_y, 0)

        self.esta_travada = True
        ursina.invoke(self.on_lock, delay=0.01)
        # >>>

    # recebe chaves do teclado e realiza ações
    def input(self, key):
        if self.esta_travada:
            return
        match key:
            case "space":
                self._drop()
            case "w":
                self._move(0, 0, 1)
            case "s":
                self._move(0, 0, -1)
            case "d":
                self._move(1, 0, 0)
            case "a":
                self._move(-1, 0, 0)
            case "1":
                self._rotate("y")
            case "2":
                self._rotate("x")
            case "3":
                self._rotate("z")
