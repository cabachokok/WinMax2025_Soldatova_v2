import os
import sys
import tempfile
from unittest.mock import Mock, patch
from PIL import Image

sys.modules['tkinter'] = Mock()
sys.modules['tkinter.filedialog'] = Mock()
sys.modules['tkinter.messagebox'] = Mock()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
with patch('tkinter.Tk'), \
     patch('tkinter.Label'), \
     patch('tkinter.Entry'), \
     patch('tkinter.Frame'), \
     patch('tkinter.Canvas'), \
     patch('tkinter.font'), \
     patch('tkinter.messagebox'):
    
    import app
    import generator
    import saved

class MockEntry:
    def __init__(self, value=""):
        self._value = value
    def get(self):
        return self._value

def test_1():
    rows_entry = MockEntry("3")
    cols_entry = MockEntry("3")
    result = app.validate_input(rows_entry, cols_entry)
    assert result is not None
    rows, cols = result
    class MockButton:
        def __init__(self, selected=False, text=""):
            self.selected = selected
            self.text = text
        def get_value(self):
            return self.text
    app.all_buttons_group1 = [MockButton(True, "16x16")]
    app.all_buttons_group2 = [MockButton(True, "океан")]
    app.all_buttons_group3 = [MockButton(True, "средний")]
    size, palette, detail = app.get_selected_params()
    if os.path.exists("sprites3.png"):
        img = generator.generate_tileset(rows, cols, size, palette, detail)
        assert img is not None
    test_img = Image.new('RGB', (50, 50), (255, 0, 0))
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        filepath = tmp.name
    saved.save_tileset(test_img, filepath, format="PNG")
    assert os.path.exists(filepath)
    os.unlink(filepath)

def test_2():
    rows_entry = MockEntry("")
    cols_entry = MockEntry("")
    result = app.validate_input(rows_entry, cols_entry)
    assert result == (None, None)

def test_3():
    rows_entry = MockEntry("abc")
    cols_entry = MockEntry("xyz")
    result = app.validate_input(rows_entry, cols_entry)
    assert result == (None, None)

def test_4():
    rows_entry = MockEntry("25")
    cols_entry = MockEntry("25")
    result = app.validate_input(rows_entry, cols_entry)
    assert result == (None, None)

def test_5():
    class MockButton:
        def __init__(self, selected=False, text=""):
            self.selected = selected
            self.text = text
        def get_value(self):
            return self.text
    app.all_buttons_group1 = [MockButton(True, "16x16")]
    app.all_buttons_group2 = []
    app.all_buttons_group3 = [MockButton(True, "средний")]
    app.more_palettes_btn.selected_palette = None
    app.more_palettes_btn.button.cget.return_value = "посмотреть ещё..."

    result = app.get_selected_params()
    assert result == (None, None, None)

def main():
    tests = [
        ("Успешный сценарий", test_1),
        ("Пустые поля", test_2),
        ("Нечисловые значения", test_3),
        ("Значения > 20", test_4),
        ("Не выбрана палитра", test_5),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            test_func()
            results.append((name, True))
            print(f"{name}: Тест пройден")
        except Exception as e:
            results.append((name, False))
            print(f"{name}: Ошибка")
    
    passed = sum(1 for _, success in results if success)
    
    if passed == len(tests):
        print("Все тесты пройдены")
    else:
        print("Не все тесты пройдены")
        sys.exit(1)

if __name__ == "__main__":
    main()
