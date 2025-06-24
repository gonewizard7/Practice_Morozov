"""
utils.py — вспомогательные функции.
"""

import cv2
from PIL import Image

def cv_to_pil(image):
    """
    Конвертирует изображение из BGR (OpenCV) в RGB (PIL).

    Parameters:
        image (np.ndarray): изображение BGR.

    Returns:
        PIL.Image: изображение в формате PIL.

    Raises:
        ValueError: если изображение пустое
    """
    if image is None or image.size == 0:
        raise ValueError("Пустое изображение")
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb_image)
