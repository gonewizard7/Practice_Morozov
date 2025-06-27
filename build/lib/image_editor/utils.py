"""
Вспомогательные функции.
"""
import cv2
from PIL import Image
import numpy as np

def cv_to_pil(image):
    """
    Конвертирует OpenCV изображение в PIL формат.

    Args:
        image (np.ndarray): изображение BGR

    Returns:
        PIL.Image: изображение RGB

    Raises:
        ValueError: если изображение пустое
    """
    if image is None or image.size == 0:
        raise ValueError("Пустое изображение")
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb_image)

def validate_coordinates(image, *coords):
    """
    Проверяет корректность координат.

    Args:
        image (np.ndarray): изображение
        *coords: координаты для проверки

    Raises:
        ValueError: если координаты вне изображения
    """
    height, width = image.shape[:2]
    for i, coord in enumerate(coords):
        if i % 2 == 0:  # X координаты
            if coord < 0 or coord >= width:
                raise ValueError(f"Координата X ({coord}) вне диапазона")
        else:  # Y координаты
            if coord < 0 or coord >= height:
                raise ValueError(f"Координата Y ({coord}) вне диапазона")

def get_image_size(image):
    """
    Возвращает размеры изображения.

    Args:
        image: изображение (np.ndarray или PIL.Image)

    Returns:
        tuple: (ширина, высота)
    """
    if isinstance(image, np.ndarray):
        height, width = image.shape[:2]
        return width, height
    elif isinstance(image, Image.Image):
        return image.size
    return None
