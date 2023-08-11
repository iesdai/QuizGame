import pygame as pg

import settings


class Button:
    def __init__(self, screen):
        pg.init()
        self.screen = screen
        self.but = pg.Rect(460, 460, 130, 40)
        self.active = False
        self.color = settings.COLOR_INACTIVE
        self.txt = settings.FONT.render('Next', True, self.color)

    def press(self, event):
        """
        Данный метод обрабатывает события нажатия кнопки мыши. Если левая кнопка мыши нажата, метод проверяет,
        находится ли указатель мыши в пределах прямоугольника кнопки. В зависимости от этого метод изменяет состояние
        активности кнопки и ее цвет.
        """
        # Проверка нажатия левой кнопки мыши
        if pg.mouse.get_pressed() == (1, 0, 0):
            pg.display.update()
            # Проверка, находится ли указатель мыши в пределах прямоугольника кнопки
            if self.but.collidepoint(event.pos):
                # Инвертирование состояния активности кнопки
                self.active = not self.active
            else:
                self.active = False
        # Изменение цвета кнопки в зависимости от состояния активности
        self.color = settings.COLOR_ACTIVE if self.active else settings.COLOR_INACTIVE
        # Обновление текста кнопки
        self.txt = settings.FONT.render('Next', True, self.color)

    def draw(self):
        """
        Данный метод отображает текст кнопки на экране, используя текущий цвет кнопки.
        """
        self.screen.blit(self.txt, (self.but.x + 5, self.but.y + 5))
