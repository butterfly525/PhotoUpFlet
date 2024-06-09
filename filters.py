import ctypes
import numpy as np
from PIL import Image, ImageFilter
import flet as ft
import cv2
def apply_gaussian_filter(image, slider: ft.Slider):
    rgb_image = image.convert('RGB')
    rgb_array = np.array(rgb_image)
    # Загрузка DLL
    my_dll = ctypes.CDLL('.\DLLs\GaussianFilter.dll')
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
    my_dll = ctypes.CDLL('.\DLLs\Autolevel_Filter.dll')
    # Определение сигнатур функций
    my_dll.apply_auto_levels_filter.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int, ctypes.c_int]
    my_dll.apply_auto_levels_filter.restype = None
    # Вызов функции из DLL
    # Применяем фильтр autolevel
    my_dll.apply_auto_levels_filter(rgb_array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)), rgb_array.shape[1], rgb_array.shape[0], rgb_array.shape[2])
    image = Image.fromarray(rgb_array)
    return image


# def apply_SSR_filter(image, sg1):
#     rgb_image = image.convert('RGB')
#     rgb_array = np.array(rgb_image)
#     gray = cv2.cvtColor(rgb_array, cv2.COLOR_BGR2GRAY)
#     im = self.singleScaleRetinex_core(gray, sg1)
#     out_image = self.scaleG(im)
#     gray_threei = cv2.merge([gray, gray, gray])
#     gray_threeO = cv2.merge([out_image, out_image, out_image])
#     retinexR = rgb_array * gray_threeO / (gray_threei + 0.01)
#     retinex = np.array(retinexR, dtype=np.uint8)
#     return retinex
