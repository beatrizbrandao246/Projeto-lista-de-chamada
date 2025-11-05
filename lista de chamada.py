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


    cabecalho = ft.Container(
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
                    expand=5,  
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


    presenca_checkboxes = []
    falta_checkboxes = []
    observacao_textfields = []


    def toggle_theme(e):
        if page.theme_mode == "light":
            page.theme_mode = "dark"
            texto.color = ft.Colors.WHITE
            cabecalho.bgcolor = ft.Colors.GREY_500  
            e.control.selected = True
        else:
            page.theme_mode = "light"
            texto.color = ft.Colors.BLACK
            cabecalho.bgcolor = ft.Colors.YELLOW_100  
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
        for cb in presenca_checkboxes:
            cb.value = False
        for cb in falta_checkboxes:
            cb.value = False
        for tf in observacao_textfields:
            tf.value = ""
        page.update()


    botao_salvar = ft.ElevatedButton("Salvar", bgcolor="Green", color="WHITE", width=200)
    botao_reset = ft.ElevatedButton("Reset", bgcolor="Red", color="WHITE", width=200, on_click=resetar_tudo)


    texto_data = ft.TextField(
        "",
        color="black",
        bgcolor=ft.Colors.GREY_100,
        width=280,
        read_only=True,
        visible=False,
    )




    alunos = sorted([
        "Pedro de Alcântara João Carlos Leopoldo Salvador Bibiano Francisco Xavier de Paula Leocádio Miguel Gabriel Rafael Gonzaga de Bragança e Bourbon",
        "Maria Eduarda Silva Santos Oliveira Pereira Costa Rodrigues Almeida Nascimento Mendonça Cavalcanti",
        "João Pedro Almeida Carvalho Ribeiro Lima Ferreira Duarte Pinto Moreira Rocha Teixeira",
        "Ana Clara Mendonça Castro Dias Barbosa Martins Nogueira Cunha Freitas Miranda",
        "Carlos Eduardo Lima Souza Costa Santos Oliveira Rodrigues Pereira Almeida Carvalho Ribeiro",
        "Ana Silva",
        "Bruno Costa",
        "Carla Santos",
        "Daniel Oliveira",
        "Eduarda Lima",
        "Fernanda Cristina Costa Pereira Silva Santos Oliveira Rodrigues Almeida Carvalho Ribeiro Lima",
        "Ricardo Augusto Souza Nogueira Cunha Freitas Miranda Castro Dias Barbosa Martins",
        "Juliana Beatriz Alves Martins Nogueira Cunha Freitas Miranda Castro Dias Barbosa",
        "Lucas Gabriel Mendes Ferreira Duarte Pinto Moreira Rocha Teixeira Almeida Carvalho",
        "Patrícia Isabela Gomes Rodrigues Almeida Carvalho Ribeiro Lima Ferreira Duarte Pinto",
        "Fernando Alves",
        "Gabriela Rocha",
        "Henrique Dias",
        "Isabela Martins",
        "João Barbosa"
    ])


    def marcar_presenca(presenca, falta):
        def func(e):
            if e.control == presenca and presenca.value:
                falta.value = False
            elif e.control == falta and falta.value:
                presenca.value = False
            page.update()
        return func


    linhas = [cabecalho]


    for aluno in alunos:
        presenca_cb = ft.Checkbox(
            label="Presente",
            active_color=ft.Colors.GREEN,
            check_color=ft.Colors.WHITE,
            fill_color=ft.Colors.GREEN,
            label_style=ft.TextStyle(color=ft.Colors.BLACK),
        )


        falta_cb = ft.Checkbox(
            label="Faltou",
            active_color=ft.Colors.RED,
            check_color=ft.Colors.WHITE,
            fill_color=ft.Colors.RED,
            label_style=ft.TextStyle(color=ft.Colors.BLACK),
        )


        observacao_tf = ft.TextField(
            hint_text="Observações...",
            border="",
            multiline=False,
            text_size=14,
            content_padding=ft.padding.symmetric(horizontal=10, vertical=5),
            text_align=ft.TextAlign.LEFT,
            color=ft.Colors.BLACK87,
            bgcolor=ft.Colors.GREY_100,
            cursor_color=ft.Colors.BLACK,
        )


        presenca_checkboxes.append(presenca_cb)
        falta_checkboxes.append(falta_cb)
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
                    ft.Container(ft.Row([presenca_cb, falta_cb], spacing=20), expand=1, alignment=ft.alignment.center),
                    ft.Container(observacao_tf, expand=2, alignment=ft.alignment.center_left, padding=10),
                ],
                expand=True,
            ),
            padding=15,
            border_radius=10,
            bgcolor=ft.Colors.GREY_200,
            margin=ft.margin.only(bottom=8),
        )
        presenca_cb.on_change = marcar_presenca(presenca_cb, falta_cb)
        falta_cb.on_change = marcar_presenca(presenca_cb, falta_cb)
        linhas.append(linha)


    container_principal = ft.Container(
        ft.Column(controls=linhas, spacing=10, scroll=ft.ScrollMode.AUTO, expand=True),
        expand=True,
    )


    layout_principal = ft.Column(
        [
            ft.Container(content=texto, padding=20, alignment=ft.alignment.center),
            ft.Divider(height=10),
            ft.Row([botao_tema, botao_calendario, texto_data], alignment="center", spacing=20),
            container_principal,
            ft.Divider(height=15),
            ft.Row([botao_reset, botao_salvar], alignment="end", spacing=20),
           
        ],
        expand=True,
    )


    page.add(layout_principal)




ft.app(target=main)



