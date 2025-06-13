import flet as ft
import subprocess, time
import re
import json
import requests
import urllib.parse
import asyncio
# Imagem e link de confirmação
LOGO_URL = "https://lh3.googleusercontent.com/chat_attachment/AP1Ws4vVUU-_RiAddakivrHdPYOfPlkue8vpmmpiekOqFJHLXHw04W9ubKgF9dOzpIve1YLvgvWQbyE7TWsNppU6lPSSM6b3dlk57eUNmKJWA3Ej2NJjSZKZ3mDOO7x-3UTsLpcM6KNbGzbwNaoO69CJ16IEPq5ufOPkkdaAsJs43W3S-f--oUh3-sRkMgNeBEwhs-y-lXP89UDFTHUPcpjUL3KSq8K8Vl8IMyE1m0qa2T7qn9f8eeOsQhpigyHoUByziDmVkc9CddqCuTP4ESrvYEw6pasfl-GlmH6b4RZ2ccWh5f2CevkMAK2oFJSw5WLF3aQ=w512"
CONFIRM_URL = "http://10.83.10.189:8000/confirmar?email="

API_URL = "http://127.0.0.1:8000/"

SMTP2GO_API_KEY = "api-250A06463CE94D1B8D229463C101927A"
REMETENTE_EMAIL = "guilherme.p.silva20@aluno.senai.br"
REMETENTE_NOME = "Sistema de Votação"

# def start_server():
#     subprocess.Popen(["python", "servidor.py"])

def enviar_email(email: str, existente: bool):
    encoded_email = urllib.parse.quote(email)

    if existente:
        conteudo = f"""
        <div style="font-family:Arial,sans-serif;background-color:#f9f9f9;padding:30px;text-align:center;color:#333;">
            <div style="max-width:600px;margin:auto;background-color:#ffffff;padding:30px;border-radius:10px;box-shadow:0 4px 8px rgba(0,0,0,0.1);">
                <img src="{LOGO_URL}" alt="Logo Votus" style="width:120px;margin-bottom:20px;border-radius:8px"/>
                <h1 style="color:#FF585B;">Bem-vindo de volta à Votus!</h1>
                <p style="font-size:16px;margin:20px 0;">
                    Identificamos que você já possui uma conta em nossa plataforma.
                    Deseja continuar com sua votação?
                </p>
                <a href="{CONFIRM_URL + encoded_email}" style="display:inline-block;margin:10px;padding:12px 24px;background-color:#FF585B;color:white;text-decoration:none;border-radius:5px;font-weight:bold;">
                    Sim, continuar votação
                </a>
                <a href="#" style="display:inline-block;margin:10px;padding:12px 24px;background-color:#cccccc;color:#333;text-decoration:none;border-radius:5px;">
                    Não, obrigado
                </a>
                <hr style="margin:40px 0;border:none;border-top:1px solid #eee"/>
                <p style="font-size:14px;color:#666;">
                    A <strong>Votus</strong> é a plataforma mais segura e moderna para suas votações. 
                    Privacidade, praticidade e confiança em cada clique. 🔒
                </p>
                <p style="font-size:13px;color:#aaa;">© 2025 Votus. Todos os direitos reservados.</p>
            </div>
        </div>
        """
    else:
        conteudo = f"""
        <div style="font-family:Arial,sans-serif;background-color:#f9f9f9;padding:30px;text-align:center;color:#333;">
            <div style="max-width:600px;margin:auto;background-color:#ffffff;padding:30px;border-radius:10px;box-shadow:0 4px 8px rgba(0,0,0,0.1);">
                <img src="{LOGO_URL}" alt="Logo Votus" style="width:120px;margin-bottom:20px;border-radius:8px"/>
                <h1 style="color:#FF585B;">Seja bem-vindo à Votus!</h1>
                <p style="font-size:16px;margin:20px 0;">
                    Percebemos que você ainda não tem uma conta em nossa plataforma.
                    Gostaria de se cadastrar agora e participar da votação?
                </p>
                <a href="{CONFIRM_URL + encoded_email}" style="display:inline-block;margin:10px;padding:12px 24px;background-color:#FF585B;color:white;text-decoration:none;border-radius:5px;font-weight:bold;">
                    Sim, quero me cadastrar
                </a>
                <a href="#" style="display:inline-block;margin:10px;padding:12px 24px;background-color:#cccccc;color:#333;text-decoration:none;border-radius:5px;">
                    Não, obrigado
                </a>
                <hr style="margin:40px 0;border:none;border-top:1px solid #eee"/>
                <p style="font-size:14px;color:#666;">
                    Descubra como a <strong>Votus</strong> revoluciona a forma de votar. 
                    Simples, intuitivo e totalmente online. Comece agora! 🗳️
                </p>
                <p style="font-size:13px;color:#aaa;">© 2025 Votus. Todos os direitos reservados.</p>
            </div>
        </div>
        """
        

    payload = {
        "api_key": SMTP2GO_API_KEY,
        "to": [email],
        "sender": REMETENTE_EMAIL,
        "subject": "Verificação de Conta",
        "html_body": conteudo,
        "text_body": "Verifique sua conta no site.",
        "custom_headers": [{"header": "Reply-To", "value": REMETENTE_EMAIL}]
    }

    response = requests.post(
        "https://api.smtp2go.com/v3/email/send",
        headers={"Content-Type": "application/json"},
        json=payload
    )

    print("Status:", response.status_code)
    print("Resposta:", response.text)
    return response.status_code == 200

def main(page: ft.Page):
    page.title = "Login"
    page.bgcolor = ft.Colors.WHITE
    page.window.full_screen = True
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # FUNÇÃO QUE ADD EMIAL NO BANCO DE DADOS
    def registrar(e):
        res = requests.post(f"{API_URL}/register", json={
            "email": email_field.value
        })
        print(email_field.value)
        if res.status_code == 200:
            print('Email adicionado com sucesso')
        else:
            print('Email não adicionado')
        page.update()


    email_field = ft.TextField(
        hint_text="Digite o seu email",
        border_color="#FF585B",
        bgcolor="#FFDEDE",
        color="#FF585B",
        width=300,
    )

    status_text = ft.Text("", color=ft.Colors.RED)

    async def verificar_email(e):
        email = email_field.value.strip()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            status_text.value = "Email inválido."
            page.update()
            return

        try:
            response = requests.post(f"{API_URL}/verificar-email", json={"email": email})
            response.raise_for_status()
            ja_cadastrado = response.json().get("existe", False)
        except Exception as ex:
            status_text.value = f"Erro ao verificar email: {ex}"
            page.update()
            return

        try:
            requests.post(f"{API_URL}/registrar-token", json={"email": email})
        except Exception as ex:
            status_text.value = f"Erro ao registrar token: {ex}"
            page.update()
            return

        if not ja_cadastrado:
            registrar(e)

        sucesso = enviar_email(email, ja_cadastrado)

        if sucesso:
            status_text.value = "Email enviado! Verifique sua caixa de entrada..."
            page.update()

            for _ in range(60):
                await asyncio.sleep(3)
                try:
                    r = requests.get(f"{API_URL}/confirmado", params={"email": email})
                    if r.status_code == 200 and r.json().get("confirmado"):
                        status_text.value = "✅ Email confirmado! Acesso liberado."
                        print("Email existente no Banco de Dados")
                        page.update()
                        return
                except:
                    pass
            status_text.value = "⏳ Tempo esgotado para confirmação."
            page.update()
        else:
            status_text.value = "Erro ao enviar o email. Veja o terminal."
            page.update()
    esquerda = ft.Container(
        content=ft.Column([
            ft.Text("Possui uma conta ?", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Text(
                "Ei, se você ainda não tem uma conta por aqui! Que tal aproveitar e \n"
                "se juntar ao melhor site de votações da internet? É rapidinho, grátis e você\n"
                " ainda participa das decisões mais importantes com apenas alguns cliques. \n"
                "Não fique de fora dessa — insira o seu e email no campo ao lado, verifique \n"
                "a sua caixa de SPAM e comece a votar com estilo!",
                size=14,
                color=ft.Colors.WHITE,
            ),
            ft.Text("OBS: O email pode demorar alguns segundos para chegar em seu correio!", size=14, color=ft.Colors.WHITE,weight=ft.FontWeight.W_600),
            ft.Image(src="image1.png", width=600)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=20),
        bgcolor="#FF585B",
        expand=True,
        padding=40
    )

    direita = ft.Container(
        content=ft.Column([
            ft.Text("Login", size=24, weight=ft.FontWeight.BOLD, color="#FF585B"),
            email_field,
            ft.ElevatedButton(
                "Login",
                bgcolor="#FF585B",
                color="white",
                on_click=verificar_email,
                width=300
            ),
            status_text
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20),
        expand=True
    )

    layout = ft.Row(
        controls=[esquerda, direita],
        expand=True
    )

    page.add(layout)


ft.app(target=main)
#rodar codigo com: uvicorn main:app --host 0.0.0.0 --port 8000 --reload