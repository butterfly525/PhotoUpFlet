import base64
import flet as ft
from flet import FilePicker, FilePickerResultEvent
from PIL import Image, ImageFilter
import io
import ctypes
import numpy as np
image_history = []  # Массив для хранения всех изменений изображения
selected_image = None  # Переменная для хранения выбранного изображения
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
            update_history_container()
            page.update()
    # Функция для показа диалогового окна выбора формата сохранения

    def show_format_dialog():
        if selected_image:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Выберите формат сохранения"),
                content=format_dropdown,
                actions=[
                    ft.TextButton("Отмена", on_click=close_dialog),
                    ft.TextButton(
                        "Сохранить", on_click=lambda _: show_save_file_dialog())
                ]
            )
            page.dialog.open = True
            page.update()

        # Функция для показа диалогового окна выбора места сохранения файла

    def show_save_file_dialog():
        close_dialog()
        save_file_picker.save_file(
            file_name=f"image.{format_dropdown.value.lower()}",
            allowed_extensions=[format_dropdown.value.lower()]
        )

        # Функция для обработки сохранения файла

    def save_file_result(e: FilePickerResultEvent):
        global selected_image
        if e.path and selected_image:
            # Получаем выбранный формат сохранения
            chosen_format = format_dropdown.value.lower()
            # Проверяем, является ли выбранный формат JPEG или JPG
            if chosen_format in ['jpeg', 'jpg']:
                # Конвертируем изображение в режим RGB, если оно в режиме RGBA
                if selected_image.mode == 'RGBA':
                    selected_image = selected_image.convert('RGB')
            selected_image.save(e.path)

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
        global selected_image
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

    def undo_button_clicked(e):
        global selected_image, image_history, current_state
        if current_state > 0:
            current_state -= 1
            selected_image = image_history[current_state]
            # Преобразование изображения в байты
            img_byte_arr = io.BytesIO()
            selected_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            # Кодирование байтов в base64
            img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
            # Отображение изображения в image_container
            image_container.content = ft.Image(src_base64=img_base64)
            update_history_container()
            page.update()
        update_button_states()

    def redo_button_clicked(e):
        global selected_image, image_history, current_state
        if current_state < len(image_history) - 1:
            current_state += 1
            selected_image = image_history[current_state]
            # Преобразование изображения в байты
            img_byte_arr = io.BytesIO()
            selected_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            # Кодирование байтов в base64
            img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
            # Отображение изображения в image_container
            image_container.content = ft.Image(src_base64=img_base64)
            update_history_container()
            page.update()
        update_button_states()

    def update_button_states():
        undo_button.disabled = current_state == 0
        redo_button.disabled = current_state == len(image_history) - 1
        page.update()

    def update_history_container():
        history_container.content.controls = []
        for i, image in enumerate(image_history):
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
            image_widget = ft.Image(src_base64=img_base64)
            container = ft.Container(
                content=image_widget,
                border=ft.border.all(
                    2, ft.colors.BLUE) if i == current_state else None,
                border_radius=ft.border_radius.all(10),
            )
            history_container.content.controls.append(container)
        page.update()

    def apply_gaussian_filter():
        global selected_image, current_state, image_history
        if selected_image:
            selected_image = selected_image.filter(
                ImageFilter.GaussianBlur(radius=slider.value))
            image_history.append(selected_image.copy())
            current_state += 1
            img_byte_arr = io.BytesIO()
            selected_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            # Кодирование байтов в base64
            img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')

            # Отображение изображения в image_container
            image_container.content = ft.Image(src_base64=img_base64)
            update_history_container()
            page.update()
        update_button_states()

    def apply_dll():
        global current_state, image_history
        rgb_image = image_history[current_state].convert('RGB')
        rgb_array = np.array(rgb_image)
        # Загрузка DLL
        my_dll = ctypes.CDLL('.\Dll1.dll')

        # Определение сигнатур функций
        my_dll.process_image.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int, ctypes.c_int]
        my_dll.process_image.restype = None

        # Вызов функции из DLL
        my_dll.process_image(rgb_array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)), rgb_array.shape[1], rgb_array.shape[0], rgb_array.shape[2])
        image = Image.fromarray(rgb_array)
        image_history.append(image.copy())
        current_state += 1
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        # Кодирование байтов в base64
        img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')

        # Отображение изображения в image_container
        image_container.content = ft.Image(src_base64=img_base64)
        update_history_container()
        page.update()
        update_button_states()
    def apply_button_clicked(e):
        global image_history
        if dropdown.value == "Фильтр Гаусса":
            if current_state < len(image_history) - 1:
                image_history = image_history[:current_state + 1]
            apply_gaussian_filter()
        elif dropdown.value == "dll":
            # Добавьте здесь обработчики для других фильтров
            apply_dll()
        update_button_states()

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
    undo_button = ft.ElevatedButton(
        text="Отменить", on_click=undo_button_clicked, disabled=True)
    redo_button = ft.ElevatedButton(
        text="Повторить", on_click=redo_button_clicked, disabled=True)

    dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Фильтр Гаусса"),
            ft.dropdown.Option("dll"),
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
    # Контейнер для отображения истории изменений изображения
    history_container = ft.Container(
        height=220,
        width=page.window_width,
        bgcolor=None,
        content=ft.GridView(
            auto_scroll=True,
            expand=True,
            run_spacing=10,
            max_extent=300,
            child_aspect_ratio=1.0,
            controls=[],
            horizontal=True
        ),
    )
    # Добавление виджетов на страницу в центрированный столбец
    page.add(
        ft.Column(
            [button_row, edit_options_row, image_container, history_container],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        file_picker,
        save_file_picker
    )


ft.app(target=main)
