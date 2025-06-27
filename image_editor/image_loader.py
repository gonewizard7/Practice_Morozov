"""
Загрузка изображений с диска.
"""
import cv2
from utils import cv_to_pil

def load_image(file_path):
    """
    Загружает изображение с заданного пути.

    Args:
        file_path (str): путь к изображению

    Returns:
        tuple: (PIL.Image, np.ndarray) изображение

    Raises:
        ValueError: если изображение не загружено
    """
    image = cv2.imread(file_path)
    if image is None:
        raise ValueError(f"Не удалось загрузить: {file_path}")
    pil_image = cv_to_pil(image)
    return pil_image, image
