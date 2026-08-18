import ursina
from typing import Literal

class Piece(ursina.Entity):
    def __init__(
            self,
            tipo: Literal["I", "O", "T", "S", "Z", "L", "J"],
            xyz:int,
            ocupados:set,
            on_lock=None,
    ):
        # <<<
        super().__init__()
        # limits da box
        self.limites = {
            # <<<
            'ymin' : -xyz*2+1,    # valor mínimo que a peça pode cair
            'xzmin' : -(xyz/2-1), # valor mínimo que a peça pode andar para z e x
            'xzmax' : xyz/2       # valor máximo que a peça pode andar para z e x
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
        self.ocupados=ocupados
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
    def rotate(self, axis):
        # <<<
        """
        rotação matemática das peças, move os cubos para posições diferentes, dando a impressão de rotação
        Regras (rotação 90° horário, regra da mão direita):
            X: (x, y, z) -> (x, -z,  y)
            Y: (x, y, z) -> ( z,  y, -x)
            Z: (x, y, z) -> (-y,  x,  z)
        """
        novos = []
        # salva quais serão os offsets novos depois das mudanças
        for x, y, z in self.mut_offsets:
            if axis == "x":   novos.append((x, -z, y))
            elif axis == "y": novos.append((z, y, -x))
            elif axis == "z": novos.append((-y, x, z))

        # verifica se os offsets novos saem da box
        for ox, oy, oz in novos:
            # coma os offsets novos com os atuais
            cx = self.position.x + ox
            cy = self.position.y + oy
            cz = self.position.z + oz

            # verifica se algum deles passa da box
            if cx < self.limites["xzmin"] or cx > self.limites["xzmax"]: return
            if cz < self.limites["xzmin"] or cz > self.limites["xzmax"]: return
            if cy > self.limites["ymin"]: return

            # verificação de colisão com outras peças
            if (cx, cy, cz) in self.ocupados: return

        # salva a nova posição
        self.mut_offsets = novos
        # muda os cubos de lugar de acordo com os novos
        for i in range(len(self.cubos)):
            self.cubos[i].position = self.mut_offsets[i]
        # >>>

    # tenta mover uma peça
    def move(self, dx:float, dy:float, dz:float)->None:
        # <<<
        #cria as posições virtuais
        for ox, oy, oz in self.mut_offsets:
            cx = self.position.x + ox + dx
            cy = self.position.y + oy + dy
            cz = self.position.z + oz + dz

            # verifica se elas saem da box
            if cx < self.limites["xzmin"] or cx > self.limites["xzmax"]: return False
            if cz < self.limites["xzmin"] or cz > self.limites["xzmax"]: return False
            if cy < self.limites["ymin"]: return False

            # verificação de colisão com outras peças
            if (cx, cy, cz) in self.ocupados: return False

        # altera a posição
        self.position += (dx, dy, dz)
        return True
        # >>>

    # começa a queda
    def _init_queda(self):
        # <<<
        ursina.invoke(self._queda_unitaria, delay=.5)
        # >>>

    # faz a peça cair de 1 em 1
    def _queda_unitaria(self):
        # <<<
        # se ja está travada, retorna
        if self.esta_travada: return

        # tenta mover
        move_ok = self.move(0,-1,0)

        # se não moveu
        if not move_ok:
            # ta travada
            self.esta_travada = True
            # chama a função pra qunaod ela travar
            self.on_lock()
            return
        # invoca novamente
        ursina.invoke(self._queda_unitaria, delay=.5)
        # >>>

    # recebe chaves do teclado e realiza ações
    def input(self, key):
        if self.esta_travada: return
        match key:
            case "space": pass  # hard drop depois
            case "w": self.move(0, 1, 0)
            case "s": self.move(0, -1, 0)
            case "d": self.move(1, 0, 0)
            case "a": self.move(-1, 0, 0)
            case "h": self.rotate("y")
            case "j": self.rotate("x")
            case "k": self.rotate("z")
