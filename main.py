import base64
from random import random

import flet as ft
from flet import FilePicker, FilePickerResultEvent
from PIL import Image, ImageFilter
import os
from filters import *
from interface_func import *
from datetime import datetime

# image_history = []  # Массив для хранения всех изменений изображения
# selected_image = None  # Переменная для хранения выбранного изображения
# current_state = -1  # Индекс текущего состояния изображения
# temp_image_history = []

def main(page: ft.Page):
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

    # Выпадающий список форматов сохранения
    format_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("PNG"),
            ft.dropdown.Option("JPG"),
            ft.dropdown.Option("JPEG")
        ]
    )
    # Диалоговое окно выбора файла
    file_picker = FilePicker(on_result=lambda e: pick_files_result(e, undo_button, redo_button, image_container, page, history_container))
    # Диалоговое окно сохранения файла
    save_file_picker = FilePicker(on_result=lambda e: save_file_result(e, format_dropdown))

    # Кнопка "Открыть файл"
    open_file_button = ft.ElevatedButton(text="Открыть файл", on_click=lambda _: file_picker.pick_files(
        allow_multiple=False,
        allowed_extensions=["png", "jpg", "jpeg"]
    ))

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
    # Кнопка "Сохранить"
    save_button = ft.ElevatedButton(
        text="Сохранить", on_click=lambda _: show_format_dialog(page, dropdown, file_picker))

    # Кнопка "Очистить поле"
    clear_button = ft.ElevatedButton(
        text="Очистить поле", on_click=lambda _: show_clear_confirmation(page, image_container, history_container))

    # Остальные кнопки и элементы
    undo_button = ft.ElevatedButton(
        text="Отменить", disabled=True)
    undo_button.on_click = lambda _: undo_button_clicked(image_container, history_container, page, undo_button, redo_button)
    redo_button = ft.ElevatedButton(
        text="Повторить", disabled=True)
    redo_button.on_click = lambda _: redo_button_clicked(image_container, history_container, page, undo_button, redo_button)
    slider = ft.Slider(min=0, max=100, divisions=10, label="{value}")
    dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Фильтр Гаусса"),
            ft.dropdown.Option("Autolevel"),
        ],
        on_change=lambda e: dropdown_changed(e, slider, page)
    )
    

    apply_button = ft.ElevatedButton(
        text="Применить", on_click = lambda e: apply_button_clicked(e, dropdown, image_container, history_container, page, undo_button, redo_button, slider))


   
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
            [button_row, edit_options_row, image_container, history_container],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        file_picker,
        save_file_picker
    )

    
ft.app(target=main)
