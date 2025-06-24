import cv2
from PIL import Image


def cv_to_pil(image):
    """
    Конвертирует изображение из BGR (OpenCV) в RGB (PIL).

    Parameters:
        image (np.ndarray): изображение BGR.

    Returns:
        PIL.Image: изображение в формате PIL.
    """
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb_image)
