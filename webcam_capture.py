"""
Захват изображения с веб-камеры.
"""
import cv2

def capture_from_webcam():
    """
    Делает снимок с веб-камеры.

    Returns:
        np.ndarray: изображение BGR

    Raises:
        RuntimeError: при ошибке камеры
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Камера недоступна")

    for _ in range(5):
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        raise RuntimeError("Ошибка захвата изображения")

    return frame
