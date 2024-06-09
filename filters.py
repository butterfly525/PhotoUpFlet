import ctypes
import numpy as np
from PIL import Image, ImageFilter
import flet as ft

def apply_gaussian_filter(image, slider: ft.Slider):
    rgb_image = image.convert('RGB')
    rgb_array = np.array(rgb_image)
    # Загрузка DLL
    my_dll = ctypes.CDLL('.\GaussianFilter.dll')
    # Определение сигнатур функций
    my_dll.apply_gaussian_filter.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double]
    my_dll.apply_gaussian_filter.restype = None
    # Вызов функции из DLL
    # Применяем фильтр Гаусса
    print(rgb_array.shape[2])
    my_dll.apply_gaussian_filter(rgb_array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)), rgb_array.shape[1], rgb_array.shape[0], rgb_array.shape[2], float(slider.value))
    image = Image.fromarray(rgb_array)
    return image

def apply_autolevel_filter(image):
    rgb_image = image.convert('RGB')
    rgb_array = np.array(rgb_image)
    # Загрузка DLL
    my_dll = ctypes.CDLL('.\Autolevel_Filter.dll')
    # Определение сигнатур функций
    my_dll.apply_auto_levels_filter.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int, ctypes.c_int]
    my_dll.apply_auto_levels_filter.restype = None
    # Вызов функции из DLL
    # Применяем фильтр autolevel
    my_dll.apply_auto_levels_filter(rgb_array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)), rgb_array.shape[1], rgb_array.shape[0], rgb_array.shape[2])
    image = Image.fromarray(rgb_array)
    return image
