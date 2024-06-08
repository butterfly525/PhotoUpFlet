from flet import FilePicker, FilePickerResultEvent
from PIL import Image, ImageFilter

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
                    ft.TextButton("Сохранить", on_click=lambda _: show_save_file_dialog())
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