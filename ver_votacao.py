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
        msg = ft.Text(value="", color=ft.Colors.RED)
        botoes_objetos = []

        def adicionar_voto(id_eleitor, id_votacao, id_objeto_votacao):
            try:
                res = requests.post(f"{API_URL}/adicionar_voto", json={
                    "id_votacao": id_votacao,
                    "id_eleitor": id_eleitor,
                    "id_objeto_votacao": id_objeto_votacao
                })
                if res.status_code == 200:
                    msg.value = "Voto feito com sucesso!"
                    msg.color = ft.Colors.GREEN
                else:
                    msg.value = res.json().get("mensagem", "Erro ao votar.")
                    msg.color = ft.Colors.RED
            except Exception as err:
                msg.value = f"Erro: {err} - FRONT-END"
                msg.color = ft.Colors.RED
            page.update()

        try:
            res = requests.get(f"{API_URL}/objetos")
            if res.status_code == 200:
                objetos = res.json()
                for obj in objetos:
                    def make_on_click(obj_id):
                        return lambda e: adicionar_voto(1, votacao_id, obj_id)

                    btn = ft.ElevatedButton(
                        text=obj['nome'],
                        on_click=make_on_click(obj['id'])  # Correção do lambda
                    )
                    botoes_objetos.append(btn)
            else:
                print("Erro ao buscar objetos")
        except Exception as e:
            print(f"Erro na requisição: {str(e)}")

        return ft.View(
            route=f"/votacao/{votacao_id}",
            controls=[
                ft.Text(f"Você está na votação ID {votacao_id}", size=24),
                *botoes_objetos,
                ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/")),
                msg
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )



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
