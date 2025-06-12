import flet as ft
import requests

API_URL = "http://127.0.0.1:8000/"  # Seu endpoint base

# Página de inserção de objetos
def objeto_page(page: ft.Page, votacao_id, votacao_nome):
    msg = ft.Text(value="", color=ft.Colors.RED)
    botoes_eleitor = []

    def adicionar_eleitor(eleitor_id):
        try:
            res = requests.post(f"{API_URL}/addEleitorVotacao", json={
                "id_votacao": votacao_id,
                "id_eleitor": eleitor_id,
                "valido": 1 # FUTURAMENTE COLOCAR UMA VERIFICAÇÃO DE SE ELEITOR PODE VOTAR
            })
            if res.status_code == 200:
                msg.value = f"Objeto {eleitor_id} adicionado com sucesso!"
                msg.color = ft.Colors.GREEN
            else:
                msg.value = res.json().get("detail", "Erro ao adicionar objeto.")
                msg.color = ft.Colors.RED
        except Exception as err:
            msg.value = f"Erro: {err} - FRONT-END"
            msg.color = ft.Colors.RED
        page.update()

    # Buscar eleitores
    try:
        res = requests.get(f"{API_URL}/eleitores")
        if res.status_code == 200:
            eleitores = res.json()
            for eleitor in eleitores:
                botao = ft.ElevatedButton(
                    text=eleitor["nome"],
                    on_click=lambda e, oid=eleitor["id"]: adicionar_eleitor(oid)
                )
                botoes_eleitor.append(botao)
        else:
            botoes_eleitor.append(ft.Text("Erro ao buscar eleitores."))
    except Exception as e:
        botoes_eleitor.append(ft.Text(f"Erro: {e} - FRONT-END"))

    page.views.append(
        ft.View(
            f"/addObjetoVotacao/{votacao_id}",
            [
                ft.Text(f"Adicionar Eleitor à Votação: {votacao_nome}", size=20),
                *botoes_eleitor,
                ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/")),
                msg
            ]
        )
    )
    page.go(f"/addEleitorVotacao/{votacao_id}")



# Página inicial com botões dinâmicos - NOMES DAS VOTAÇÕES
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
                        on_click=lambda e, v=votacao: objeto_page(page, v["ID_Votacao"], v["Nome"]) # FUNÇÃO QUE MANDA PRA OUTRA PAGINA COM OS OBJETOS
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