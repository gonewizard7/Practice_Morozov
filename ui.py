"""
ui.py

Модуль пользовательского интерфейса приложения.
Реализует окно с кнопками: загрузка изображения, снимок с камеры и отображение цветовых каналов.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from image_loader import load_image
from webcam_capture import capture_from_webcam
from channel_extractor import extract_channel
from utils import cv_to_pil

def run_app():
    """
    Запускает основное окно приложения.
    """
    current_image = None
    current_image_cv = None

    def update_image_display(pil_img):
        """
        Обновляет изображение, отображаемое в интерфейсе.

        :param pil_img: PIL.Image для отображения
        """
        max_width = 800
        max_height = 600
        img_width, img_height = pil_img.size

        if img_width > max_width or img_height > max_height:
            ratio = min(max_width / img_width, max_height / img_height)
            new_size = (int(img_width * ratio), int(img_height * ratio))
            pil_img = pil_img.resize(new_size, Image.LANCZOS)

        img_tk = ImageTk.PhotoImage(pil_img)
        image_label.config(image=img_tk)
        image_label.image = img_tk

    def on_load_image():
        """
        Загружает изображение с диска.
        """
        nonlocal current_image, current_image_cv
        path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.png *.jpg *.jpeg")]
        )
        if not path:
            return
        try:
            pil_img, cv_img = load_image(path)
            current_image = pil_img
            current_image_cv = cv_img
            update_image_display(pil_img)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def on_capture():
        """
        Делает снимок с веб-камеры.
        """
        nonlocal current_image, current_image_cv
        try:
            cv_img = capture_from_webcam()
            pil_img = cv_to_pil(cv_img)
            current_image_cv = cv_img
            current_image = pil_img
            update_image_display(pil_img)
        except Exception as e:
            messagebox.showerror("Ошибка камеры", str(e))

    def on_show_channel(channel):
        """
        Показывает выбранный цветовой канал (R, G или B).

        :param channel: Строка: 'R', 'G' или 'B'
        """
        nonlocal current_image_cv
        if current_image_cv is None:
            messagebox.showwarning("Нет изображения", "Сначала загрузите изображение.")
            return
        try:
            channel_img = extract_channel(current_image_cv, channel.lower())
            update_image_display(channel_img)
        except Exception as e:
            messagebox.showerror("Ошибка канала", str(e))

    root = tk.Tk()
    root.title("Обработка изображений")
    root.geometry("900x700")

    # Создаем фрейм для кнопок
    control_frame = tk.Frame(root)
    control_frame.pack(pady=10)

    btn_load = tk.Button(control_frame, text="Загрузить изображение", command=on_load_image)
    btn_load.pack(side=tk.LEFT, padx=5)

    btn_capture = tk.Button(control_frame, text="Сделать снимок", command=on_capture)
    btn_capture.pack(side=tk.LEFT, padx=5)

    # Фрейм для кнопок каналов
    channel_frame = tk.Frame(root)
    channel_frame.pack(pady=5)

    for ch in ("R", "G", "B"):
        btn = tk.Button(
            channel_frame,
            text=f"Показать {ch}",
            command=lambda c=ch: on_show_channel(c),
            width=12
        )
        btn.pack(side=tk.LEFT, padx=5)

    # Область для отображения изображения
    image_frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=2)
    image_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    image_label = tk.Label(image_frame)
    image_label.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
