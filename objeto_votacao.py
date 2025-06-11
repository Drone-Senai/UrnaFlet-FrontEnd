import flet as ft
import requests

API_URL = "http://127.0.0.1:8000/"  # Seu endpoint base

# Página de inserção de objetos
def objeto_page(page: ft.Page, votacao_id, votacao_nome):
    msg = ft.Text(value="", color=ft.Colors.RED)
    botoes_objetos = []

    def adicionar_objeto(objeto_id):
        try:
            res = requests.post(f"{API_URL}/addObjetoVotacao", json={
                "id_votacao": votacao_id,
                "id_objeto": objeto_id
            })
            if res.status_code == 200:
                msg.value = f"Objeto {objeto_id} adicionado com sucesso!"
                msg.color = ft.Colors.GREEN
            else:
                msg.value = res.json().get("detail", "Erro ao adicionar objeto.")
                msg.color = ft.Colors.RED
        except Exception as err:
            msg.value = f"Erro: {err}"
            msg.color = ft.Colors.RED
        page.update()

    # Buscar objetos
    try:
        res = requests.get(f"{API_URL}/objetos")
        if res.status_code == 200:
            objetos = res.json()
            for obj in objetos:
                botao = ft.ElevatedButton(
                    text=obj["nome"],
                    on_click=lambda e, oid=obj["id"]: adicionar_objeto(oid)
                )
                botoes_objetos.append(botao)
        else:
            botoes_objetos.append(ft.Text("Erro ao buscar objetos."))
    except Exception as e:
        botoes_objetos.append(ft.Text(f"Erro: {e}"))

    page.views.append(
        ft.View(
            f"/addObjetoVotacao/{votacao_id}",
            [
                ft.Text(f"Adicionar Objetos à Votação: {votacao_nome}", size=20),
                *botoes_objetos,
                ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/")),
                msg
            ]
        )
    )
    page.go(f"/addObjetoVotacao/{votacao_id}")



# Página inicial com botões dinâmicos
def main(page: ft.Page):
    page.title = "Lista de Votações"
    page.vertical_alignment = ft.MainAxisAlignment.START

    def carregar_votacoes():
        try:
            res = requests.get(f"{API_URL}/votacoes")
            if res.status_code == 200:
                votacoes = res.json()
                botoes = []
                for votacao in votacoes:
                    botao = ft.ElevatedButton(
                        text=f"{votacao['Nome']} - {votacao['Tema']}",
                        on_click=lambda e, v=votacao: objeto_page(page, v["ID_Votacao"], v["Nome"])
                    )
                    botoes.append(botao)
                page.views.append(
                    ft.View(
                        "/",
                        [
                            ft.Text("Escolha uma votação:", size=24),
                            *botoes
                        ]
                    )
                )
                page.go("/")
            else:
                page.add(ft.Text("Erro ao buscar votações. - Front-End"))
        except Exception as e:
            page.add(ft.Text(f"Erro na conexão: {e} - Front-End"))

    page.on_route_change = lambda e: None
    carregar_votacoes()


ft.app(target=main)
