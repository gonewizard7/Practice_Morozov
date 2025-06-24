"""
image_loader.py — загрузка изображений с диска.
"""

import cv2
from utils import cv_to_pil

def load_image(file_path):
    """
    Загружает изображение с заданного пути.

    Parameters:
        file_path (str): путь к изображению.

    Returns:
        tuple: (PIL.Image, np.ndarray) - изображение в формате PIL и оригинал в формате BGR.

    Raises:
        FileNotFoundError: если файл не найден.
        ValueError: если изображение не удалось прочитать.
    """
    image = cv2.imread(file_path)
    if image is None:
        raise ValueError(f"Невозможно прочитать изображение по пути: {file_path}")
    pil_image = cv_to_pil(image)
    return pil_image, image
