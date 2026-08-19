# Tetris 3D (de verdade).

## Descrição:
Uma simples cópia do Tetris, mas em três dimensões

Não encontrei muitas versões do Tetris realmente 3D, há muitas opções com jogabilidade 2D e gráficos 3D, então quis fazer minha versão.

Aliás, preferi o ursina porque meu PCCT, o **mundi-pieces**, foi baseado nele, acho uma engine simples e poderosa, acredito que tenha sido a melhor escolha.

## Instalação
### Via pip:
```bash
# clona o repo
git clone https://github.com/rry-monteiro/tot.git
cd tot
pip install pyinstaller
pyinstaller tot.spec
# copia pro local
```

### Via UV (recomendado):
```bash
# clona o repo
git clone https://github.com/rry-monteiro/te3d.git
cd te3d
# sincroniza
uv sync
# compacta
uv run pyinstaller te3d.spec
```

## Imagens: