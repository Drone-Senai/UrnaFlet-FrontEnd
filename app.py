import flet as ft
import requests

API_URL = "http://127.0.0.1:8000/"

def main(page: ft.Page):
    page.title = "Login com FastAPI"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    nome = ft.TextField(label="Usuário", width=300)
    email = ft.TextField(label="Email",  width=300)
    msg = ft.Text(value="", color=ft.Colors.RED)

    def registrar(e):
        res = requests.post(f"{API_URL}/register", json={
            "nome": nome.value,
            "email": email.value
        })
        if res.status_code == 200:
            msg.value = "Usuário criado com sucesso!"
            msg.color = ft.Colors.GREEN
        else:
            msg.value = res.json().get("detail", "Erro")
            msg.color = ft.Colors.RED
        page.update()

    def logar(e):
        res = requests.post(f"{API_URL}/login", json={
            "nome": nome.value,
            "email": email.value
        })
        if res.status_code == 200:
            token = res.json()["access_token"]
            msg.value = "Login realizado com sucesso!"
            msg.color = ft.Colors.GREEN
            # Aqui você pode salvar o token para requisições futuras
        else:
            msg.value = res.json().get("detail", "Erro ao logar")
            msg.color = ft.Colors.RED
        page.update()

    page.add(
        ft.Column([
            nome,
            email,
            ft.Row([
                ft.ElevatedButton("Registrar", on_click=registrar),
                ft.ElevatedButton("Login", on_click=logar)
            ]),
            msg
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(target=main)
