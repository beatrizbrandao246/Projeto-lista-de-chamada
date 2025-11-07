import flet as ft
import datetime

def main(page: ft.Page):
    page.theme_mode = "light"
    page.title = "Lista de Chamada Escolar"
    page.window.maximized = True
    page.padding = 15
    page.scroll = "adaptive"
    page.locale_configuration = ft.LocaleConfiguration(
        supported_locales=[
            ft.Locale( "pt" , "BR" ),
         ],
        current_locale=ft.Locale( "de" , "DE" ),
    )
    
    texto = ft.Text(
        "Lista de Chamada Escolar",
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLACK,
        text_align=ft.TextAlign.CENTER,
    )

    turmas = {
        "1º Ano A": [
            "Ana Silva",
            "Bruno Costa", 
            "Carla Santos",
            "Daniel Oliveira",
            "Eduarda Lima"
        ],
        "1º Ano B": [
            "Fernando Alves",
            "Gabriela Rocha", 
            "Henrique Dias",
            "Isabela Martins",
            "João Barbosa"
        ],
        "2º Ano A": [
            "Pedro de Alcântara",
            "Maria Eduarda Silva",
            "João Pedro Almeida"
        ],
        "2º Ano B": [
            "Ana Clara Mendonça",
            "Carlos Eduardo Lima",
            "Fernanda Cristina Costa"
        ],
        "3º Ano": [
            "Ricardo Augusto Souza",
            "Juliana Beatriz Alves",
            "Lucas Gabriel Mendes",
            "Patrícia Isabela Gomes"
        ]
    }

    turma_atual = "1º Ano A"
    status_dropdowns = []
    observacao_textfields = []
    container_principal = ft.Container()
    
    # Campo de texto para pesquisa por nome
    campo_pesquisa = ft.TextField(
        hint_text="Digite o nome do aluno...",
        width=250,
        text_size=14,
        border_color=ft.Colors.BLUE_400,
        border_width=1,
        border_radius=10,
        on_change=lambda e: filtrar_alunos()
    )

    def criar_cabecalho():
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "Nome do Aluno",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.LEFT,
                            color=ft.Colors.BLACK87,  
                        ),
                        expand=3,
                        padding=10,
                        alignment=ft.alignment.center_left,
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Status",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.Colors.BLACK87
                        ),
                        expand=2,
                        padding=15,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Observações",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.LEFT,
                            color=ft.Colors.BLACK87,
                        ),
                        expand=2,
                        padding=15,
                        alignment=ft.alignment.center_left,
                    ),
                ],
                expand=True,
            ),
            padding=10,
            bgcolor=ft.Colors.YELLOW_100,  
            border_radius=10,
            margin=ft.margin.only(bottom=10),
            expand=True,
        )

    def toggle_theme(e):
        if page.theme_mode == "light":
            page.theme_mode = "dark"
            texto.color = ft.Colors.WHITE
            e.control.selected = True
        else:
            page.theme_mode = "light"
            texto.color = ft.Colors.BLACK
            e.control.selected = False
        page.update()

    botao_tema = ft.IconButton(
        icon=ft.Icons.NIGHTLIGHT,
        selected_icon=ft.Icons.WB_SUNNY,
        on_click=toggle_theme,
        selected=False,
        style=ft.ButtonStyle(
            color={"selected": ft.Colors.WHITE, "": ft.Colors.BLACK}
        ),
    )

    def handle_change(e):
        texto_data.value = f"Data Escolhida: {e.control.value.strftime('%d/%m/%Y')}"
        texto_data.visible = True
        page.update()

    def handle_dismissal(e):
        page.add(ft.Text("Data Invalida"))

    botao_calendario = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
            ft.DatePicker(
                first_date=datetime.datetime(year=2025, month=1, day=1),
                last_date=datetime.datetime(year=2045, month=12, day=31),
                on_change=handle_change,
                on_dismiss=handle_dismissal,
            )
        )
    )

    def resetar_tudo(e):
        for dropdown in status_dropdowns:
            dropdown.value = None
            dropdown.border_color = ft.Colors.BLUE_400
            dropdown.color = ft.Colors.BLACK87
        for tf in observacao_textfields:
            tf.value = ""
        campo_pesquisa.value = ""  # Limpa a pesquisa
        carregar_alunos_turma(turma_atual)  # Recarrega para mostrar todos os alunos
        page.update()

    def atualizar_cor_dropdown(dropdown):
        if dropdown.value == "Presente":
            dropdown.border_color = ft.Colors.GREEN_600
            dropdown.color = ft.Colors.GREEN_600
        elif dropdown.value == "Faltou":
            dropdown.border_color = ft.Colors.RED_600
            dropdown.color = ft.Colors.RED_600
        elif dropdown.value == "Justificado":
            dropdown.border_color = ft.Colors.TEAL_600
            dropdown.color = ft.Colors.TEAL_600
        else:
            dropdown.border_color = ft.Colors.BLUE_400
            dropdown.color = ft.Colors.BLACK87

    def on_dropdown_change(e):
        atualizar_cor_dropdown(e.control)
        page.update()

    def mudar_turma(e):
        nonlocal turma_atual
        turma_atual = e.control.value
        texto_turma.value = f"Turma: {turma_atual}"
        campo_pesquisa.value = ""  # Limpa a pesquisa ao mudar de turma
        carregar_alunos_turma(turma_atual)
        page.update()

    # Função para filtrar alunos por nome
    def filtrar_alunos():
        termo_pesquisa = campo_pesquisa.value.lower().strip() if campo_pesquisa.value else ""
        alunos = turmas.get(turma_atual, [])
        
        linhas = [criar_cabecalho()]
        
        for i, aluno in enumerate(alunos):

            if not termo_pesquisa or termo_pesquisa in aluno.lower():
                status_dropdown = status_dropdowns[i]
                observacao_tf = observacao_textfields[i]
                
                nome_aluno = ft.Text(
                    aluno,
                    size=15,
                    text_align=ft.TextAlign.LEFT,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    color=ft.Colors.BLACK87,
                )

                linha = ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(nome_aluno, expand=3, alignment=ft.alignment.center_left, padding=10),
                            ft.Container(status_dropdown, expand=1, alignment=ft.alignment.center),
                            ft.Container(observacao_tf, expand=2, alignment=ft.alignment.center_left, padding=10),
                        ],
                        expand=True,
                    ),
                    padding=15,
                    border_radius=10,
                    bgcolor=ft.Colors.GREY_300,
                    margin=ft.margin.only(bottom=8),
                )
                linhas.append(linha)
        
        container_principal.content = ft.Column(
            controls=linhas, 
            spacing=10, 
            scroll=ft.ScrollMode.AUTO, 
            expand=True
        )
        page.update()

    def carregar_alunos_turma(turma_selecionada):
        status_dropdowns.clear()
        observacao_textfields.clear()
        
        alunos = turmas.get(turma_selecionada, [])
        
        linhas = [criar_cabecalho()]
        
        for aluno in alunos:
            status_dropdown = ft.Dropdown(
                width=150,
                options=[
                    ft.dropdown.Option("Presente"),
                    ft.dropdown.Option("Faltou"),
                    ft.dropdown.Option("Justificado"),
                ],
                hint_text="Selecione...",
                text_size=14,
                border_color=ft.Colors.BLACK87,
                color=ft.Colors.BLACK87,
                border_width=1,
                on_change=on_dropdown_change,
                border_radius=10, 
            )

            observacao_tf = ft.TextField(
                hint_text="Observações...",
                border="underline",
                multiline=False,
                text_size=14,
                content_padding=ft.padding.symmetric(horizontal=10, vertical=5),
                text_align=ft.TextAlign.LEFT,
                color=ft.Colors.BLACK87,
                cursor_color=ft.Colors.BLACK,
            )

            status_dropdowns.append(status_dropdown)
            observacao_textfields.append(observacao_tf)

            nome_aluno = ft.Text(
                aluno,
                size=15,
                text_align=ft.TextAlign.LEFT,
                max_lines=2,
                overflow=ft.TextOverflow.ELLIPSIS,
                color=ft.Colors.BLACK87,
            )

            linha = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(nome_aluno, expand=3, alignment=ft.alignment.center_left, padding=10),
                        ft.Container(status_dropdown, expand=1, alignment=ft.alignment.center),
                        ft.Container(observacao_tf, expand=2, alignment=ft.alignment.center_left, padding=10),
                    ],
                    expand=True,
                ),
                padding=15,
                border_radius=10,
                bgcolor=ft.Colors.GREY_300,
                margin=ft.margin.only(bottom=8),
            )
            linhas.append(linha)
        
        container_principal.content = ft.Column(
            controls=linhas, 
            spacing=10, 
            scroll=ft.ScrollMode.AUTO, 
            expand=True
        )

    dropdown_turmas = ft.Dropdown(
        width=200,
        options=[ft.dropdown.Option(turma) for turma in turmas.keys()],
        value=turma_atual,
        on_change=mudar_turma,
        text_size=12,
        border_color=ft.Colors.BLACK87,
        border_width=1,
        border_radius=50
    )

    texto_turma = ft.Text(
        f"Turma: {turma_atual}",
        size=14,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLACK87,
    )

    botao_salvar = ft.ElevatedButton("Salvar", bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE, width=200)
    botao_reset = ft.ElevatedButton("Reset", bgcolor=ft.Colors.RED, color=ft.Colors.WHITE, width=200, on_click=resetar_tudo)

    texto_data = ft.TextField(
        "",
        color=ft.Colors.BLACK,
        bgcolor=ft.Colors.GREY_100,
        width=280,
        read_only=True,
        visible=False,
    )

    carregar_alunos_turma(turma_atual)

    layout_principal = ft.Column(
        [
            ft.Container(content=texto, padding=20, alignment=ft.alignment.center),
            ft.Divider(height=10),
            ft.Row([botao_tema, botao_calendario, texto_data], alignment="center", spacing=20),
            ft.Row([
                texto_turma, 
                dropdown_turmas,
                ft.Container(expand=True), 
                campo_pesquisa  
            ], alignment="center", spacing=20),
            container_principal,
            ft.Divider(height=15),
            ft.Row([botao_reset, botao_salvar], alignment="end", spacing=20),
        ],  
        expand=True,
    )

    page.add(layout_principal)

ft.app(target=main)
