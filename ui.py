import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image

from image_loader import load_image
from webcam_capture import capture_from_webcam
from channel_extractor import extract_channel
from utils import cv_to_pil

current_image = None

def run_app():
    """Запуск основного окна приложения."""
    def open_file():
        nonlocal current_image
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.jpg *.png")]
            )
            if not file_path:
                return
            current_image = load_image(file_path)
            display_image(current_image)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение:\n{e}")

    def capture_image():
        nonlocal current_image
        try:
            current_image = capture_from_webcam()
            display_image(current_image)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Проблема с веб-камерой:\n{e}")

    def display_image(img_cv):
        img_pil = cv_to_pil(img_cv)
        img_tk = ImageTk.PhotoImage(img_pil)
        label.config(image=img_tk)
        label.image = img_tk  # Храним ссылку

    def show_channel(channel):
        if current_image is None:
            messagebox.showwarning("Внимание", "Сначала загрузите изображение.")
            return
        ch_img = extract_channel(current_image, channel)
        display_image(ch_img)

    # Окно
    root = tk.Tk()
    root.title("Image Channel Viewer")

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Загрузить изображение", command=open_file).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Сделать снимок с веб-камеры", command=capture_image).pack(side=tk.LEFT, padx=5)

    ch_frame = tk.Frame(root)
    ch_frame.pack(pady=5)
    tk.Button(ch_frame, text="Красный", command=lambda: show_channel('r')).pack(side=tk.LEFT, padx=3)
    tk.Button(ch_frame, text="Зелёный", command=lambda: show_channel('g')).pack(side=tk.LEFT, padx=3)
    tk.Button(ch_frame, text="Синий", command=lambda: show_channel('b')).pack(side=tk.LEFT, padx=3)

    label = tk.Label(root)
    label.pack(pady=10)

    root.mainloop()
