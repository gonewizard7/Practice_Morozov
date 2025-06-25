"""
Пользовательский интерфейс приложения.
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import ImageTk, Image
from image_loader import load_image
from webcam_capture import capture_from_webcam
from channel_extractor import extract_channel
from image_processing import crop_image, adjust_brightness, draw_line
from utils import cv_to_pil, validate_coordinates, get_image_size

def run_app():
    """
    Запускает главное окно приложения.
    Управляет состоянием изображений и операциями.
    """
    image_stack = []
    current_channel = None

    def push_image_state(image_cv):
        """Сохраняет текущее состояние изображения."""
        nonlocal current_channel
        current_channel = None
        image_stack.append(image_cv.copy())
        update_undo_button_state()
        update_image_info()

    def pop_image_state():
        """Восстанавливает предыдущее состояние."""
        nonlocal current_channel
        current_channel = None
        if len(image_stack) > 1:
            image_stack.pop()
            image = image_stack[-1].copy()
            update_image_info()
            return image
        if image_stack:
            update_image_info()
            return image_stack[0]
        return None

    def get_display_image():
        """Возвращает изображение для отображения."""
        if not image_stack:
            return None

        image_cv = image_stack[-1]

        if current_channel:
            return extract_channel(image_cv, current_channel)

        return cv_to_pil(image_cv)

    def update_image_display():
        """Обновляет отображение изображения."""
        image = get_display_image()
        if image is None:
            return

        # Конвертируем PIL Image в PhotoImage
        max_width = 800
        max_height = 600
        img_width, img_height = image.size

        if img_width > max_width or img_height > max_height:
            ratio = min(max_width / img_width, max_height / img_height)
            new_size = (int(img_width * ratio), int(img_height * ratio))
            image = image.resize(new_size, Image.LANCZOS)

        img_tk = ImageTk.PhotoImage(image)
        image_label.config(image=img_tk)
        image_label.image = img_tk

        update_image_info()

    def update_image_info():
        """Обновляет информацию об изображении."""
        if not image_stack:
            size_label.config(text="Размер: -")
            type_label.config(text="Тип: -")
            coord_label.config(text="Допустимые координаты: -")
            return

        image_cv = image_stack[-1]
        width, height = get_image_size(image_cv)

        # Определяем тип изображения
        if len(image_cv.shape) == 2:
            img_type = "Черно-белое"
        elif image_cv.shape[2] == 3:
            img_type = "Цветное (RGB)"
        else:
            img_type = f"Каналов: {image_cv.shape[2]}"

        size_label.config(text=f"Размер: {width}×{height} пикселей")
        type_label.config(text=f"Тип: {img_type}")

        coord_text = f"Допустимые координаты: X: 0-{width-1}, Y: 0-{height-1}"
        coord_label.config(text=coord_text)

        status_text = f"Шагов: {len(image_stack)}"
        status_label.config(text=status_text)

    def update_undo_button_state():
        """Обновляет состояние кнопки 'Отменить'."""
        if len(image_stack) > 1:
            btn_undo.config(state=tk.NORMAL)
        else:
            btn_undo.config(state=tk.DISABLED)

    def on_load_image():
        """Обработчик загрузки изображения с диска."""
        path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.png *.jpg *.jpeg")])
        if not path:
            return
        try:
            pil_img, cv_img = load_image(path)
            image_stack.clear()
            push_image_state(cv_img)
            update_image_display()
            reset_operation_state()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def on_capture():
        """Обработчик захвата изображения с камеры."""
        try:
            cv_img = capture_from_webcam()
            image_stack.clear()
            push_image_state(cv_img)
            update_image_display()
            reset_operation_state()
        except Exception as e:
            messagebox.showerror("Ошибка камеры", str(e))

    def on_undo():
        """Отменяет последнюю операцию."""
        if len(image_stack) > 1:
            prev_state = pop_image_state()
            image_stack[-1] = prev_state
            update_image_display()

    def on_show_channel(channel):
        """Переключает отображение цветового канала."""
        nonlocal current_channel
        if not image_stack:
            messagebox.showwarning("Ошибка", "Загрузите изображение")
            return

        # Переключаем канал
        if current_channel == channel:
            current_channel = None
        else:
            current_channel = channel

        update_image_display()

    def reset_operation_state():
        """Сбрасывает состояние операций."""
        operation_combobox.set('')
        for entry in param_entries.values():
            entry.delete(0, tk.END)

    def validate_input(entries, types=int):
        """Проверяет корректность введенных данных."""
        values = []
        for entry in entries:
            value_str = entry.get()
            if not value_str:
                raise ValueError("Все поля должны быть заполнены")
            try:
                value = types(value_str)
                values.append(value)
            except ValueError:
                raise ValueError("Некорректное числовое значение")
        return values

    def apply_operation():
        """Применяет выбранную операцию к изображению."""
        if not image_stack:
            messagebox.showwarning("Ошибка", "Загрузите изображение")
            return

        operation = operation_combobox.get()
        if not operation:
            messagebox.showwarning("Ошибка", "Выберите операцию")
            return

        try:
            current_cv_image = image_stack[-1]

            if operation == "Обрезка":
                values = validate_input([
                    param_entries["x1"],
                    param_entries["y1"],
                    param_entries["x2"],
                    param_entries["y2"]
                ])
                x1, y1, x2, y2 = values

                if x1 >= x2 or y1 >= y2:
                    raise ValueError("Координаты должны быть: x1 < x2, y1 < y2")

                validate_coordinates(current_cv_image, x1, y1, x2, y2)
                result = crop_image(current_cv_image, x1, y1, x2, y2)

            elif operation == "Яркость":
                values = validate_input([param_entries["brightness"]])
                value = values[0]

                if not -255 <= value <= 255:
                    raise ValueError("Яркость должна быть от -255 до 255")

                result = adjust_brightness(current_cv_image, value)

            elif operation == "Линия":
                values = validate_input([
                    param_entries["line_x1"],
                    param_entries["line_y1"],
                    param_entries["line_x2"],
                    param_entries["line_y2"],
                    param_entries["thickness"]
                ])
                x1, y1, x2, y2, thickness = values

                if thickness <= 0:
                    raise ValueError("Толщина линии должна быть > 0")

                validate_coordinates(current_cv_image, x1, y1, x2, y2)
                result = draw_line(current_cv_image, x1, y1, x2, y2, thickness)

            push_image_state(result)
            update_image_display()

        except Exception as e:
            messagebox.showerror("Ошибка операции", str(e))

    def on_operation_select(event):
        """Обновляет интерфейс при выборе операции."""
        operation = operation_combobox.get()

        for widget in param_frame.winfo_children():
            widget.grid_forget()

        row = 0
        if operation == "Обрезка":
            ttk.Label(param_frame, text="Левый верхний угол:"
                     ).grid(row=row, column=0, padx=5, pady=2, sticky="e")
            param_entries["x1"].grid(row=row, column=1, padx=5, pady=2)
            param_entries["y1"].grid(row=row, column=2, padx=5, pady=2)
            row += 1
            ttk.Label(param_frame, text="Правый нижний угол:"
                     ).grid(row=row, column=0, padx=5, pady=2, sticky="e")
            param_entries["x2"].grid(row=row, column=1, padx=5, pady=2)
            param_entries["y2"].grid(row=row, column=2, padx=5, pady=2)

        elif operation == "Яркость":
            ttk.Label(param_frame, text="Яркость (-255 до 255):"
                     ).grid(row=row, column=0, padx=5, pady=2, sticky="e")
            param_entries["brightness"].grid(row=row, column=1, padx=5, pady=2)

        elif operation == "Линия":
            ttk.Label(param_frame, text="Начало линии:"
                     ).grid(row=row, column=0, padx=5, pady=2, sticky="e")
            param_entries["line_x1"].grid(row=row, column=1, padx=5, pady=2)
            param_entries["line_y1"].grid(row=row, column=2, padx=5, pady=2)
            row += 1
            ttk.Label(param_frame, text="Конец линии:"
                     ).grid(row=row, column=0, padx=5, pady=2, sticky="e")
            param_entries["line_x2"].grid(row=row, column=1, padx=5, pady=2)
            param_entries["line_y2"].grid(row=row, column=2, padx=5, pady=2)
            row += 1
            ttk.Label(param_frame, text="Толщина линии:"
                     ).grid(row=row, column=0, padx=5, pady=2, sticky="e")
            param_entries["thickness"].grid(row=row, column=1, padx=5, pady=2)

    # Создание главного окна
    root = tk.Tk()
    root.title("Редактор изображений")
    root.geometry("1000x900")

    # Панель информации об изображении
    info_frame = ttk.Frame(root, padding=10)
    info_frame.pack(fill=tk.X, padx=10, pady=5)

    size_label = ttk.Label(info_frame, text="Размер: -")
    size_label.pack(side=tk.LEFT, padx=10)

    type_label = ttk.Label(info_frame, text="Тип: -")
    type_label.pack(side=tk.LEFT, padx=10)

    coord_label = ttk.Label(info_frame, text="Допустимые координаты: -")
    coord_label.pack(side=tk.LEFT, padx=10)

    # Панель управления
    control_frame = ttk.Frame(root, padding=10)
    control_frame.pack(fill=tk.X, padx=10, pady=5)

    # Кнопки управления
    ttk.Button(control_frame, text="Загрузить изображение",
              command=on_load_image).pack(side=tk.LEFT, padx=5)
    ttk.Button(control_frame, text="Сделать снимок",
              command=on_capture).pack(side=tk.LEFT, padx=5)
    btn_undo = ttk.Button(control_frame, text="Отменить",
                         command=on_undo, state=tk.DISABLED)
    btn_undo.pack(side=tk.RIGHT, padx=5)

    # Панель цветовых каналов
    channel_frame = ttk.LabelFrame(control_frame, text="Цветовые каналы")
    channel_frame.pack(side=tk.LEFT, padx=20)

    channel_buttons = {}
    for ch, text in [('r', "Красный (R)"), ('g', "Зеленый (G)"), ('b', "Синий (B)")]:
        btn = ttk.Button(channel_frame, text=text,
                        command=lambda c=ch: on_show_channel(c))
        btn.pack(side=tk.LEFT, padx=2)
        channel_buttons[ch] = btn

    # Панель операций
    operation_frame = ttk.LabelFrame(root, text="Операции с изображением",
                                   padding=10)
    operation_frame.pack(fill=tk.X, padx=10, pady=5)

    ttk.Label(operation_frame, text="Выберите операцию:"
             ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    operations = ["Обрезка", "Яркость", "Линия"]
    operation_combobox = ttk.Combobox(operation_frame, values=operations,
                                     state="readonly", width=15)
    operation_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    operation_combobox.bind("<<ComboboxSelected>>", on_operation_select)

    # Параметры операций
    param_frame = ttk.Frame(operation_frame)
    param_frame.grid(row=1, column=0, columnspan=3, pady=5, sticky="w")

    # Поля ввода
    param_entries = {
        "x1": ttk.Entry(param_frame, width=8),
        "y1": ttk.Entry(param_frame, width=8),
        "x2": ttk.Entry(param_frame, width=8),
        "y2": ttk.Entry(param_frame, width=8),
        "brightness": ttk.Entry(param_frame, width=8),
        "line_x1": ttk.Entry(param_frame, width=8),
        "line_y1": ttk.Entry(param_frame, width=8),
        "line_x2": ttk.Entry(param_frame, width=8),
        "line_y2": ttk.Entry(param_frame, width=8),
        "thickness": ttk.Entry(param_frame, width=8)
    }

    # Кнопка применения
    ttk.Button(operation_frame, text="Применить",
              command=apply_operation, width=20
              ).grid(row=2, column=0, columnspan=3, pady=10)

    # Область изображения
    image_frame = ttk.LabelFrame(root, text="Просмотр изображения",
                               padding=10)
    image_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    image_label = ttk.Label(image_frame)
    image_label.pack(fill=tk.BOTH, expand=True)

    # Строка состояния
    status_frame = ttk.Frame(root)
    status_frame.pack(fill=tk.X, padx=10, pady=5)
    status_label = ttk.Label(status_frame, text="Готово к работе")
    status_label.pack(side=tk.RIGHT, anchor="e")

    root.mainloop()
