import ursina


class Layer(ursina.Entity):
    def __init__(self, xyz: int, y: int):
        # inicia a camada no y desejado
        # como serão criadas várias camadas de uma vez, passamos só a var y
        super().__init__(position=(0, y, 0))
        # quantos blocos a camada aguenta
        self.capacidade = xyz**2
        self.y_position = y
