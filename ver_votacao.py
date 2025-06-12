import flet as ft
import requests
from functools import partial

API_URL = "http://127.0.0.1:8000"

def main(page: ft.Page):
    page.title = "Sistema de Votação"
    page.theme_mode = ft.ThemeMode.LIGHT

    def ir_para_votacao(e, votacao_id: int):
        page.go(f"/votacao/{votacao_id}")

    def carregar_view_lista_votacoes():
        res = requests.get(f"{API_URL}/votacoes")
        if res.status_code != 200:
            return ft.View("/", [ft.Text("Erro ao carregar votações")])

        votacoes = res.json()
        cards = []

        for v in votacoes:
            cards.append(
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
                             ft.Text("XX"),   # <--------Adicionar um contador real quando voto estiver pronto 
                        ]),
                        ft.ElevatedButton(
                            "Participar",
                            bgcolor=ft.Colors.RED,
                            color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(
                                padding=ft.padding.symmetric(horizontal=24, vertical=20)
                            ),
                            on_click=partial(ir_para_votacao, votacao_id=v["ID_Votacao"])
                        )
                    ],
                    alignment="spaceBetween"),
                    border=ft.border.all(2, ft.Colors.RED),
                    border_radius=10,
                    padding=10,
                    margin=5,
                    bgcolor=ft.Colors.WHITE,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=ft.Colors.RED_100,
                        offset=ft.Offset(2, 2)
                    )
                )
            )

        return ft.View(
            route="/",
            controls=[
                ft.Text("Votações", size=30, weight="bold", color=ft.Colors.RED),
                *cards
            ],
            vertical_alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    #/votacoes/1/objetos?eleitor_id=10 <--- exemplo
    def carregar_view_votacao(votacao_id: str):
        botoes_objetos_possiveis = []
        try:
            res = requests.get(f"{API_URL}/objetos")
            if res.status_code == 200:
                objetos = res.json()
                for obj in objetos:
                    botao = ft.ElevatedButton(
                        text=obj["nome"],
                        on_click=lambda e, oid=obj["id"]: obj(oid) # <--- FUNÇÃO A SER CHAMADA AINDA
                    )
                    botoes_objetos_possiveis.append(botao)
            else:
                botoes_objetos_possiveis.append(ft.Text("Erro ao buscar objetos."))
        except Exception as e:
            botoes_objetos_possiveis.append(ft.Text(f"Erro: {e} - FRONT-END"))
        
        page.views.append(
            ft.View(
                f"/addObjetoVotacao/{votacao_id}",
                [
                    ft.Text(f"Votar em qual Objeto para a votação: teste", size=20), #{votacao_nome}
                    *botoes_objetos_possiveis,
                    ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/"))
                ]
            )
        )
        page.go(f"/addEleitorVotacao/{votacao_id}")
        # return ft.View(
        #     route=f"/votacao/{votacao_id}",
        #     controls=[
        #         ft.Text(f"Você está na votação ID {votacao_id}", size=24),
        #         ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/"))
        #     ],
        #     vertical_alignment=ft.MainAxisAlignment.CENTER,
        #     horizontal_alignment=ft.CrossAxisAlignment.CENTER
        # )

    def route_change(e: ft.RouteChangeEvent):
        rota = e.route
        page.views.clear()

        if rota == "/":
            page.views.append(carregar_view_lista_votacoes())
        elif rota.startswith("/votacao/"):
            id_votacao = rota.split("/")[2]
            page.views.append(carregar_view_votacao(id_votacao))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
