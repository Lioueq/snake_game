import pygame
from random import randrange
import time
import pygame_gui

# необходимые переменные и константа в которой хранятся темы
THEMES = {'default': ['default', 'red', 'blue', 'black', 'white'],
          'anime': ['anime', 'red', 'brown', 'pink', 'white'],
          'ocean': ['ocean', 'orange', 'green', 'blue', 'white']}
music_play = True
difficulty = 'Легкий'
theme = THEMES['default']


class Snake:  # класс змеи
    def __init__(self, screen, clock):
        self.head_pos = [300, 300]
        self.body = [[300, 300]]
        self.x_move = 0
        self.y_move = 0
        self.length = 1
        self.screen = screen
        self.clock = clock

    def render(self):  # рисование змеи
        self.head_pos[0] += self.x_move
        self.head_pos[1] += self.y_move
        self.body.append([self.body[-1][0] + self.x_move, self.body[-1][1] + self.y_move])
        self.body = self.body[-self.length:]
        for i in self.body:
            pygame.draw.rect(self.screen, theme[1], (i[0], i[1], 10, 10))

    def body_groove(self):  # +1 к росту
        self.length += 1

    def crush_check(self):  # проверка на столконовение
        if self.body.count(self.head_pos) >= 2:
            return True
        if 0 > self.head_pos[0] or self.head_pos[0] >= 720 or 0 > self.head_pos[1] \
                or self.head_pos[1] >= 460:
            return True
        return False


class Food:  # класс еды
    def __init__(self, screen):
        self.x, self.y = randrange(0, 720, 10), randrange(0, 460, 10)
        self.screen = screen

    def render(self):  # рисование еды
        pygame.draw.rect(self.screen, theme[2], (self.x, self.y, 10, 10))

    def update(self):  # обновление позиции еды
        self.x, self.y = randrange(60, 720, 10), randrange(60, 460, 10)


def game_over(screen, clock, score, sound):  # смерть игрока
    # инициализация
    pygame.mixer.music.stop()
    sound.play()
    time.sleep(1)
    # проверка для проигрывания фоновой музыки
    if music_play:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('data/music2.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
    screen.fill(theme[3])
    text = ['GAME OVER', f'Итоговый счет равен: {score}']
    font = pygame.font.Font(None, 50)
    text_coord = 50
    # отображение текста
    for line in text:
        string_rendered = font.render(line, True, pygame.Color(theme[4]))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 175
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    # инициализация графического интерфейса
    manager = pygame_gui.UIManager((720, 460))
    play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(250, 200, 180, 40),
                                               text='Начать заново',
                                               manager=manager)
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(250, 300, 180, 40),
                                               text='Выйти в главное меню',
                                               manager=manager)
    run = True
    while run:  # основной цикл
        time_delta = clock.tick(25) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play_button:  # кнопка игры
                        new_game()
                    if event.ui_element == exit_button:  # кнопка выхода
                        main_window()
            manager.process_events(event)
        # рисование сцены
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()


def new_game():  # игровой процесс
    # инициализация
    direction = ''
    change_to = ''
    pygame.init()
    # уровень сложности
    if difficulty == 'Легкий':
        fps = 15
    elif difficulty == 'Средний':
        fps = 30
    else:
        fps = 60
    clock = pygame.time.Clock()
    pygame.display.set_caption('Змейка')
    size = 720, 460
    screen = pygame.display.set_mode(size)
    # проверка для проигрывания фоновой музыки
    if music_play:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('data/music.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
    sound1 = pygame.mixer.Sound('data/crush_sound.mp3')
    sound1.set_volume(0.5)
    sound2 = pygame.mixer.Sound('data/pick_up_sound.mp3')
    sound2.set_volume(0.5)
    running = True
    score = 0
    snake = Snake(screen, clock)
    food = Food(screen)
    food.render()
    font = pygame.font.Font(None, 50)
    # основной цикл
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                elif event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                elif event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
        # система движения
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
        if direction == 'UP':
            snake.y_move = -10
            snake.x_move = 0
        if direction == 'DOWN':
            snake.y_move = 10
            snake.x_move = 0
        if direction == 'LEFT':
            snake.x_move = -10
            snake.y_move = 0
        if direction == 'RIGHT':
            snake.x_move = 10
            snake.y_move = 0
        # Проверка на попадание в позицию еды
        if snake.head_pos[0] == food.x and snake.head_pos[1] == food.y:
            sound2.play()
            score += 1
            food.update()
            snake.body_groove()
        # рисование кадра
        screen.fill(theme[3])
        score_text = font.render(f'Счет: {score}', True, pygame.Color(theme[4]))
        screen.blit(score_text, (0, 0))
        snake.render()
        food.render()
        # проверка на столкновение
        if snake.crush_check():
            game_over(screen, clock, score, sound1)
        clock.tick(fps)
        pygame.display.flip()


def main_window(var=0):  # главное меню
    # инициализация
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Змейка')
    size = 720, 460
    main_window_screen = pygame.display.set_mode(size)
    main_window_screen.fill(theme[3])
    # проверка для проигрывания фоновой музыки
    if music_play and var != 1:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('data/music3.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
    # инициализация графического интерфейса
    manager = pygame_gui.UIManager(size)
    play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(300, 100, 100, 40),
                                               text='Начать игру',
                                               manager=manager)
    settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(300, 200, 100, 40),
                                                   text='Настройки',
                                                   manager=manager)
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(300, 300, 100, 40),
                                               text='Выйти',
                                               manager=manager)
    run = True
    while run:  # основной цикл
        time_delta = clock.tick(25) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play_button:  # кнопка начала игры
                        new_game()
                    if event.ui_element == settings_button:  # кнопка настроек
                        settings_window()
                    if event.ui_element == exit_button:  # кнопка выхода
                        exit()
            manager.process_events(event)
        # рисование сцены
        manager.update(time_delta)
        manager.draw_ui(main_window_screen)
        pygame.display.flip()


def settings_window():  # меню настроек
    # инициализация
    global music_play, difficulty, theme
    var = 1
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Настройки')
    size = 720, 460
    settings_screen = pygame.display.set_mode(size)
    # инициализация графического интерфейса
    s_manager = pygame_gui.UIManager(size)
    music_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(275, 200, 150, 40),
                                                text='Вкл/выкл музыку',
                                                manager=s_manager)
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(250, 400, 200, 40),
                                               text='Выйти в главное меню',
                                               manager=s_manager)
    s_difficulty = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=['Легкий', 'Средний', 'Сложный'],
                                                                        starting_option=difficulty,
                                                                        relative_rect=pygame.Rect(275, 100, 150, 40),
                                                                        manager=s_manager)
    s_theme = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(options_list=['default', 'anime', 'ocean'],
                                                                   starting_option=theme[0],
                                                                   relative_rect=pygame.Rect(275, 300, 150, 40),
                                                                   manager=s_manager)
    run = True
    while run:  # основной цикл
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == exit_button:  # кнопка выхода
                        main_window(var)
                    if event.ui_element == music_button:  # кнопка проигрывания музыки
                        if music_play:
                            var = 0
                            music_play = False
                            pygame.mixer.music.stop()
                        else:
                            var = 1
                            music_play = True
                            pygame.mixer.music.play()
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == s_difficulty:  # смена сложности
                        difficulty = event.text
                    if event.ui_element == s_theme:  # смена темы
                        theme = THEMES[event.text]
            s_manager.process_events(event)
        # рисование сцены
        settings_screen.fill(theme[3])
        s_manager.update(time_delta)
        s_manager.draw_ui(settings_screen)
        pygame.display.flip()


if __name__ == '__main__':
    main_window()
