import ctypes
import numpy as np
from PIL import Image, ImageFilter
import flet as ft
import cv2
from numpy import nonzero, zeros, float32

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

def apply_histogram_equalization(image):
    rgb_image = image.convert('RGB')
    rgb_array = np.array(rgb_image)
    # Загрузка DLL
    my_dll = ctypes.CDLL('.\DLLs\Histogram_equalization_algorithm.dll')
    # Определение сигнатур функций
    my_dll.apply_histogram_equalization.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int, ctypes.c_int]
    my_dll.apply_histogram_equalization.restype = None
    # Вызов функции из DLL
    # Применяем фильтр autolevel
    my_dll.apply_histogram_equalization(rgb_array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)), rgb_array.shape[1], rgb_array.shape[0], rgb_array.shape[2])
    image = Image.fromarray(rgb_array)
    return image


def apply_clahe(image, slider: ft.Slider):
    rgb_image = image.convert('RGB')
    rgb_array = np.array(rgb_image)
    # Загрузка DLL
    my_dll = ctypes.CDLL('.\DLLs\CLAHE.dll')
    # Определение сигнатур функций
    my_dll.apply_clahe_filter.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int, ctypes.c_int]
    my_dll.apply_clahe_filter.restype = None
    # Вызов функции из DLL
    # Применяем фильтр autolevel
    my_dll.apply_clahe_filter(rgb_array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)), rgb_array.shape[1], rgb_array.shape[0], rgb_array.shape[2])
    image = Image.fromarray(rgb_array)
    return image

def apply_artifact_removal(image, slider: ft.Slider):
    rgb_image = image.convert('RGB')
    rgb_array = np.array(rgb_image)
    # Загрузка DLL
    my_dll = ctypes.CDLL('.\DLLs\ArtifactRemoval.dll')
    # Определение сигнатур функций
    my_dll.apply_artifact_removal_filter.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    my_dll.apply_artifact_removal_filter.restype = None
    # Вызов функции из DLL
    # Применяем фильтр autolevel
    my_dll.apply_artifact_removal_filter(rgb_array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)), rgb_array.shape[1], rgb_array.shape[0], rgb_array.shape[2], int(slider.value))
    image = Image.fromarray(rgb_array)
    return image

def apply_contrast_enhancement(image):
    rgb_image = image.convert('RGB')
    rgb_array = np.array(rgb_image)
    # Загрузка DLL
    my_dll = ctypes.CDLL('.\DLLs\BalanceContrastEnhancementTechnique.dll')
    # Определение сигнатур функций
    my_dll.apply_contrast_enhancement_filter.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int, ctypes.c_int]
    my_dll.apply_contrast_enhancement_filter.restype = None
    # Вызов функции из DLL
    # Применяем фильтр autolevel
    my_dll.apply_contrast_enhancement_filter(rgb_array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)), rgb_array.shape[1], rgb_array.shape[0], rgb_array.shape[2])
    image = Image.fromarray(rgb_array)
    print(type(image))
    return image

# def apply_contrast_enhancement(image, slider):
    # rgb_image = image.convert('RGB')
    # rgb_array = np.array(rgb_image)
    # # Загрузка DLL
    # my_dll = ctypes.CDLL('.\DLLs\SingleScaleRetinex.dll')
    # # Определение сигнатур функций
    # my_dll.apply_ssr_filter.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_float]
    # my_dll.apply_ssr_filter.restype = None
    # # Вызов функции из DLL
    # # Применяем фильтр autolevel
    # my_dll.apply_ssr_filter(rgb_array.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8)), rgb_array.shape[1], rgb_array.shape[0], rgb_array.shape[2], float(slider.value))
    # image = Image.fromarray(rgb_array)
    # return image
    #SSR
 
def SSR(img, slider):
    sigma = slider.value
    # Convert PIL Image to OpenCV format
    img = np.array(img)
    
    # Convert to float32
    img = img.astype(np.float32) / 255.0

    # Split image into its channels
    img_channels = cv2.split(img)

    # Apply SSR to each channel
    ssr_channels = []
    for channel in img_channels:
        # Add a small constant to avoid taking the log of zero
        log_R = np.log10(channel + 1e-6)

        # Convert sigma to float
        sigma = float(sigma)

        # Compute the Gaussian blur
        gaussian_blur = cv2.GaussianBlur(log_R, (0, 0), sigma)

        # Compute the SSR
        ssr = log_R - gaussian_blur

        # Normalize the SSR
        ssr = (ssr - ssr.min()) / (ssr.max() - ssr.min())

        # Add to the list of SSR channels
        ssr_channels.append(ssr)

    # Merge the SSR channels
    img_ssr = cv2.merge(ssr_channels)

    # Clip the values to the valid range
    img_ssr = np.clip(img_ssr, 0, 1)

    # Convert back to uint8 and PIL Image
    img_ssr = (img_ssr * 255).astype(np.uint8)
    img_ssr = Image.fromarray(img_ssr)
    return img_ssr


def MSR(img, slider):
    sigma_list=[15, 80, slider.value]
    # Convert PIL Image to OpenCV format
    img = np.array(img)

    # Convert to float32
    img = img.astype(np.float32) / 255.0

    # Split image into its channels
    img_channels = cv2.split(img)

    # Apply MSR to each channel
    msr_channels = []
    for channel in img_channels:
        # Compute the log of the image
        log_R = np.log10(channel + 1e-6)

        # Compute the MSR
        msr = np.zeros_like(log_R)
        for sigma in sigma_list:
            # Convert sigma to float
            sigma = float(sigma)

            # Compute the Gaussian blur
            gaussian_blur = cv2.GaussianBlur(log_R, (0, 0), sigma)

            # Add to the MSR
            msr += log_R - gaussian_blur

        # Normalize the MSR
        msr = (msr - msr.min()) / (msr.max() - msr.min())

        # Add to the list of MSR channels
        msr_channels.append(msr)

    # Merge the MSR channels
    img_msr = cv2.merge(msr_channels)

    # Convert back to uint8 and PIL Image
    img_msr = np.clip(img_msr, 0, 1)
    img_msr = (img_msr * 255).astype(np.uint8)
    img_msr = Image.fromarray(img_msr)

    return img_msr