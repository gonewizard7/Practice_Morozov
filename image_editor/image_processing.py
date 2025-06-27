"""
Дополнительные операции над изображениями.
"""
import cv2
import numpy as np
from image_editor.utils import validate_coordinates

def crop_image(image, x1, y1, x2, y2):
    """
    Обрезает изображение по координатам.

    Args:
        image (np.ndarray): исходное изображение
        x1, y1 (int): левый верхний угол
        x2, y2 (int): правый нижний угол

    Returns:
        np.ndarray: обрезанное изображение

    Raises:
        ValueError: при неверных координатах
    """
    validate_coordinates(image, x1, y1, x2, y2)
    if x1 >= x2 or y1 >= y2:
        raise ValueError("Координаты: x1 < x2, y1 < y2")
    return image[y1:y2, x1:x2]

def adjust_brightness(image, value):
    """
    Регулирует яркость изображения.

    Args:
        image (np.ndarray): исходное изображение
        value (int): значение яркости (-255 до 255)

    Returns:
        np.ndarray: изображение с измененной яркостью

    Raises:
        ValueError: при неверном значении
    """
    if not -255 <= value <= 255:
        raise ValueError("Яркость должна быть -255..255")

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    v = np.clip(v, 0, 255)
    merged = cv2.merge([h, s, v])
    return cv2.cvtColor(merged, cv2.COLOR_HSV2BGR)

def draw_line(image, x1, y1, x2, y2, thickness):
    """
    Рисует зеленую линию на изображении.

    Args:
        image (np.ndarray): исходное изображение
        x1, y1 (int): начало линии
        x2, y2 (int): конец линии
        thickness (int): толщина линии

    Returns:
        np.ndarray: изображение с линией

    Raises:
        ValueError: при неверных параметрах
    """
    validate_coordinates(image, x1, y1, x2, y2)
    if thickness <= 0:
        raise ValueError("Толщина линии должна быть > 0")

    result = image.copy()
    color = (0, 255, 0)  # Зеленый цвет
    cv2.line(result, (x1, y1), (x2, y2), color, thickness)
    return result
