import flet as ft
import requests
from datetime import datetime, date

API_URL = "http://127.0.0.1:8000/"

def main(page: ft.Page):
    page.title = "Cadastro de Projeto"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Campos de entrada
    nome = ft.TextField(label="Nome", width=300)
    tema = ft.TextField(label="Tema", width=300)
    data_atual = datetime.now()
    data_hoje = data_atual.strftime("%d/%m/%Y")
    data_encerramento_txt = ft.Text("Data de encerramento não selecionada", size=14)

    # Variável para guardar a data selecionada
    data_info = None  # Variável do tipo data

    def on_date_change(e):
        nonlocal data_info  # para modificar a variável do escopo externo
        data_info = e.control.value
        data_formatada = data_info.strftime("%d/%m/%Y")
        data_encerramento_txt.value = f"Encerramento: {data_formatada}"
        page.update()

    date_picker = ft.DatePicker(
        on_change=on_date_change,
        first_date=datetime(2000, 1, 1),
        last_date=datetime(2030, 12, 31),
    )
    page.overlay.append(date_picker)

    botao_data = ft.ElevatedButton("Selecionar Data de Encerramento", on_click=lambda _: page.open(date_picker))

    msg = ft.Text(value="", color=ft.Colors.RED)

    def AddVotacao(e):
        if not all([nome.value, tema.value, data_info]):
            msg.value = "Preencha todos os campos e selecione uma data."
            msg.color = ft.Colors.RED
            page.update()
            return

        try:
            res = requests.post(f"{API_URL}/addVotacao", json={
                "nome": nome.value,
                "tema": tema.value,
                "data_hoje": data_hoje,
                "data_encerramento": data_info.strftime("%d/%m/%Y")  
            })
            if res.status_code == 200:
                msg.value = "Votação Adicionada com sucesso!"
                msg.color = ft.Colors.GREEN
            else:
                msg.value = res.json().get("detail", "Erro ao Adicionar")
                msg.color = ft.Colors.RED
        except Exception as err:
            msg.value = f"Erro na requisição: {err}"
            msg.color = ft.Colors.RED

        page.update()
    
    encerrar_id = ft.TextField(label="ID da Votação para Encerrar", width=300)

    def encerrar_votacao(e):
        if not encerrar_id.value:
            msg.value = "Digite o ID da votação que deseja encerrar."
            msg.color = ft.Colors.RED
            page.update()
            return
        try:
            res = requests.post(f"{API_URL}/encerrarVotacao", json={"id_votacao": int(encerrar_id.value)})
            if res.status_code == 200:
                msg.value = f"Votação {encerrar_id.value} encerrada com sucesso!"
                msg.color = ft.Colors.GREEN
            else:
                msg.value = res.json().get("detail", "Erro ao encerrar votação.")
                msg.color = ft.Colors.RED
        except Exception as err:
            msg.value = f"Erro na requisição: {err}"
            msg.color = ft.Colors.RED
        page.update()

    # Layout da página
    page.add(
        ft.Column([
            nome,
            tema,
            botao_data,
            data_encerramento_txt,
            ft.ElevatedButton("Adicionar Votação", on_click=AddVotacao),
            ft.Divider(),
            encerrar_id,
            ft.ElevatedButton("Encerrar Votação", on_click=encerrar_votacao),
            msg
        ])
    )

ft.app(target=main)
