from PIL import Image, ImageEnhance, ImageOps
import random

PALETTES = {
    "океан": [(8, 37, 103), (27, 59, 111), (36, 110, 185), (64, 144, 203), (100, 160, 214), (132, 185, 229), (169, 214, 229), (189, 224, 245), (209, 235, 252), (227, 245, 255)],
    "пустыня": [(120, 88, 42), (150, 118, 72), (194, 178, 128), (210, 190, 150), (225, 198, 153), (235, 215, 175), (245, 225, 164), (248, 235, 185), (248, 241, 192), (252, 248, 220)],
    "лес": [(23, 58, 24), (44, 95, 45), (65, 122, 67), (81, 152, 114), (100, 165, 100), (136, 176, 75), (160, 195, 100), (188, 231, 132), (200, 240, 150), (220, 250, 180)],
    "город": [(20, 20, 20), (45, 45, 45), (74, 74, 74), (100, 100, 100), (125, 125, 125), (150, 150, 150), (176, 176, 176), (200, 200, 200), (217, 217, 217), (235, 235, 235)],
    "пляж": [(180, 130, 70), (210, 160, 100), (230, 180, 120), (254, 207, 137), (254, 190, 106), (253, 160, 60), (253, 126, 20), (255, 165, 50), (255, 200, 100), (255, 230, 180)],
    "ледник": [(180, 220, 240), (205, 236, 245), (185, 225, 240), (161, 214, 226), (140, 200, 220), (121, 201, 226), (110, 185, 210), (90, 164, 199), (70, 140, 180), (50, 120, 160)],
    "горы": [(40, 40, 40), (60, 60, 60), (85, 85, 85), (102, 102, 102), (119, 119, 119), (136, 136, 136), (153, 153, 153), (170, 170, 170), (187, 187, 187), (204, 204, 204)],
    "пещера": [(15, 15, 15), (30, 30, 30), (46, 46, 46), (60, 60, 60), (75, 75, 75), (90, 90, 90), (106, 106, 106), (120, 120, 120), (140, 140, 140), (160, 160, 160)],
    "болото": [(30, 50, 25), (40, 65, 30), (59, 83, 35), (70, 95, 45), (85, 107, 47), (100, 120, 60), (107, 142, 35), (130, 160, 70), (144, 238, 144), (170, 250, 170)],
    "вулкан": [(30, 10, 5), (60, 20, 10), (90, 30, 15), (120, 40, 20), (150, 50, 25), (180, 60, 30), (210, 70, 35), (230, 80, 40), (240, 100, 50), (250, 120, 60)],
    "космос": [(0, 0, 20), (10, 10, 40), (20, 20, 60), (40, 20, 80), (60, 30, 100), (80, 40, 120), (100, 60, 140), (120, 80, 160), (140, 100, 180), (160, 120, 200)],
    "радуга": [(255, 0, 0), (255, 127, 0), (255, 255, 0), (127, 255, 0), (0, 255, 0), (0, 255, 127), (0, 255, 255), (0, 127, 255), (127, 0, 255), (255, 0, 255)],
    "неон": [(255, 0, 0), (255, 40, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 100, 255), (255, 0, 255), (255, 20, 147), (255, 140, 0), (255, 215, 0)],
    "закат": [(40, 10, 60), (80, 20, 100), (120, 40, 120), (180, 60, 100), (220, 80, 80), (255, 100, 60), (255, 140, 40), (255, 180, 30), (255, 220, 50), (255, 240, 120)],
}

def load_sprites_from_sheet_with_zoom(sheet_path, tile_size, zoom=0.5):
    sheet = Image.open(sheet_path).convert("RGBA")
    sheet_width, sheet_height = sheet.size  # 1724x1411
    
    # Примерный размер одного спрайта на листе
    sprite_on_sheet_width = sheet_width / 11  # 156 пикселей
    sprite_on_sheet_height = sheet_height / 9  # 156 пикселей
    
    sprites = []
    
    for row in range(9):
        for col in range(11):
            # Координаты центра спрайта
            center_x = col * sprite_on_sheet_width + sprite_on_sheet_width / 2
            center_y = row * sprite_on_sheet_height + sprite_on_sheet_height / 2
            
            # Размер области, которую мы вырезаем
            extract_size = int(sprite_on_sheet_width * zoom)
            
            # Если нужный tile_size меньше extract_size, то масштабируем потом
            left = int(center_x - extract_size / 2)
            top = int(center_y - extract_size / 2)
            right = int(center_x + extract_size / 2)
            bottom = int(center_y + extract_size / 2)
            
            # Проверяем границы
            left = max(0, left)
            top = max(0, top)
            right = min(sheet_width, right)
            bottom = min(sheet_height, bottom)
            
            box = (left, top, right, bottom)
            sprite = sheet.crop(box)
            
            # Масштабируем до нужного размера
            sprite = sprite.resize((tile_size, tile_size), Image.Resampling.NEAREST)
            sprites.append(sprite)
    return sprites

def apply_material_effects(sprite, palette, detail_level):
    size = sprite.size[0]
    result = Image.new("RGB", (size, size))
    base_color = random.choice(palette)
    pattern_color = random.choice([c for c in palette if c != base_color])
    element_size = max(1, {
        "низкий": size // 4,   
        "средний": size // 8,  
        "высокий": size // 16   
    }[detail_level])
    
    for x in range(0, size, element_size):
        for y in range(0, size, element_size):
            sprite_x = min(x, sprite.width - 1)
            sprite_y = min(y, sprite.height - 1)
            pixel = sprite.getpixel((sprite_x, sprite_y))
            brightness = sum(pixel[:3]) / 3
            if brightness > 160:
                color = pattern_color
            elif brightness < 96:
                color = base_color
            else:
                mix = (brightness - 96) / (160 - 96)
                color = tuple(
                    int(base_color[i] * (1 - mix) + pattern_color[i] * mix)
                    for i in range(3)
                )
            for dx in range(element_size):
                for dy in range(element_size):
                    pos_x, pos_y = x + dx, y + dy
                    if pos_x < size and pos_y < size:
                        result.putpixel((pos_x, pos_y), color)
    return result

def generate_tileset(rows, cols, tile_size, palette_name, detail_level):
    sprites = load_sprites_from_sheet_with_zoom("sprites3.png", tile_size, zoom=0.3)  
    palette = PALETTES.get(palette_name, PALETTES["океан"])
    tileset_img = Image.new("RGB", (cols * tile_size, rows * tile_size))
    for r in range(rows):
        for c in range(cols):
            base_sprite = random.choice(sprites)
            tile = apply_material_effects(base_sprite, palette, detail_level)
            tileset_img.paste(tile, (c * tile_size, r * tile_size))
    
    return tileset_img
