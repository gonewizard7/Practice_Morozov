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
            "Веб-камера недоступна. Возможные причины:\n"
            "- Она не подключена\n"
            "- Используется другим приложением\n"
            "- Нет прав доступа"
        )

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        raise RuntimeError("Ошибка при получении изображения с камеры.")

    return frame
