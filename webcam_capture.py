"""
webcam_capture.py — захват изображения с веб-камеры.
"""

import cv2

def capture_from_webcam():
    """
    Делает снимок с первой доступной веб-камеры.

    Returns:
        np.ndarray: изображение в формате BGR.

    Raises:
        RuntimeError: если невозможно подключиться к камере.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError(
            "Веб-камера недоступна. Проверьте:\n"
            "- Подключение камеры\n"
            "- Разрешения доступа\n"
            "- Занятость другим приложением"
        )

    # Делаем несколько кадров для инициализации
    for _ in range(5):
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        raise RuntimeError("Не удалось получить изображение с камеры")

    return frame