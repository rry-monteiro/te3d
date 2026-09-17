from ursina import Button, color, Vec2

explode = Button(
    "EXPLODE",
    color=color.black,
    origin=(7, 0),
    on_click=mundi.explode_sphere,
    scale=Vec2(0.113, 0.06),
)

implode = Button(
    "IMPLODE",
    color=color.black,
    origin=(7, 2),
    on_click=Func(mundi.implode_sphere),
    scale=Vec2(0.113, 0.06),
)

ajuda = Button(
    "AJUDA",
    parent=camera.ui,
    scale=(0.12, 0.06),
    position=(0.75, 0.45),
    on_click=Func(open_info),
)
