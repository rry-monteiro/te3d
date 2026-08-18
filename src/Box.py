import ursina

class Box(ursina.Entity):
    def __init__(self, xyz: int):
        super().__init__()
        self.xyz = xyz
        self._build()

    def _get_dimensions(self):
        # se for impar, ajusta somando 1
        if self.xyz % 2 == 1:
            self.xyz += 1
        # retorna lado da face quadrada e profundidade
        return self.xyz, self.xyz*2

    def _build(self):
        # ajustando as dimensões
        s, d = self._get_dimensions()

        map_limits = {
            # <<<
            'fundo': {
                'scale': (s, s),
                # 'rotation': (0, 0, 90),
                # 'position': (0.5, 0.5, d+0.5),
                'rotation': (90, 0, 0),
                'position': (0.5, -d+0.5, 0.5),
            },
            # direita
            'parede_1_dir': {
                'scale': (d, s),
                # 'rotation': (0, 90, 0),
                # 'position': (s/2 + 0.5, 0.5, s+0.5),
                'rotation': (0, 90, 90),
                'position': (s/2 + 0.5, -s+0.5, 0.5),
            },
            # esquerda
            'parede_2_esq': {
                'scale': (d, s),
                # 'rotation': (0, -90, 0),
                # 'position': (-s/2 + 0.5, 0.5, s + 0.5),
                'rotation': (0, -90, 90),
                'position': (-s/2 + 0.5, -s+0.5, 0.5),
            },
            # tras
            'parede_1_tras': {
                'scale': (s, d),
                # 'rotation': (90, 0, 0),
                # 'position': (0.5, -s/2 + 0.5, s + 0.5),
                'rotation': (0, 0, 0),
                'position': (0.5, -s + 0.5, s/2+0.5),
            },
            # frente
            'parede_2_fre': {
                'scale': (s, d),
                # 'rotation': (-90, 0, 0),
                # 'position': (0.5, s/2 + 0.5, s + 0.5),
                'rotation': (0, -180, 0),
                'position': (0.5, -s+0.5, -s/2+0.5),

            },
            # >>>
        }
        
        # itero nos dados do mapa pra gerar cada limite
        for nome, props in map_limits.items():
            ursina.Entity(
                model='quad',
                texture='white_cube',
                color=ursina.color.gray,
                shader=ursina.shaders.lit_with_shadows_shader,
                parent=self,
                scale=props['scale'],
                rotation=props['rotation'],
                position=props['position'],
            )
