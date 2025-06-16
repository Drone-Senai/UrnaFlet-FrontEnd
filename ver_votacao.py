import flet as ft
import requests
from functools import partial
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

API_URL = "http://127.0.0.1:8000"

def main(page: ft.Page):
    page.title = "Sistema de Votação"
    page.theme_mode = ft.ThemeMode.LIGHT

    def ir_para_votacao(e, votacao_id: int):
        page.go(f"/votacao/{votacao_id}")
        
    def ir_para_resultados(e, votacao_id: int):
        page.go(f"/resultados/{votacao_id}")

    def carregar_view_lista_votacoes():
        res = requests.get(f"{API_URL}/votacoes")
        if res.status_code != 200:
            return ft.View("/", [ft.Text("Erro ao carregar votações")])

        votacoes = res.json()
        cards = []

        for v in votacoes:

            data_final = datetime.strptime(v["Data_final"], "%d/%m/%Y")
            encerrada = data_final < datetime.now() or v["Status_Votacao"] == 0
            # print(encerrada)

            texto_botao = "Ver Resultados" if encerrada else "Participar"
            texto_status = "Encerrada" if encerrada else "Ativa"
            rota_destino = ir_para_resultados if encerrada else ir_para_votacao
                                    
            cards.append(
                ft.Container(
                    content=ft.Row ([
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
                            ft.Text("Status", weight="bold"),
                            ft.Text(texto_status),
                        ]),
                        ft.Column([
                            ft.Text("Participantes", weight="bold"),
                             ft.Text("XX"),   # <--------Adicionar um contador real quando voto estiver pronto 
                        ]),
                        # IF SE PASSOU DA DATA
                        ft.ElevatedButton(
                            texto_botao,
                            bgcolor=ft.Colors.RED,
                            color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(
                                padding=ft.padding.symmetric(horizontal=24, vertical=20)
                            ),
                            on_click=partial(rota_destino, votacao_id=v["ID_Votacao"])
                        )
                        # FIM DO IF
                    ],
                    alignment="spaceBetween"), # <--- FIM DA ROW
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
            res = requests.get(f"{API_URL}/objetos", params={"id_votacao": votacao_id})
            if res.status_code == 200:
                objetos = res.json()
                for obj in objetos:
                    def make_on_click(obj_id):
                        return lambda e: adicionar_voto(1, votacao_id, obj_id) #<--- 1 aqui provisorio até termos rotas funcionando para trazer o id_eleitor

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

    def gerar_grafico_base64(resultados):
        nomes = [r["nome"] for r in resultados]
        votos = [r["total_votos"] for r in resultados]

        fig, ax = plt.subplots(figsize=(5, 4), facecolor='none')
        ax.pie(votos, labels=nomes, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        fig.patch.set_alpha(0.0)

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', transparent=True)
        plt.close(fig)

        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        return img_base64
        
    def carregar_view_resultado(votacao_id: str):
        msg = ft.Text(value="", color=ft.Colors.RED)
        text_resultados = []

        try:
            res = requests.get(f"{API_URL}/resultados", params={"id_votacao": votacao_id})
            if res.status_code == 200:
                resultados = res.json()
                for result in resultados:
                    texto = ft.Text(
                        value=f"{result['nome']} - {result['total_votos']} voto(s)",
                        size=18
                    )
                    text_resultados.append(texto)
                

                img_base64 = gerar_grafico_base64(resultados)
                grafico_img = ft.Image(
                    src_base64=img_base64,
                    width=400,
                    height=400,
                    fit=ft.ImageFit.CONTAIN
                )

                # Encontrar quem ganhou (quem tem maior total_votos)
                vencedor = max(resultados, key=lambda r: r['total_votos'])
                resultado_votacao = ft.Text(
                    value=f"{vencedor['nome']} - Ganhou a Votação com {vencedor['total_votos']} voto(s)",
                    size=18,
                    weight='bold'
                )
            else:
                print("Erro ao buscar resultados")
        except Exception as e:
            print(f"Erro na requisição: {str(e)}")
        


        return ft.View(
            route=f"/resultados/{votacao_id}",
            controls=[
                ft.Text(f"Você está nos resultados da votação ID {votacao_id}", size=24),
                *text_resultados,
                grafico_img if grafico_img else ft.Text("Gráfico não disponível"),
                resultado_votacao,
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
        elif rota.startswith("/resultados/"):
            id_votacao = rota.split("/")[2]
            page.views.append(carregar_view_resultado(id_votacao))

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
