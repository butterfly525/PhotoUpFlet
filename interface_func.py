import base64
from random import random

import flet as ft
from flet import FilePicker, FilePickerResultEvent
from PIL import Image, ImageFilter
import os
from filters import *
from datetime import datetime

image_history = []  # Массив для хранения всех изменений изображения
selected_image = None  # Переменная для хранения выбранного изображения
current_state = -1  # Индекс текущего состояния изображения
temp_image_history = []


def pick_files_result(e: FilePickerResultEvent, undo_button: ft.ElevatedButton, redo_button: ft.ElevatedButton, image_container: ft.Container, page: ft.Page, history_container: ft.Container):
    global image_history, selected_image, current_state
    selected_files = e.files
    if selected_files:
        if current_state < len(image_history) - 1:
            for i in range(current_state+1, len(image_history)):
                file_path = image_history[i]
                try:
                    os.remove(file_path)
                    print('remove', file_path)
                except OSError as e:
                    print(f"Ошибка при удалении файла: {e.strerror}")

            del image_history[current_state + 1:]
        selected_image = Image.open(selected_files[0].path)

        current_state += 1
        now = datetime.now()
        date_part = now.strftime('%d%m')
        time_part = now.strftime('%H%M%S')

        file_name = f'./temp_files/file_{date_part}_{time_part}.{selected_image.format}'
        selected_image.save(file_name, selected_image.format)
        image_history.append(file_name)

        image_container.content = ft.Image(src=selected_files[0].path)
        update_button_states(undo_button, redo_button, page)
        update_history_container(history_container, page)
        page.update()

# Функция для показа диалогового окна выбора формата сохранения


def show_format_dialog(page: ft.Page, format_dropdown: ft.Dropdown, save_file_picker: FilePicker):
    global selected_image
    if selected_image:
        page.dialog = ft.AlertDialog(
            title=ft.Text("Выберите формат сохранения"),
            content=format_dropdown,
            actions=[
                ft.TextButton("Отмена", on_click=close_dialog(page)),
                ft.TextButton(
                    "Сохранить", on_click=lambda _: show_save_file_dialog(save_file_picker, format_dropdown, page))
            ]
        )
        page.dialog.open = True
        page.update()


def update_button_states(undo_button: ft.ElevatedButton, redo_button: ft.ElevatedButton, page: ft.Page):
    global image_history, current_state
    undo_button.disabled = current_state == 0
    redo_button.disabled = current_state == len(image_history) - 1
    page.update()


def update_history_container(history_container: ft.Container, page: ft.Page):
    global image_history, current_state, selected_image
    history_container.content.controls = []
    if current_state < len(image_history) - 1:
        for i in range(len(image_history[:current_state+1])):
            selected_image = Image.open(image_history[i])
            image_widget = ft.Image(src=image_history[i])
            container = ft.Container(
                content=image_widget,
                border=ft.border.all(
                    2, ft.colors.BLUE) if i == current_state else None,
                border_radius=ft.border_radius.all(10),
            )
            history_container.content.controls.append(container)
    else:
        for i, image in enumerate(image_history):
            selected_image = Image.open(image_history[i])
            image_widget = ft.Image(src=image)
            container = ft.Container(
                content=image_widget,
                border=ft.border.all(
                    2, ft.colors.BLUE) if i == current_state else None,
                border_radius=ft.border_radius.all(10),
            )
            history_container.content.controls.append(container)
    page.update()


def dropdown_changed(e, slider: ft.Slider, page: ft.Page):
    if e.control.value == "Фильтр Гаусса":
        slider.min = 1
        slider.max = 10
        slider.disabled = False
    elif e.control.value == "Autolevel":
        slider.min = 1
        slider.max = 10
        slider.disabled = True
    page.update()

# Функция для показа диалогового окна выбора места сохранения файла


def show_save_file_dialog(save_file_picker: FilePicker, format_dropdown: ft.Dropdown, page: ft.Page):
    close_dialog(page)
    save_file_picker.save_file(
        file_name=f"image.{format_dropdown.value.lower()}",
        allowed_extensions=[format_dropdown.value.lower()]
    )

    # Функция для обработки сохранения файла


def save_file_result(e: FilePickerResultEvent, format_dropdown: ft.Dropdown):
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


def close_dialog(e, page: ft.Page):
    page.dialog.open = False
    page.update()

# Функция для показа диалогового окна подтверждения очистки поля


def show_clear_confirmation(page: ft.Page, image_container: ft.Container, history_container: ft.Container):
    global selected_image
    if selected_image:
        page.dialog = ft.AlertDialog(
            title=ft.Text("Подтвердите очистку поля"),
            content=ft.Image(src=selected_image),
            actions=[
                ft.TextButton("Отмена", on_click=close_dialog(page)),
                ft.TextButton("Очистить", on_click=lambda _: clear_field(image_container, history_container, page))
            ]
        )
        page.dialog.open = True
        page.update()

# Функция для очистки поля с изображением


def clear_field(image_container: ft.Container, history_container: ft.Container, page: ft.Page):
    global selected_image, image_history, current_state
    selected_image = None
    image_container.content = None
    history_container.content.controls = []
    image_history = []
    current_state = -1
    close_dialog(page)
    page.update()


def undo_button_clicked(image_container: ft.Container, history_container: ft.Container, page: ft.Page, undo_button: ft.ElevatedButton, redo_button: ft.ElevatedButton):
    global image_history, current_state, selected_image
    if current_state > 0:
        current_state -= 1
        image_container.content = ft.Image(src=image_history[current_state])
        selected_image = Image.open(image_history[current_state])
    update_history_container(history_container, page)
    update_button_states(undo_button, redo_button, page)
    page.update()


def redo_button_clicked(image_container: ft.Container, history_container: ft.Container, page: ft.Page, undo_button: ft.ElevatedButton, redo_button: ft.ElevatedButton):
    global image_history, current_state, selected_image
    if current_state < len(image_history) - 1:
        current_state += 1
        image_container.content = ft.Image(src=image_history[current_state])
        selected_image = Image.open(image_history[current_state])
    update_history_container(history_container, page)
    update_button_states(undo_button, redo_button, page)
    page.update()


def apply_button_clicked(e, dropdown: ft.Dropdown, image_container: ft.Container, history_container: ft.Container, page: ft.Page, undo_button: ft.ElevatedButton, redo_button: ft.ElevatedButton, slider: ft.Slider):
    global current_state, image_history, selected_image
    if current_state < len(image_history) - 1:
        for i in range(current_state + 1, len(image_history)):
            file_path = image_history[i]
            try:
                os.remove(file_path)
                print('remove', file_path)
            except OSError as e:
                print(f"Ошибка при удалении файла: {e.strerror}")
        del image_history[current_state + 1:]
    image = Image.open(image_history[current_state])
    format_img = image.format
    if dropdown.value == "Фильтр Гаусса":
        image = apply_gaussian_filter(image, slider)
    elif dropdown.value == "Autolevel":
        image = apply_autolevel_filter(image)
    current_state += 1
    now = datetime.now()
    date_part = now.strftime('%d%m')
    time_part = now.strftime('%H%M%S')
    file_name = f'./temp_files/file_{date_part}_{time_part}.{selected_image.format}'
    image.save(file_name, format_img)
    image_history.append(file_name)
    image_container.content = ft.Image(src=image_history[current_state])
    selected_image = Image.open(image_history[current_state])
    update_button_states(undo_button, redo_button, page)
    update_history_container(history_container, page)
    page.update()
