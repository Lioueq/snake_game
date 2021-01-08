import pygame
from random import randrange


class Snake:
    def __init__(self):
        self.head_pos = [300, 300]
        self.body = [[300, 300]]
        self.x_move = 10
        self.y_move = 0
        self.length = 1

    def render(self):
        self.head_pos[0] += self.x_move
        self.head_pos[1] += self.y_move
        self.body.append([self.body[-1][0] + self.x_move, self.body[-1][1] + self.y_move])
        self.body = self.body[-self.length:]
        for i in self.body:
            pygame.draw.rect(screen, 'red', (i[0], i[1], 8, 8))

    def body_groove(self):
        self.length += 1
        print(len(self.body))


class Food:
    def __init__(self):
        self.x, self.y = randrange(0, 720, 10), randrange(0, 460, 10)

    def render(self):
        pygame.draw.rect(screen, 'brown', (self.x, self.y, 10, 10))

    def update(self):
        self.x, self.y = randrange(0, 720, 10), randrange(0, 460, 10)


snake = Snake()
food = Food()
pygame.init()
fps = 60
clock = pygame.time.Clock()
pygame.display.set_caption('Змейка')
size = width, height = 720, 460
screen = pygame.display.set_mode(size)
running = True
food.render()
font = pygame.font.Font(None, 50)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.y_move = -10
                snake.x_move = 0
            if event.key == pygame.K_DOWN:
                snake.y_move = 10
                snake.x_move = 0
            if event.key == pygame.K_RIGHT:
                snake.y_move = 0
                snake.x_move = 10
            if event.key == pygame.K_LEFT:
                snake.y_move = 0
                snake.x_move = -10
    if snake.head_pos[0] == food.x and snake.head_pos[1] == food.y:
        food.update()
        snake.body_groove()
    screen.fill('black')
    snake.render()
    food.render()
    clock.tick(fps)
    pygame.display.flip()
