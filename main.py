import random

import sys

import pygame as pg

import menu
import quiz
import settings
import button
from enum import Enum


# Определение перечисления для состояний игры
class GameState(Enum):
    START_MENU = 1
    GAME = 2


class Game:
    def __init__(self):
        # Инициализация Pygame
        pg.init()
        # Создание окна игры с заданными размерами
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGTH), pg.RESIZABLE)
        pg.display.set_caption('Quiz Game')
        # Создание часов Pygame для контроля FPS
        self.clock = pg.time.Clock()
        # Изначальное состояние игры - "start_menu"
        self.game_state = GameState.START_MENU
        # Создание объектов меню, викторины и кнопки
        self.menu = menu.Menu(self.screen)
        self.quiz = quiz.Quiz(self.screen)
        self.button = button.Button(self.screen)

        self.number_of_question = 0
        self.score = 0
        self.error = 0
        self.count = 0

    def start_menu(self):
        """
        Данный метод отображает стартовое меню. Если состояние игры равно "start_menu" и нажата клавиша пробел,
        игра переходит в состояние "game".
        """
        if self.game_state == GameState.START_MENU:
            # Отрисовка стартового меню
            self.menu.draw_start_menu()
            # Проверка, была ли нажата клавиша пробела для начала игры
            if pg.key.get_pressed()[pg.K_SPACE]:
                self.game_state = GameState.GAME

    def start_game(self):
        """
        Данный метод отвечает за начало игры. Внутри метода происходит обработка событий, проверка клавиш и
        отображение игровых элементов. В зависимости от действий игрока (нажатие кнопки, ввод ответа и т.д.)
        обновляются значения счета, ошибок и других параметров игры. Если сделано 3 ошибки, игра завершается.
        """
        # Генерация случайного номера вопроса для викторины
        self.number_of_question = random.randint(0, 29375)
        if self.game_state == GameState.GAME:
            # Инициализация переменных для подсчета очков и ошибок
            self.score, self.count, self.error = 0, 0, 0
            # Отображение текущего счета и числа ошибок
            self.quiz.score += str(self.score)
            self.quiz.error = 'Ошибок: ' + str(self.error) + '/3'
            while True:
                self.check_events()

    def run(self):
        """
        Данный метод является основным циклом игры. Он вызывает другие методы для проверки событий, отображения
        стартового меню и запуска игры.
        """
        while True:
            self.check_events()
            self.start_menu()
            self.screen.fill(settings.COLOR_BACKGROUND)
            self.start_game()

    def check_events(self):
        """
        Данный метод проверяет события в игре. Если происходит событие выхода из игры (нажатие крестика или клавиши
        ESC), игра завершается.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
                # Если происходит событие выхода из игры (нажатие крестика или клавиши ESC), завершаем игру
                pg.quit()
                sys.exit()
            if self.game_state == GameState.GAME:
                if self.button.active:
                    # Генерация нового номера вопроса и обновление экрана
                    self.number_of_question = random.randint(0, 29375)
                    pg.display.update()
                    # Увеличение счетчика вопросов
                    self.count += 1
                    # Проверка правильности ответа и обновление счета и числа ошибок
                    if self.quiz.answer_text.lower() == self.quiz.text.lower():
                        self.score += 1
                        self.quiz.score = 'Очки: ' + str(self.score)
                        self.quiz.blit_text(self.quiz.score, (1100, 670), settings.WHITE)
                    else:
                        self.error += 1
                        self.quiz.error = 'Ошибок: ' + str(self.error) + '/3'
                        self.quiz.blit_text(self.quiz.error, (1090, 600), settings.WHITE)
                        # Если количество ошибок достигло 3, выход из игры
                        if self.error == 3:
                            pg.quit()
                            sys.exit()
                    self.quiz.text = ''
                    self.quiz.txt_surface = settings.FONT.render(self.quiz.text, True, self.quiz.color)
                    self.button.active = False

                pg.display.update()
                self.quiz.handle_event(event)
                self.button.press(event)
                self.quiz.update()
                self.screen.fill(settings.COLOR_BACKGROUND)
                self.quiz.game(self.number_of_question)
                self.quiz.draw()
                self.button.draw()
                pg.display.flip()
                self.clock.tick(settings.FPS)
                pg.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
