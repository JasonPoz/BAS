import sqlite3

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.anchorlayout import AnchorLayout
from kivy.config import Config
from kivy.core.window import Window
# Глобальные настройки
Window.clearcolor = (10, 1, 1, 1)
Window.size = (540, 960)  # Установка начального размера окна

class MyApp(App):
    def build(self):
        self.language = "Русский"  # Изначально устанавливаем русский язык
        self.conn = sqlite3.connect('sirius.sqlite3')  # Подключение к базе данных SQLite
        self.cursor = self.conn.cursor()

        # Создаем строку ввода
        search_input = TextInput(hint_text="Введите термин", multiline=False, size_hint=(None, None), size=(400, 50))
        search_input.bind(on_text=self.search_term)  # Привязываем метод search_term к событию on_text

        # Создаем верхнюю панель для кнопок и строки ввода
        top_panel = BoxLayout(orientation='vertical', size_hint=(1, None), height=200, padding=[10, 80], spacing=10)

        # Добавляем строку поиска в верхнюю панель
        top_panel.add_widget(search_input)

        # Создаем кнопки
        self.tariffs_button = Button(text='Тарифы', size_hint=(None, None), size=(120, 40))
        self.about_button = Button(text='О приложении', size_hint=(None, None), size=(160, 40))
        russian_button = Button(text='Русский', size_hint=(None, None), size=(120, 40), on_press=self.switch_language_russian)
        english_button = Button(text='Английский', size_hint=(None, None), size=(160, 40), on_press=self.switch_language_english)

        # Добавляем кнопки в верхнюю панель
        top_panel.add_widget(self.tariffs_button)
        top_panel.add_widget(self.about_button)
        top_panel.add_widget(russian_button)
        top_panel.add_widget(english_button)

        # Создаем метку для отображения текста
        self.label = Label(text='Приветственный текст', size_hint=(.6, .6), font_size='25sp',
                      pos_hint={'center_x': .4, 'center_y': .3}, bold=True, italic=True, color=(0, 0, 0, 1))

        # Создаем главный макет
        box1 = AnchorLayout()
        box1.add_widget(top_panel)
        box1.add_widget(self.label)

        return box1



    def switch_language_english(self, instance):
        self.language = "English"
        self.tariffs_button.text = "Tariffs"
        self.about_button.text = "About in app"
        self.update_language()

    def switch_language_russian(self, instance):
        self.language = "Русский"
        self.tariffs_button.text = "Тарифы"
        self.about_button.text = "О приложении"
        self.update_language()
    def update_language(self):
        for widget in self.root.children:
            if isinstance(widget, BoxLayout):
                for child in widget.children:
                    if isinstance(child, Button):
                        if self.language == "Русский":
                            if child.text == 'Русский':
                                child.disabled = True
                            elif child.text == 'Английский':
                                child.disabled = False
                        elif self.language == "English":
                            if child.text == 'Русский':
                                child.disabled = False
                            elif child.text == 'Английский':
                                child.disabled = True

    def search_term(self, instance):
        term = instance.text
        if term:
            self.cursor.execute("""
                SELECT * FROM glossary 
                WHERE term_eng LIKE ? 
                    OR term_rus LIKE ? 
                    OR definition_rus LIKE ? 
                    OR definition_eng LIKE ? 
                    OR context_eng LIKE ? 
                    OR context_rus LIKE ?
            """, (f'%{term}%', f'%{term}%', f'%{term}%', f'%{term}%', f'%{term}%', f'%{term}%'))
            results = self.cursor.fetchall()
            if results:
                definitions = "\n".join(
                    result[6] for result in results)  # Получаем определения терминов из 7-го столбца
                self.label.text = definitions
            else:
                self.label.text = "Термин не найден"
        else:
            self.label.text = "Введите термин"

    def on_stop(self):
        # Закрытие соединения с базой данных при завершении приложения
        self.conn.close()
if __name__ == "__main__":
    MyApp().run()