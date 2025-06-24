"""
channel_extractor.py — выделение цветового канала изображения.
"""

import numpy as np
import cv2
from PIL import Image

def extract_channel(cv_img, channel):
    """
    Возвращает изображение с одним из каналов: 'r', 'g' или 'b'.

    :param cv_img: изображение как numpy.ndarray (формат BGR)
    :param channel: строка 'r', 'g' или 'b'
    :return: PIL.Image только с указанным каналом
    """
    channel_map = {'b': 0, 'g': 1, 'r': 2}

    if channel not in channel_map:
        raise ValueError("Неверный канал. Используйте 'r', 'g' или 'b'.")

    # Создаем копию изображения и обнуляем другие каналы
    extracted = np.zeros_like(cv_img)
    extracted[:, :, channel_map[channel]] = cv_img[:, :, channel_map[channel]]

    # Конвертируем в RGB для PIL
    rgb_image = cv2.cvtColor(extracted, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb_image)
