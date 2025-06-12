import flet as ft
from telas import inicial_ADM, objeto_ADM, objeto_votacao_ADM

def main(page: ft.Page):
    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(inicial_ADM.build(page))
        elif page.route == "/objetos":
            page.views.append(objeto_ADM.build(page))
        elif page.route == "/objeto-votacao":
            page.views.append(objeto_votacao_ADM.build(page))
        page.update()
    page.on_route_change = route_change
    page.go(page.route or "/")  # abre a rota atual ou padrão "/"

ft.app(target=main)
