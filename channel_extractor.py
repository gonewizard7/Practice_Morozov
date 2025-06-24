import cv2
import numpy as np


def extract_channel(image, channel):
    """
    Извлекает указанный цветовой канал из изображения.

    Parameters:
        image (np.ndarray): исходное изображение в формате BGR.
        channel (str): 'r', 'g' или 'b'.

    Returns:
        np.ndarray: изображение с выделенным каналом.
    """
    b, g, r = cv2.split(image)
    zeros = np.zeros_like(b)

    if channel == 'r':
        return cv2.merge([zeros, zeros, r])
    elif channel == 'g':
        return cv2.merge([zeros, g, zeros])
    elif channel == 'b':
        return cv2.merge([b, zeros, zeros])
    else:
        raise ValueError("Неверный канал. Используйте 'r', 'g' или 'b'.")
