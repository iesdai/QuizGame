import pandas as pd

import pygame as pg

import settings
import button


class Quiz:
    def __init__(self, screen):
        """
        Данный метод инициализирует переменные, создает экземпляр класса кнопки, загружает данные вопросов из файла и
        устанавливает начальные значения для отображения текста на экране.
        """
        pg.init()
        self.screen = screen
        self.clock = pg.time.Clock()
        # Область для кнопки "Next"
        self.rect = pg.Rect(640, 460, 130, 50)
        self.color = settings.COLOR_INACTIVE
        self.text = ''
        self.txt_surface = settings.FONT.render(self.text, True, self.color)
        self.txt = settings.FONT.render('Next', True, self.color)
        self.active = False
        self.df = pd.read_csv('Russian_QA_Jeopardy_dataset_extended.csv', on_bad_lines='skip', sep='\t')
        self.butt = button.Button(self.screen)
        self.question_text = ''
        self.answer_text = ''
        self.score = 'Очки: '
        self.topic = 'Тема: '
        self.error = 'Ошибок: '
        self.end = 'Чтобы выйти из игры нажмите esc(escape)'

    def game(self, random):
        """
        Данный метод используется для установки текущего вопроса, темы и ответа на основе случайно выбранного вопроса
        из загруженных данных. Также метод отображает необходимую информацию на экране.
        """
        self.question_text = self.df.loc[random, 'QuestionText']
        self.topic = 'Тема: '
        self.topic += self.df.loc[random, 'Topic']
        self.answer_text = self.df.loc[random, 'Answer']
        self.blit_text(self.end, (30, 670), settings.WHITE)
        self.blit_text(self.topic, (30, 70), settings.WHITE)
        self.blit_text(self.error, (1060, 600), settings.WHITE)
        self.blit_text(self.score, (1100, 670), settings.WHITE)
        self.blit_text(self.question_text, (50, 260), settings.WHITE)

    def blit_text(self, text, pos, color):
        """
        Данный метод используется для отображения текста на экране. Он разбивает текст на слова и отображает их с
        учетом переноса на новую строку, если текст не помещается в ширину окна.
        """
        # Разбиваем текст на слова
        words = [word.split(' ') for word in text.splitlines()]
        # Расстояние между словами
        space = settings.FONT.size(' ')[0]
        # Максимальная ширина и высота окна
        max_width, max_height = self.screen.get_size()
        # Начальные координаты для отрисовки текста
        x, y = pos
        word_height = 0
        for line in words:
            for word in line:
                # Создание поверхности с текстом
                word_surface = settings.FONT.render(word, True, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]
                    y += word_height
                # Отображение поверхности с текстом на экране
                self.screen.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]
            y += word_height

    def handle_event(self, event):
        """
        Данный метод обрабатывает события ввода пользователя, такие как нажатия клавиш и клики мыши. В зависимости от
        события, метод обновляет состояние активности кнопки и текста кнопки.
        """
        if pg.mouse.get_pressed() != (1, 0, 0):
            pass
        # Проверка нажатия левой кнопки мыши
        else:
            pg.display.update()
            # Проверка, находится ли указатель мыши в пределах прямоугольника кнопки
            if self.rect.collidepoint(event.pos):
                # Инвертирование состояния активности кнопки
                self.active = not self.active
            else:
                self.active = False

        # Изменение цвета кнопки в зависимости от состояния активности
        self.color = settings.COLOR_ACTIVE if self.active else settings.COLOR_INACTIVE
        if event.type != pg.KEYDOWN or not self.active:
            return
        # Обработка событий клавиатуры только если кнопка активна
        if event.key == pg.K_BACKSPACE:
            # Удаление последнего символа из текста кнопки
            self.text = self.text[:-1]
        else:
            # Добавление введенного символа к тексту кнопки
            self.text += event.unicode
        # Обновление поверхности с текстом кнопки
        self.txt_surface = settings.FONT.render(self.text, True, self.color)

    def update(self):
        """
        Данный метод обновляет ширину прямоугольника кнопки в зависимости от текущего текста.
        """
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self):
        """
        Данный метод отображает текст кнопки и прямоугольник кнопки на экране.
        """
        # Отображение текста кнопки на экране
        self.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Отображение прямоугольника кнопки на экране
        pg.draw.rect(self.screen, self.color, self.rect, 3)
