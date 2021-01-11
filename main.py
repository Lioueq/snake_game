import pygame
from random import randrange
import time
import pygame_gui


class Snake:
    def __init__(self, screen, clock):
        self.head_pos = [300, 300]
        self.body = [[300, 300]]
        self.x_move = 0
        self.y_move = 0
        self.length = 1
        self.screen = screen
        self.clock = clock

    def render(self):
        self.head_pos[0] += self.x_move
        self.head_pos[1] += self.y_move
        self.body.append([self.body[-1][0] + self.x_move, self.body[-1][1] + self.y_move])
        self.body = self.body[-self.length:]
        for i in self.body:
            pygame.draw.rect(self.screen, 'red', (i[0], i[1], 10, 10))

    def body_groove(self):
        self.length += 1

    def crush_check(self):
        if self.body.count(self.head_pos) >= 2:
            return True
        if 0 > self.head_pos[0] or self.head_pos[0] >= 720 or 0 > self.head_pos[1] \
                or self.head_pos[1] >= 460:
            return True
        return False


class Food:
    def __init__(self, screen):
        self.x, self.y = randrange(0, 720, 10), randrange(0, 460, 10)
        self.screen = screen

    def render(self):
        pygame.draw.rect(self.screen, 'blue', (self.x, self.y, 10, 10))

    def update(self):
        self.x, self.y = randrange(60, 720, 10), randrange(60, 460, 10)


def game_over(screen, clock, score, sound):
    pygame.mixer.music.stop()
    pygame.mixer.music.load('data/music2.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    sound.play()
    time.sleep(1)
    screen.fill('white')
    text = ['GAME OVER', f'Итоговый счет равен: {score}', 'Нажмите R чтобы начать заново',
            'Нажмите T чтобы выйти в главное меню', 'Нажмите ESC чтобы выйти']
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    new_game()
                if event.key == pygame.K_t:
                    main_window()
                if event.key == pygame.K_ESCAPE:
                    exit()
        pygame.display.flip()
        clock.tick(25)


def new_game():
    pygame.init()
    fps = 25
    clock = pygame.time.Clock()
    pygame.display.set_caption('Змейка')
    size = 720, 460
    screen = pygame.display.set_mode(size)
    pygame.mixer.music.stop()
    pygame.mixer.music.load('data/music.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    sound1 = pygame.mixer.Sound('data/crush_sound.mp3')
    sound1.set_volume(0.5)
    sound2 = pygame.mixer.Sound('data/pick_sound.mp3')
    sound2.set_volume(0.5)
    running = True
    score = 0
    snake = Snake(screen, clock)
    food = Food(screen)
    food.render()
    font = pygame.font.Font(None, 50)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.y_move != 10:
                    snake.y_move = -10
                    snake.x_move = 0
                elif event.key == pygame.K_DOWN and snake.y_move != -10:
                    snake.y_move = 10
                    snake.x_move = 0
                elif event.key == pygame.K_RIGHT and snake.x_move != -10:
                    snake.y_move = 0
                    snake.x_move = 10
                elif event.key == pygame.K_LEFT and snake.x_move != 10:
                    snake.y_move = 0
                    snake.x_move = -10
        if snake.head_pos[0] == food.x and snake.head_pos[1] == food.y:
            sound2.play()
            score += 1
            food.update()
            snake.body_groove()
        if snake.crush_check():
            game_over(screen, clock, score, sound1)
        screen.fill('black')
        score_text = font.render(f'Счет: {score}', True, pygame.Color('white'))
        screen.blit(score_text, (0, 0))
        snake.render()
        food.render()
        clock.tick(fps)
        pygame.display.flip()


def main_window():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Змейка')
    size = 720, 460
    main_window_screen = pygame.display.set_mode(size)
    pygame.mixer.music.stop()
    pygame.mixer.music.load('data/music3.mp3')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
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
    while run:
        time_delta = clock.tick(25) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play_button:
                        new_game()
                    if event.ui_element == settings_button:
                        settings_window()
                    if event.ui_element == exit_button:
                        exit()
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(main_window_screen)
        pygame.display.flip()


def settings_window():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Настройки')
    size = 720, 460
    settings_screen = pygame.display.set_mode(size)
    s_manager = pygame_gui.UIManager(size)
    music_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(275, 100, 150, 40),
                                                text='Вкл/выкл музыку',
                                                manager=s_manager)
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(250, 400, 200, 40),
                                               text='Выйти в главное меню',
                                               manager=s_manager)
    run = True
    while run:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == exit_button:
                        main_window()
                    if event.ui_element == music_button:
                        pass
            s_manager.process_events(event)
        s_manager.update(time_delta)
        s_manager.draw_ui(settings_screen)
        pygame.display.flip()


if __name__ == '__main__':
    main_window()
