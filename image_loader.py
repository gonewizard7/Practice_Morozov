import cv2


def load_image(file_path):
    """
    Загружает изображение с заданного пути.

    Parameters:
        file_path (str): путь к изображению.

    Returns:
        np.ndarray: изображение в формате BGR.

    Raises:
        FileNotFoundError: если файл не найден.
        ValueError: если изображение не удалось прочитать.
    """
    image = cv2.imread(file_path)
    if image is None:
        raise ValueError("Невозможно прочитать изображение. Возможно, файл повреждён.")
    return image
