import flet as ft
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
from PIL import Image

def main(page: ft.Page):
    page.title = "Simulador de Juros Composto"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def calcular_juros_composto(e):
        # Obter os valores inseridos pelo usuário
        try:
            inicial = float(valor_inicial.value.replace(",", "."))
            mensal = float(valor_mensal.value.replace(",", "."))
            juros = float(taxa_juros.value.replace(",", ".")) / 100
            time = int(tempo.value)

            # Calcular os valores ao longo do tempo
            tempos = list(range(time + 1))
            valores = [inicial * (1 + juros) ** t + mensal * ((1 + juros) ** t - 1) / juros if juros != 0 else inicial + mensal * t for t in tempos]

            # Gerar o gráfico
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(tempos, valores, label="Valor ao longo do tempo")
            ax.set_title("Crescimento de um valor com Juros Compostos e Aportes Mensais")
            ax.set_xlabel("Tempo (anos)")
            ax.set_ylabel("Valor acumulado (R$)")
            ax.grid(True)
            ax.legend()

            # Salvar o gráfico em um buffer de memória
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)

            # Converte o buffer de imagem para algo que o Flet possa exibir
            img = Image.open(buf)
            img.show()  # Se você quiser visualizar o gráfico em um visualizador de imagens, pode descomentar esta linha

            # Converter para o formato que o Flet pode mostrar
            chart_image.value = buf
            chart_image.visible = True
            page.update()

            # Exibir o resultado final
            resultado.value = f"R$ {valores[-1]:.2f}".replace(".", ",")
            resultado.visible = True
            page.update()

        except ValueError:
            page.add(ft.Text("Por favor, insira valores válidos.", color="red"))
            page.update()

    # Elementos da interface
    text_titulo = ft.Text("Simulador de Juros Composto", size=30, weight=ft.FontWeight.BOLD)
    text_valor_inicial = ft.Text("Valor inicial:", size=20)
    valor_inicial = ft.TextField(label="0,00", width=200)
    text_valor_mensal = ft.Text("Valor mensal:", size=20)
    valor_mensal = ft.TextField(label="0,00", width=200)
    text_taxa_juros = ft.Text("Taxa de juros (Anual):", size=20)
    taxa_juros = ft.TextField(label="0,00", width=200)
    text_tempo = ft.Text("Tempo (Anos):", size=20)
    tempo = ft.TextField(label="0", width=200)
    botão = ft.ElevatedButton("Calcular", width=200, on_click=calcular_juros_composto)
    text_resultado = ft.Text("Resultado:", size=20)
    resultado = ft.Text("0,00", size=20, weight=ft.FontWeight.BOLD, visible=False)

    # Container para exibir o gráfico
    chart_image = ft.Image(src="", visible=False)

    # Adicionar os elementos à página
    page.add(
        text_titulo,
        text_valor_inicial,
        valor_inicial,
        text_valor_mensal,
        valor_mensal,
        text_taxa_juros,
        taxa_juros,
        text_tempo,
        tempo,
        text_resultado,
        resultado,
        botão,
        chart_image
    )

# Iniciar o aplicativo Flet
ft.app(target=main)
