import tkinter as tk
from tkinter import font, messagebox
import generator
import saved
from PIL import Image, ImageTk

class SelectableButton:
    def __init__(self, parent, text, x, y, group=None, width=250, height=60):
        self.selected = False
        self.group = group
        self.text = text
        self.button = tk.Label(
            parent,
            text=text,
            bg='#EFC141',
            fg='black',
            font=('Arial', 16),
            relief='flat',
        )
        self.button.place(x=x, y=y, width=width, height=height)
        self.button.bind('<Button-1>', self.select)
        self.button.bind('<Enter>', self.on_hover)
        self.button.bind('<Leave>', self.on_leave)

        if group == 1:
            all_buttons_group1.append(self)
        elif group == 2:
            all_buttons_group2.append(self)
        elif group == 3:
            all_buttons_group3.append(self)

    def select(self, event=None):
        if self.group == 1:
            for btn in all_buttons_group1:
                btn.deselect()
        elif self.group == 2:
            for btn in all_buttons_group2:
                btn.deselect()
        elif self.group == 3:
            for btn in all_buttons_group3:
                btn.deselect()

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


class DropdownMenu:
    def __init__(self, parent, x, y, width=790, height=60):
        self.parent = parent
        self.is_open = False
        self.width = width
        self.height = height
        self.selected_palette = None
        self.selected = False

        self.button = tk.Label(
            parent,
            text="посмотреть ещё...",
            bg="#EFC141",
            fg="black",
            font=("Arial", 16),
            relief="flat"
        )
        self.button.place(x=x, y=y, width=width, height=height)
        self.button.bind("<Button-1>", self.toggle)
        self.button.bind('<Enter>', self.on_hover)
        self.button.bind('<Leave>', self.on_leave)
        
        all_buttons_group2.append(self)

        self.frame = tk.Frame(parent, bg="#CCA243", relief="flat", pady=20)
        self.items = []

        extra_names = [
            "город", "пляж", "ледник", 
            "горы", "пещера", "болото",
            "закат","неон","радуга",
            "космос","вулкан",
        ]

        self.build_items(extra_names)

    def build_items(self, names):
        for it in self.items:
            try:
                it.button.destroy()
            except:
                pass
        self.items.clear()
        row = 0
        col = 0
        max_cols = 3
        for name in names:
            btn = SelectableButton(
                self.frame,
                name,
                x=col * 270,
                y=row * 80,
                group=2,
                width=250,
                height=60
            )
            btn.button.bind("<Button-1>", lambda e, n=name: self.select_from_dropdown(n))
            self.items.append(btn)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        total_rows = (len(names) + max_cols - 1) // max_cols
        self.frame_width = (max_cols * 270) - 20
        self.frame_height = total_rows * 80 + 20

    def select_from_dropdown(self, palette_name):
        for btn in all_buttons_group2:
            btn.deselect()
        self.selected_palette = palette_name
        self.button.config(
            text=palette_name,
            bg='#CCA243',
            highlightbackground='#5E0C32',
            highlightthickness=2
        )
        self.close()
        self.selected = True

    def select(self, event=None):
        for btn in all_buttons_group2:
            if btn != self:
                btn.deselect()
        
        self.selected = True
        self.button.config(
            bg='#CCA243',
            highlightbackground='#5E0C32',
            highlightthickness=2
        )

    def deselect(self):
        self.selected = False
        self.selected_palette = None
        self.button.config(
            bg='#EFC141',
            highlightthickness=0,
            text="посмотреть ещё..."
        )
        self.close()

    def on_hover(self, event):
        if not self.selected:
            self.button.config(bg='#CCA243')

    def on_leave(self, event):
        if not self.selected:
            self.button.config(bg='#EFC141')

    def toggle(self, event=None):
        if self.is_open:
            self.close()
        else:
            self.open()

    def open(self):
        self.is_open = True
        btn_x = self.button.winfo_x()
        btn_y = self.button.winfo_y()
        self.frame.place(
            x=btn_x, 
            y=btn_y + self.height, 
            width=self.frame_width, 
            height=self.frame_height
        )
        self.frame.lift()

    def close(self):
        self.is_open = False
        self.frame.place_forget()

    def get_value(self):
        if self.selected_palette:
            return self.selected_palette
        elif self.button.cget('text') != "посмотреть ещё...":
            return self.button.cget('text')
        return None

def validate_input(rows_entry, cols_entry):
    try:
        rows = rows_entry.get().strip()
        cols = cols_entry.get().strip()
        if not rows or not cols:
            messagebox.showerror("Ошибка", "Введите количество строк и столбцов!")
            return None, None
        rows = int(rows)
        cols = int(cols)
        if rows <= 0 or cols <= 0:
            messagebox.showerror("Ошибка", "Количество строк и столбцов должно быть больше 0!")
            return None, None
        if rows > 20 or cols > 20:
            messagebox.showerror("Ошибка", "Слишком большой размер! Максимум 20x20.")
            return None, None
        return rows, cols
    except ValueError:
        messagebox.showerror("Ошибка", "Введите целые числа в поля строк и столбцов!")
        return None, None

def display_tileset(image): # Функция вывода тайлсета
    try:
        tileset_canvas.delete("all")
        display_width = 400
        display_height = 400
        # Получаем размер оригинального изображения
        img_width, img_height = image.size
        # Сохраняем пропорции
        scale_x = display_width / img_width
        scale_y = display_height / img_height
        scale = min(scale_x, scale_y)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        # Масштабируем с NEAREST для пиксельной графики
        image_resized = image.resize((new_width, new_height), Image.Resampling.NEAREST)
        # Конвертируем в PhotoImage
        photo = ImageTk.PhotoImage(image_resized)
        # Центрируем изображение
        x_offset = (380 - new_width) // 2
        y_offset = (380 - new_height) // 2
        # Отображаем на canvas
        tileset_canvas.create_image(
            x_offset + new_width // 2,
            y_offset + new_height // 2,
            image=photo,
            anchor='center'
        )
        # Сохраняем ссылку
        tileset_canvas.image = photo
        return True
        
    except Exception as e:
        print(f"Ошибка при отображении тайлсета: {e}")
        # Показываем ошибку
        tileset_canvas.create_text(
            190, 190,
            text="Ошибка отображения",
            fill='red',
            font=('Arial', 12)
        )
        return False

def reset_settings(): # Функция сброса кнопок
    for btn in all_buttons_group1:
        btn.deselect()
    for btn in all_buttons_group2:
        btn.deselect()
    for btn in all_buttons_group3:
        btn.deselect()
    # Сброс меню
    more_palettes_btn.deselect()
    # Очищаем canvas
    tileset_canvas.delete("all")
    tileset_canvas.create_text(
        190, 190,
        text="Тайлсет не сгенерирован",
        fill='gray',
        font=('Arial', 14)
    )
    # Очищаем глобальную переменную
    global current_tileset
    current_tileset = None
    # Сбрасываем поля ввода
    rows_entry.delete(0, tk.END)
    cols_entry.delete(0, tk.END)
    rows_entry.insert(0, "3")
    cols_entry.insert(0, "3")

def get_selected_params():
    # Получаем выбранный размер
    selected_size = None
    size_map = {"8x8": 8, "16x16": 16, "32x32": 32}
    for btn in all_buttons_group1:
        if btn.selected:
            selected_size = size_map.get(btn.get_value())
            break
    # Получаем выбранную палитру
    selected_palette = None
    for btn in all_buttons_group2:
        if btn.selected:
            if hasattr(btn, 'get_value'):
                selected_palette = btn.get_value()
            else:
                selected_palette = btn.button.cget('text')
            break
    if not selected_palette:
        selected_palette = more_palettes_btn.get_value()
    # Получаем выбранный уровень детализации
    selected_detail = None
    for btn in all_buttons_group3:
        if btn.selected:
            selected_detail = btn.get_value()
            break
    # Проверяем, все ли выбрано
    if not selected_size:
        messagebox.showerror("Ошибка", "Выберите размер тайлов!")
        return None, None, None
    if not selected_palette:
        messagebox.showerror("Ошибка", "Выберите палитру!")
        return None, None, None
    if not selected_detail:
        messagebox.showerror("Ошибка", "Выберите уровень детализации!")
        return None, None, None
    return selected_size, selected_palette, selected_detail

def create_tileset():# Основная функция
    global current_tileset
    # Проверяем ввод размера сетки
    rows, cols = validate_input(rows_entry, cols_entry)
    if rows is None or cols is None:
        return
    # Получаем параметры
    params = get_selected_params()
    if params[0] is None:
        return
    selected_size, selected_palette, selected_detail = params
    try:
        # Генерируем тайлсет
        tileset = generator.generate_tileset(
            rows=rows,
            cols=cols, 
            tile_size=selected_size,
            palette_name=selected_palette,
            detail_level=selected_detail
        )
        # Сохраняем в глобальную переменную
        current_tileset = tileset
        # Отображаем тайлсет
        display_tileset(tileset)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при генерации:\n{str(e)}")

def create_single_tile(): # Функция создания одного тайла
    global current_tileset
    # Получаем параметры
    params = get_selected_params()
    if params[0] is None:
        return
    selected_size, selected_palette, selected_detail = params
    try:
        # Генерируем один тайл
        tile = generator.generate_tileset(
            rows=1,
            cols=1, 
            tile_size=selected_size,
            palette_name=selected_palette,
            detail_level=selected_detail
        )
        # Сохраняем в глобальную переменную
        current_tileset = tile
        # Отображаем тайл
        display_tileset(tile)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при генерации тайла:\n{str(e)}")

def save_tileset_dialog(): # Cохранение тайлсета
    global current_tileset
    if current_tileset is None:
        messagebox.showerror("Ошибка", "Сначала создайте тайлсет!")
        return
    saved.save_image_dialog(root, current_tileset)

# Интерфейс
root = tk.Tk()
root.title("MaxWin2025 - Генератор тайлсетов")
root.geometry("1440x900")
root.configure(bg='#987247')

font2 = font.Font(family="Verdana", size=20, weight="normal", slant="roman")

graphics_frame = tk.Frame(
    root,
    relief='flat',
    bg='#987247'
)
graphics_frame.place(x=40, y=40, width=400, height=400)

# Canvas для отображения тайлсета
tileset_canvas = tk.Canvas(
    graphics_frame, 
    width=380,
    height=380,
    bg='#987247',
    highlightthickness=0
)
tileset_canvas.place(relx=0.5, rely=0.5, anchor='center')
# Начальное сообщение
tileset_canvas.create_text(
    190, 190,
    text="Тайлсет не сгенерирован",
    fill='gray',
    font=('Arial', 14)
)

# Глобальные списки групп
all_buttons_group1 = []
all_buttons_group2 = []
all_buttons_group3 = []
format_buttons = []  # Для кнопок выбора формата

# Глобальная переменная для хранения последнего сгенерированного тайлсета
current_tileset = None

# Размер сетки
grid_label = tk.Label(
    root,
    bg='#914638',
    relief='flat',
    text="РАЗМЕР СЕТКИ",
    font=font2,
    fg='black'
)
grid_label.place(x=40, y=460, width=400, height=60)

# Поля для ввода
grid_frame = tk.Frame(root, bg='#987247')
grid_frame.place(x=40, y=540, width=400, height=100)

# Строки
rows_label = tk.Label(
    grid_frame,
    text="Строки:",
    bg='#987247',
    fg='black',
    font=('Arial', 16)
)
rows_label.place(x=20, y=10)
rows_entry = tk.Entry(
    grid_frame,
    font=('Arial', 16),
    bg='#EFC141',
    fg='black',
    relief='flat',
    justify='center',
    width=8
)
rows_entry.place(x=120, y=10)
rows_entry.insert(0, "3")

# Столбцы
cols_label = tk.Label(
    grid_frame,
    text="Столбцы:",
    bg='#987247',
    fg='black',
    font=('Arial', 16)
)
cols_label.place(x=20, y=50)
cols_entry = tk.Entry(
    grid_frame,
    font=('Arial', 16),
    bg='#EFC141',
    fg='black',
    relief='flat',
    justify='center',
    width=8
)
cols_entry.place(x=120, y=50)
cols_entry.insert(0, "3")

# Размер
size_label = tk.Label(
    root,
    bg='#914638',
    relief='flat',
    text="РАЗМЕР ТАЙЛОВ",
    font=font2,
    fg='black'
)
size_label.place(x=610, y=20, width=790, height=60)
btn1 = SelectableButton(root, "8x8", 610, 100, group=1, width=250, height=60)
btn2 = SelectableButton(root, "16x16", 880, 100, group=1, width=250, height=60)
btn3 = SelectableButton(root, "32x32", 1150, 100, group=1, width=250, height=60)

# Палитра
palet_label = tk.Label(
    root,
    bg='#914638',
    relief='flat',
    text="ПАЛИТРА",
    font=font2,
    fg='black'
)
palet_label.place(x=610, y=180, width=790, height=60)
btn4 = SelectableButton(root, "океан", 610, 260, group=2, width=250, height=60)
btn5 = SelectableButton(root, "пустыня", 880, 260, group=2, width=250, height=60)
btn6 = SelectableButton(root, "лес", 1150, 260, group=2, width=250, height=60)
more_palettes_btn = DropdownMenu(root, 610, 340, width=790, height=60)

# Уровень детализации
quality_label = tk.Label(
    root,
    bg='#914638',
    relief='flat',
    text="УРОВЕНЬ ДЕТАЛИЗАЦИИ",
    font=font2,
    fg='black'
)
quality_label.place(x=610, y=420, width=790, height=60)
btn7 = SelectableButton(root, "низкий", 610, 500, group=3, width=250, height=60)
btn8 = SelectableButton(root, "средний", 880, 500, group=3, width=250, height=60)
btn9 = SelectableButton(root, "высокий", 1150, 500, group=3, width=250, height=60)

# Сбросить настройки
reset_button = tk.Label(
    root,
    text="СБРОСИТЬ НАСТРОЙКИ",
    bg='#913D36',
    fg='black',  
    font=('Arial', 20, 'bold'),
    relief='flat',
    cursor="hand2"
)
reset_button.place(x=40, y=660, width=400, height=80)
reset_button.bind('<Button-1>', lambda e: reset_settings())
reset_button.bind('<Enter>', lambda e: reset_button.config(bg='#A8453E'))
reset_button.bind('<Leave>', lambda e: reset_button.config(bg='#913D36'))

# Создать 1 тайл
create_tile_button = tk.Label(
    root,
    text="СОЗДАТЬ ТАЙЛ",
    bg='#913D36',
    fg='black',  
    font=('Arial', 24, 'bold'),
    relief='flat',
    cursor="hand2"
)
create_tile_button.place(x=610, y=580, width=380, height=80)
create_tile_button.bind('<Button-1>', lambda e: create_single_tile())
create_tile_button.bind('<Enter>', lambda e: create_tile_button.config(bg='#A8453E'))
create_tile_button.bind('<Leave>', lambda e: create_tile_button.config(bg='#913D36'))

# Создать тайлсет
create_tileset_button = tk.Label(
    root,
    text="СОЗДАТЬ ТАЙЛСЕТ",
    bg='#913D36',
    fg='black',  
    font=('Arial', 24, 'bold'),
    relief='flat',
    cursor="hand2"
)
create_tileset_button.place(x=1020, y=580, width=380, height=80)
create_tileset_button.bind('<Button-1>', lambda e: create_tileset())
create_tileset_button.bind('<Enter>', lambda e: create_tileset_button.config(bg='#A8453E'))
create_tileset_button.bind('<Leave>', lambda e: create_tileset_button.config(bg='#913D36'))

# Соранить тайлсет
save_button = tk.Label(
    root,
    text="СОХРАНИТЬ ТАЙЛСЕТ",
    bg='#914638',
    fg='black',
    font=('Arial', 24, 'bold'),
    relief='flat',
    cursor="hand2"
)
save_button.place(x=610, y=680, width=790, height=80)
save_button.bind('<Button-1>', lambda e: save_tileset_dialog())
save_button.bind('<Enter>', lambda e: save_button.config(bg='#A8453E'))
save_button.bind('<Leave>', lambda e: save_button.config(bg='#914638'))

# Запуск
root.mainloop()
