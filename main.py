import flet as ft
from flet import FilePicker, FilePickerResultEvent
from PIL import Image, ImageFilter


image_history = []  # Массив для хранения всех изменений изображения
    
    # Переменная для хранения выбранного изображения
selected_image = None
    # Функция для обработки выбора файла
current_state = -1  # Индекс текущего состояния изображения

def main(page: ft.Page):
    
    
    def pick_files_result(e: FilePickerResultEvent):
        global image_history, selected_image, current_state
        selected_files = e.files
        if selected_files:
            selected_image = Image.open(selected_files[0].path)
            image_history.append(selected_image.copy())
            current_state += 1
            image_container.content = ft.Image(src=selected_files[0].path)
            page.update()

    # Функция для обработки сохранения файла
    def save_file_result(e: FilePickerResultEvent):
        if e.path and selected_image:
            with open(selected_image, "rb") as f:
                data = f.read()
            with open(e.path, "wb") as f:
                f.write(data)

    # Функция для показа диалогового окна выбора формата сохранения
    def show_format_dialog():
        if selected_image:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Выберите формат сохранения"),
                content=format_dropdown,
                actions=[
                    ft.TextButton("Отмена", on_click=close_dialog),
                    ft.TextButton("Сохранить", on_click=lambda _: save_file())
                ]
            )
            page.dialog.open = True
            page.update()

    # Функция для сохранения файла с выбранным форматом
    def save_file():
        if selected_image:
            close_dialog()
            save_file_picker.save_file(
                file_name=f"image.{format_dropdown.value.lower()}",
                allowed_extensions=[format_dropdown.value.lower()]
            )

    # Функция для закрытия диалогового окна
    def close_dialog(e=None):
        page.dialog.open = False
        page.update()

    # Функция для показа диалогового окна подтверждения очистки поля
    def show_clear_confirmation():
        if selected_image:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Подтвердите очистку поля"),
                content=ft.Image(src=selected_image),
                actions=[
                    ft.TextButton("Отмена", on_click=close_dialog),
                    ft.TextButton("Очистить", on_click=lambda _: clear_field())
                ]
            )
            page.dialog.open = True
            page.update()

    # Функция для очистки поля с изображением
    def clear_field():
        selected_image = None
        image_container.content = None
        close_dialog()
        page.update()

    def dropdown_changed(e):
        if e.control.value == "Фильтр Гаусса":
            slider.min = 0
            slider.max = 10
        else:
            # Установите здесь значения по умолчанию или для других фильтров
            slider.min = 0
            slider.max = 100
        page.update()

    def apply_gaussian_filter():
        global selected_image, current_state, image_history
        if selected_image:
            selected_image = selected_image.filter(
                ImageFilter.GaussianBlur(radius=slider.value))
            image_history.append(selected_image.copy())
            current_state += 1
             # Проверяем, является ли изображение в режиме RGBA
            if selected_image.mode == 'RGBA':
                # Конвертируем изображение в режим RGB
                rgb_image = selected_image.convert('RGB')
                # Обновляем контент контейнера с конвертированным изображением
                image_container.content = ft.Image(src=rgb_image.tobytes())
                
            else:
                # Если изображение уже в режиме RGB, просто обновляем контент контейнера
                image_container.content = ft.Image(src=selected_image.tobytes())
            page.update()
            
    def apply_button_clicked(e):
        if dropdown.value == "Фильтр Гаусса":
            apply_gaussian_filter()
        else:
            # Добавьте здесь обработчики для других фильтров
            pass
    
    def undo_button_clicked(e):
        global selected_image, image_history, current_state
        if current_state > 0:
            current_state -= 1
            selected_image = image_history[current_state]
            selected_image.save("undo_image.jpg")
            image_container.content = ft.Image(src="undo_image.jpg")
            page.update()

    def redo_button_clicked(e):
        global selected_image, image_history, current_state
        if current_state < len(image_history) - 1:
            current_state += 1
            selected_image = image_history[current_state]
            selected_image.save("redo_image.jpg")
            image_container.content = ft.Image(src="redo_image.jpg")
            page.update()

    page.title = "Редактор изображений"

    # Устанавливаем окно приложения во весь экран
    page.window_maximized = True

    # Контейнер для отображения области картинки
    image_container = ft.Container(
        width=800,
        height=600,
        bgcolor=None,
        alignment=ft.alignment.center
    )


    # Диалоговое окно выбора файла
    file_picker = FilePicker(on_result=pick_files_result)
    # Диалоговое окно сохранения файла
    save_file_picker = FilePicker(on_result=save_file_result)

    # Кнопка "Открыть файл"
    open_file_button = ft.ElevatedButton(text="Открыть файл", on_click=lambda _: file_picker.pick_files(
        allow_multiple=False,
        allowed_extensions=["png", "jpg", "jpeg"]
    ))

    # Выпадающий список форматов сохранения
    format_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("PNG"),
            ft.dropdown.Option("JPG"),
            ft.dropdown.Option("JPEG")
        ]
    )

    # Кнопка "Сохранить"
    save_button = ft.ElevatedButton(
        text="Сохранить", on_click=lambda _: show_format_dialog())

    # Кнопка "Очистить поле"
    clear_button = ft.ElevatedButton(
        text="Очистить поле", on_click=lambda _: show_clear_confirmation())

    # Остальные кнопки и элементы
    undo_button = ft.ElevatedButton(text="Отменить", on_click=undo_button_clicked)
    redo_button = ft.ElevatedButton(text="Повторить", on_click=redo_button_clicked)

    dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Фильтр Гаусса"),
            ft.dropdown.Option("Опция 2"),
        ],
        on_change=dropdown_changed
    )
    slider = ft.Slider(min=0, max=100, divisions=10, label="{value}")

    apply_button = ft.ElevatedButton(
        text="Применить", on_click=apply_button_clicked)
    history_slider = ft.Slider(min=0, max=10, divisions=10, label="{value}")

    # Верхняя строка с кнопками
    button_row = ft.Row(
        [open_file_button, save_button, undo_button, redo_button, clear_button],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Строка с опциями редактирования
    edit_options_row = ft.Row(
        [dropdown, slider, apply_button],
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Добавление виджетов на страницу в центрированный столбец
    page.add(
        ft.Column(
            [button_row, edit_options_row, image_container, history_slider],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        file_picker,
        save_file_picker
    )


ft.app(target=main)
