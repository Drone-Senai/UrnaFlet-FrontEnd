import flet as ft
import requests
from functools import partial

API_URL = "http://127.0.0.1:8000/"

def build(page: ft.Page):
    page.clean()
    page.scroll = ft.ScrollMode.AUTO
    page.title = "Votações Disponíveis"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    msg = ft.Text(value="", color=ft.Colors.RED)
    cards = ft.Column([], spacing=15, alignment=ft.MainAxisAlignment.CENTER)

    def ir_para_votacao(votacao_id: int):
        page.go(f"/votacao/{votacao_id}")

    def carregar_votacoes():
        try:
            res = requests.get(f"{API_URL}/votacoes")
            if res.status_code == 200:
                votacoes = res.json()
                cards.controls.clear()

                for v in votacoes:
                    cards.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Column([
                                    ft.Text("Data de Encerramento", weight="bold"),
                                    ft.Text(v["Data_final"] or "dd/mm/yyyy"),
                                ]),
                                ft.Column([
                                    ft.Text("Código", weight="bold"),
                                    ft.Text(str(v["ID_Votacao"])),
                                ]),
                                ft.Column([
                                    ft.Text("Assunto", weight="bold"),
                                    ft.Text(v["Tema"]),
                                ]),
                                ft.Column([
                                    ft.Text("Participantes", weight="bold"),
                                    ft.Text("XX"),  # Contador pode ser adicionado futuramente
                                ]),
                                ft.ElevatedButton(
                                    "Participar",
                                    bgcolor=ft.Colors.RED,
                                    color=ft.Colors.WHITE,
                                    on_click=partial(ir_para_votacao, v["ID_Votacao"]),
                                    style=ft.ButtonStyle(padding=15, shape=ft.RoundedRectangleBorder(radius=10))
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            border=ft.border.all(2, ft.Colors.RED),
                            border_radius=10,
                            padding=15,
                            margin=5,
                            bgcolor=ft.Colors.WHITE,
                            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.RED_100)
                        )
                    )
            else:
                cards.controls = [ft.Text("Erro ao carregar votações.", color=ft.Colors.RED)]

        except Exception as err:
            msg.value = f"Erro: {err}"
        page.update()

    def voltar(e):
        page.go("/")

    carregar_votacoes()

    return ft.View(
        route="/ver_votacao",
        controls=[
            ft.Column([
                ft.Text("Votações Disponíveis", size=30, weight="bold", color=ft.Colors.RED),
                cards,
                msg,
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "Voltar",
                    icon=ft.Icons.ARROW_BACK,
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE,
                    on_click=voltar
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True)
        ],
        scroll=ft.ScrollMode.AUTO,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
