import pygame as pg

import settings


class Menu:
    def __init__(self, screen):
        pg.init()
        # Экран, на котором будет отображаться меню
        self.screen = screen

    def draw_start_menu(self):
        """
        Данный метод отвечает за отрисовку элементов стартового меню.
        """
        # Заполнение экрана цветом фона
        self.screen.fill(settings.COLOR_BACKGROUND)
        # Создание поверхности с заголовком
        title = settings.FONT.render('Quiz Game', True, settings.WHITE)
        # Создание поверхности с инструкцией
        start_button = settings.FONT.render('Чтобы начать нажмите проблем', True, settings.WHITE)
        # Создание поверхности с инструкцией
        end_surface = settings.FONT.render('Чтобы выйти из игры нажмите esc(escape)', True, settings.WHITE)
        # Отображение поверхности с инструкцией на экране
        self.screen.blit(end_surface, (30, 670))
        # Отображение заголовка по центру экрана
        self.screen.blit(title,
                         (settings.WIDTH / 2 - title.get_width() / 2, settings.HEIGTH / 2 -
                          title.get_height() / 2))
        # Отображение инструкции по центру экрана ниже заголовка
        self.screen.blit(start_button,
                         (settings.WIDTH / 2 - start_button.get_width() / 2, settings.HEIGTH / 2 +
                          start_button.get_height() / 2))
        # Обновление экрана, чтобы отобразить изменения
        pg.display.update()
