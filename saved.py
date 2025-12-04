from PIL import Image
import tkinter as tk
from tkinter import messagebox
import tkinter.filedialog as fd
import os
from datetime import datetime


class FormatSelectButton:
    def __init__(self, parent, text, x, y, width=120, height=50):
        self.selected = False
        self.text = text
        self.button = tk.Label(
            parent,
            text=text,
            bg='#EFC141',
            fg='black',
            font=('Arial', 14),
            relief='flat',
        )
        self.button.place(x=x, y=y, width=width, height=height)
        self.button.bind('<Button-1>', self.select)
        self.button.bind('<Enter>', self.on_hover)
        self.button.bind('<Leave>', self.on_leave)

    def select(self, event=None):
        self.selected = True
        self.button.config(
            relief='flat',
            bg='#CCA243',
            highlightbackground='#5E0C32',
            highlightthickness=2
        )

    def deselect(self):
        self.selected = False
        self.button.config(
            relief='flat',
            bg='#EFC141',
            highlightthickness=0
        )

    def on_hover(self, event):
        if not self.selected:
            self.button.config(bg='#CCA243')

    def on_leave(self, event):
        if not self.selected:
            self.button.config(bg='#EFC141')

    def get_value(self):
        return self.text


def save_image_dialog(parent, image, callback=None):
    dialog = SaveDialog(parent, image, callback)
    return dialog


def save_image(image, filepath, format="PNG"):
    try:
        # Конвертируем для JPEG, если нужно
        if format.upper() == "JPEG" and image.mode != "RGB":
            image = image.convert("RGB")
        # Сохраняем изображение
        image.save(filepath, format=format.upper())
        return True
    except Exception as e:
        raise Exception(f"Ошибка при сохранении файла {filepath}: {str(e)}")


class SaveDialog:
    def __init__(self, parent, image, callback=None):
        self.parent = parent
        self.image = image
        self.callback = callback
        self.create_window()
        self.create_widgets()
        
    def create_window(self): # Создание окна диалога
        self.window = tk.Toplevel(self.parent)
        self.window.title("Сохранение тайлсета")
        self.window.geometry("800x600")
        self.window.configure(bg='#987247')
        self.window.resizable(False, False)
        self.window.grab_set()
        self.window.focus_set()
        # Обработка закрытия окна
        self.window.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
    def create_widgets(self): # Создание виджетов в окне
        # Заголовок
        title_label = tk.Label(
            self.window,
            text="СОХРАНЕНИЕ",
            bg='#914638',
            fg='black',
            font=('Arial', 24, 'bold'),
            relief='flat'
        )
        title_label.place(x=0, y=0, width=800, height=80)
        
        # Имя файла
        name_label = tk.Label(
            self.window,
            text="ВВЕДИТЕ ИМЯ",
            bg='#987247',
            fg='black',
            font=('Arial', 16, 'bold')
        )
        name_label.place(x=50, y=100)
        
        self.filename_var = tk.StringVar(value="tileset")
        self.filename_entry = tk.Entry(
            self.window,
            textvariable=self.filename_var,
            font=('Arial', 16),
            bg='#EFC141',
            fg='black',
            relief='flat',
            justify='center'
        )
        self.filename_entry.place(x=50, y=140, width=670, height=50)
        
        # Метка расширения
        self.extension_label = tk.Label(
            self.window,
            text=".png",
            bg='#987247',
            fg='black',
            font=('Arial', 16)
        )
        self.extension_label.place(x=700, y=140, height=50)
        
        # Формат файла
        format_label = tk.Label(
            self.window,
            text="ВЫБЕРИТЕ ФОРМАТ",
            bg='#987247',
            justify='center',
            fg='black',
            font=('Arial', 16, 'bold')
        )
        format_label.place(x=50, y=220)
        
        # Кнопки форматов
        format_frame = tk.Frame(self.window, bg='#987247')
        format_frame.place(x=50, y=260, width=700, height=60)
        
        self.format_buttons = []
        formats = ["JPEG", "PNG", "GIF", "BMP"]
        format_width = 160
        
        for i, fmt in enumerate(formats):
            x_pos = i * (format_width + 10) 
            btn = FormatSelectButton(format_frame, fmt, x_pos, 0, 
                                   width=format_width, height=50)
            btn.button.bind('<Button-1>', 
                           lambda e, b=btn: (self.select_format(b), 
                                            self.update_extension()))
            self.format_buttons.append(btn)
            
        # Выбираем PNG по умолчанию
        for btn in self.format_buttons:
            if btn.text == "PNG":
                self.select_format(btn)
                break
        
        # Выбор папки
        location_label = tk.Label(
            self.window,
            text="ВЫБЕРИТЕ РАСПОЛОЖЕНИЕ",
            bg='#987247',
            fg='black',
            font=('Arial', 16, 'bold')
        )
        location_label.place(x=50, y=340)
        
        self.folder_path_var = tk.StringVar(value="Расположение...")
        location_button = tk.Label(
            self.window,
            textvariable=self.folder_path_var,
            bg='#EFC141',
            fg='black',
            font=('Arial', 16),
            relief='flat',
        )
        location_button.place(x=50, y=380, width=670, height=50)
        location_button.bind('<Button-1>', lambda e: self.select_folder())
        location_button.bind('<Enter>', 
                           lambda e: location_button.config(bg='#CCA243'))
        location_button.bind('<Leave>', 
                           lambda e: location_button.config(bg='#EFC141'))
        
        # Кнопки действий
        buttons_frame = tk.Frame(self.window, bg='#987247')
        buttons_frame.place(x=50, y=460, width=700, height=80)
        
        # Кнопка Сохранить
        save_btn = tk.Label(
            buttons_frame,
            text="СОХРАНИТЬ",
            bg='#913D36',
            fg='black',
            font=('Arial', 20, 'bold'),
            relief='flat',
        )
        save_btn.place(x=0, y=0, width=340, height=60)
        save_btn.bind('<Button-1>', lambda e: self.perform_save())
        save_btn.bind('<Enter>', lambda e: save_btn.config(bg='#A8453E'))
        save_btn.bind('<Leave>', lambda e: save_btn.config(bg='#913D36'))
        
        # Кнопка Отмена
        cancel_btn = tk.Label(
            buttons_frame,
            text="ОТМЕНА",
            bg='#914638',
            fg='black',
            font=('Arial', 20, 'bold'),
            relief='flat',
        )
        cancel_btn.place(x=360, y=0, width=340, height=60)
        cancel_btn.bind('<Button-1>', lambda e: self.on_cancel())
        cancel_btn.bind('<Enter>', lambda e: cancel_btn.config(bg='#A8453E'))
        cancel_btn.bind('<Leave>', lambda e: cancel_btn.config(bg='#914638'))
    
    def select_format(self, selected_button):# Выбор формата файла
        for btn in self.format_buttons:
            btn.deselect()
        selected_button.select()
    
    def update_extension(self): # Обновление расширения файла
        selected_format = None
        for btn in self.format_buttons:
            if btn.selected:
                selected_format = btn.get_value().lower()
                break
        
        if selected_format:
            if selected_format == "jpeg":
                self.extension_label.config(text=".jpg")
            else:
                self.extension_label.config(text=f".{selected_format}")
    
    def select_folder(self): # Выбор папки для сохранения
        folder = fd.askdirectory(title="Выберите папку для сохранения")
        if folder:
            self.folder_path_var.set(folder)
    
    def perform_save(self):# Выполнение сохранения"""
        selected_format = None
        for btn in self.format_buttons:
            if btn.selected:
                selected_format = btn.get_value()
                break
        if not selected_format:
            messagebox.showerror("Ошибка", "Выберите формат файла!")
            return
        
        # Получаем имя файла
        filename = self.filename_var.get().strip()
        if not filename:
            messagebox.showerror("Ошибка", "Введите имя файла!")
            return
        
        # Получаем путь к папке
        folder_path = self.folder_path_var.get()
        if folder_path == "Расположение...":
            messagebox.showerror("Ошибка", "Выберите папку для сохранения!")
            return
        
        # Формируем полный путь
        if selected_format.lower() == "jpeg":
            extension = ".jpg"
        else:
            extension = f".{selected_format.lower()}"
        
        # Добавляем расширение
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            filename += extension
        
        full_path = os.path.join(folder_path, filename)
        
        try:
            # Сохраняем файл
            save_image(self.image, full_path, format=selected_format)
            
            # Вызываем callback, если он есть
            if self.callback:
                self.callback(full_path)
            
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении:\n{str(e)}")
    
    def on_cancel(self): # Обработка отмены
        self.window.destroy()


def save_tileset(image, filepath, format="PNG"):
    return save_image(image, filepath, format)

