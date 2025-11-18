import flet as ft
import datetime

def main(page: ft.Page):

    page.theme_mode = "light"
    page.title = "Lista de Chamada Escolar"
    page.window.maximized = True
    page.padding = 15
    page.scroll = "adaptive"
    page.locale_configuration = ft.LocaleConfiguration(
        supported_locales=[ft.Locale("pt", "BR")],
        current_locale=ft.Locale("pt", "BR"),
    )

    texto = ft.Text(
        "Lista de Chamada Escolar",
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    turmas = {
        "1º Ano A": ["Ana Silva", "Bruno Costa", "Carla Santos", "Daniel Oliveira", "Eduarda Lima"],
        "1º Ano B": ["Fernando Alves", "Gabriela Rocha", "Henrique Dias", "Isabela Martins", "João Barbosa"],
        "2º Ano A": ["Pedro de Alcântara", "Maria Eduarda Silva", "João Pedro Almeida"],
        "2º Ano B": ["Ana Clara Mendonça", "Carlos Eduardo Lima", "Fernanda Cristina Costa"],
        "3º Ano": ["Ricardo Augusto Souza", "Juliana Beatriz Alves", "Lucas Gabriel Mendes", "Patrícia Isabela Gomes"],
    }

    todos = []
    for v in turmas.values():
        todos.extend(v)
    turmas["Todos os Alunos"] = sorted(set(todos))

    turma_atual = "1º Ano A"
    status_dropdowns = []
    observacao_textfields = []
    container_principal = ft.Container()

    def criar_cabecalho():
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(ft.Text("Nome do Aluno", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                                 expand=3, padding=10, alignment=ft.alignment.center_left),
                    ft.Container(ft.Text("Status", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                                 expand=1, padding=10, alignment=ft.alignment.center),
                    ft.Container(ft.Text("Observações", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                                 expand=2, padding=10, alignment=ft.alignment.center_left),
                ],
                expand=True,
            ),
            bgcolor=ft.Colors.YELLOW_100,
            border_radius=10,
            padding=10,
            margin=ft.margin.only(bottom=10),
            expand=True,
        )

    cabecalho_bg_light = ft.Colors.YELLOW_100
    cabecalho_bg_dark = ft.Colors.GREY_400
    cabecalho = criar_cabecalho()

    def toggle_theme(e):
        if page.theme_mode == "light":
            page.theme_mode = "dark"
            texto.color = ft.Colors.WHITE
            cabecalho.bgcolor = cabecalho_bg_dark
            container_filtros.bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST
            container_filtros.border = ft.border.all(1, ft.Colors.GREY_700)
            container_filtros.shadow = ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK26)


            campo_pesquisa.color = ft.Colors.WHITE
            campo_pesquisa.hint_style = ft.TextStyle(color=ft.Colors.WHITE70)


            for tf in observacao_textfields:
                tf.bgcolor = ft.Colors.WHITE
                tf.color = ft.Colors.BLACK
                tf.hint_style = ft.TextStyle(color=ft.Colors.BLACK45)

            for dd in status_dropdowns:
                dd.bgcolor = ft.Colors.WHITE
                dd.color = ft.Colors.BLACK

            e.control.selected = True

        else:
            page.theme_mode = "light"
            texto.color = ft.Colors.BLACK
            cabecalho.bgcolor = cabecalho_bg_light
            container_filtros.bgcolor = ft.Colors.WHITE
            container_filtros.border = ft.border.all(1, ft.Colors.GREY_300)
            container_filtros.shadow = ft.BoxShadow(blur_radius=8, color=ft.Colors.GREY_400)

            campo_pesquisa.color = ft.Colors.BLACK
            campo_pesquisa.hint_style = ft.TextStyle(color=ft.Colors.BLACK54)

            for tf in observacao_textfields:
                tf.bgcolor = None
                tf.color = ft.Colors.BLACK
                tf.hint_style = ft.TextStyle(color=ft.Colors.BLACK45)

            for dd in status_dropdowns:
                dd.bgcolor = None
                dd.color = ft.Colors.BLACK87

            e.control.selected = False

        page.update()

    botao_tema = ft.IconButton(
        icon=ft.Icons.NIGHTLIGHT,
        selected_icon=ft.Icons.WB_SUNNY,
        on_click=toggle_theme,
        selected=False,
    )

    texto_data = ft.Text("", size=14, color="black")

    container_data = ft.Container(
        content=texto_data,
        padding=10,
        bgcolor=ft.Colors.GREY_200,   
        border_radius=8,
        visible=False,
    )

    def handle_change(e):
        texto_data.value = f"Data escolhida: {e.control.value.strftime('%d/%m/%Y')}"
        container_data.visible = True
        page.update()

    def handle_dismissal(e):
        page.snack_bar = ft.SnackBar(ft.Text("Data inválida"))
        page.snack_bar.open = True
        page.update()

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

    def carregar_alunos_turma(turma_selecionada, termo_pesquisa=""):
        status_dropdowns.clear()
        observacao_textfields.clear()
        alunos = turmas.get(turma_selecionada, [])
        linhas = [cabecalho]

        for aluno in alunos:
            if termo_pesquisa and termo_pesquisa.lower() not in aluno.lower():
                continue

            status_dropdown = ft.Dropdown(
                width=150,
                options=[
                    ft.dropdown.Option("Presente"),
                    ft.dropdown.Option("Faltou"),
                    ft.dropdown.Option("Justificado"),
                ],
                hint_text="Selecione...",
                text_size=14,
                border_color=ft.Colors.BLUE_400,
                border_width=1,
                color=ft.Colors.BLACK87,
                border_radius=10,
                on_change=on_dropdown_change,
            )


            observacao_tf = ft.TextField(
                hint_text="Observações...",
                border="underline",
                text_size=14,
                color=ft.Colors.BLACK,
                bgcolor=ft.Colors.WHITE if page.theme_mode == "dark" else None,
                content_padding=ft.padding.symmetric(horizontal=10, vertical=5),
                hint_style=ft.TextStyle(
                    color=ft.Colors.BLACK45 if page.theme_mode == "dark" else ft.Colors.BLACK38
                ),
            )

            status_dropdowns.append(status_dropdown)
            observacao_textfields.append(observacao_tf)

            nome_aluno = ft.Text(
                aluno, size=15, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS, color=ft.Colors.BLACK87
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
                bgcolor=ft.Colors.GREY_200,
                margin=ft.margin.only(bottom=8),
            )
            linhas.append(linha)

        if len(linhas) == 1:
            linhas.append(ft.Text("Nenhum aluno encontrado.", italic=True))

        container_principal.content = ft.Column(controls=linhas, spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
        page.update()


    campo_pesquisa = ft.TextField(
        hint_text="Digite o nome do aluno...",
        width=300,
        color=ft.Colors.BLACK,
        hint_style=ft.TextStyle(color=ft.Colors.BLACK54),
        on_change=lambda e: carregar_alunos_turma(turma_atual, campo_pesquisa.value.strip()),
    )

    texto_turma = ft.Text(f"Turma: {turma_atual}", size=14, weight=ft.FontWeight.BOLD)

    def mudar_turma(e):
        nonlocal turma_atual
        turma_atual = e.control.value
        texto_turma.value = f"Turma: {turma_atual}"
        campo_pesquisa.value = ""
        carregar_alunos_turma(turma_atual)
        page.update()

    dropdown_turmas = ft.Dropdown(
        width=220,
        options=[ft.dropdown.Option(t) for t in turmas.keys()],
        value=turma_atual,
        text_size=12,
        border_color=ft.Colors.BLACK87,
        border_width=1,
        border_radius=50,
        on_change=mudar_turma,  
    )

    filtros_row = ft.Row(
        controls=[
            ft.Row(
                controls=[
                    texto_turma,
                    dropdown_turmas,
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            campo_pesquisa,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    container_filtros = ft.Container(
        content=filtros_row,
        padding=10,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=12,
        margin=ft.margin.only(bottom=10),
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.GREY_400),
    )

    def resetar_tudo(e):
        for dropdown in status_dropdowns:
            dropdown.value = None
            dropdown.border_color = ft.Colors.BLUE_400
            dropdown.color = ft.Colors.BLACK87
        for tf in observacao_textfields:
            tf.value = ""
        campo_pesquisa.value = ""
        carregar_alunos_turma(turma_atual)
        page.update()

    botao_salvar = ft.ElevatedButton("Salvar", bgcolor="Green", color="WHITE", width=200)
    botao_reset = ft.ElevatedButton("Reset", bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE, width=160, on_click=resetar_tudo)

    carregar_alunos_turma(turma_atual)

    layout_principal = ft.Column(
        [
            ft.Container(content=texto, padding=20, alignment=ft.alignment.center),
            ft.Divider(height=10),
            ft.Row([botao_tema, botao_calendario, container_data], alignment="center", spacing=20),
            container_filtros,
            container_principal,
            ft.Divider(height=15),
            ft.Row([botao_reset, botao_salvar], alignment="end", spacing=20),
        ],
        expand=True,
    )

    page.add(layout_principal)

ft.app(target=main)
