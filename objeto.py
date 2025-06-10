import flet as ft
import requests

API_URL = "http://127.0.0.1:8000/"

def main(page: ft.Page):
    page.title = "Cadastro de Objeto"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    nome = ft.TextField(label="Nome do Objeto", width=300)
    descricao = ft.TextField(label="Descrição", multiline=True, width=300)
    msg = ft.Text(value="", color=ft.Colors.RED)
    foto_path = ft.Text(value="")

    imagem_visualizacao = ft.Image(src="", width=200, visible=False)

    file_picker = ft.FilePicker()

    def selecionar_foto(e):
        file_picker.pick_files(allow_multiple=False)

    def foto_selecionada(e: ft.FilePickerResultEvent):
        if e.files:
            foto_path.value = e.files[0].path
            page.update()

    def cadastrar(e):
        if not foto_path.value:
            msg.value = "Selecione uma imagem."
            msg.color = ft.Colors.RED
            imagem_visualizacao.visible = False
            page.update()
            return

        with open(foto_path.value, "rb") as f:
            files = {"foto": f}
            data = {"nome": nome.value, "descricao": descricao.value}
            res = requests.post(f"{API_URL}/objeto", data=data, files=files)

        if res.status_code == 200:
            dados = res.json()
            objeto_id = dados.get("id")

            msg.value = (
                f"Objeto cadastrado com sucesso!\n"
                f"Nome: {dados.get('nome')}\n"
                f"Descrição: {dados.get('descricao')}"
            )
            msg.color = ft.Colors.GREEN

            imagem_visualizacao.src = f"{API_URL}imagem/{objeto_id}"
            imagem_visualizacao.visible = True
        else:
            msg.value = res.json().get("detail", "Erro ao cadastrar")
            msg.color = ft.Colors.RED
            imagem_visualizacao.visible = False

        page.update()

    file_picker.on_result = foto_selecionada
    page.overlay.append(file_picker)  # ESSENCIAL para evitar erro do FilePicker

    page.add(
        ft.Column([
            nome,
            descricao,
            ft.ElevatedButton("Selecionar Foto", on_click=selecionar_foto),
            foto_path,
            ft.ElevatedButton("Cadastrar Objeto", on_click=cadastrar),
            msg,
            imagem_visualizacao
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(target=main)
