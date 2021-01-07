import pygame


class Snake:
    def __init__(self):
        self.x, self.y = 400, 400
        self.x_shift = 0
        self.y_shift = 0

    def render(self):
        self.x += self.x_shift
        self.y += self.y_shift
        pygame.draw.rect(screen, 'white', (self.x, self.y, 10, 10))


if __name__ == '__main__':
    snake = Snake()
    pygame.init()
    fps = 60
    clock = pygame.time.Clock()
    pygame.display.set_caption('Змейка')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.y_shift = -10
                    snake.x_shift = 0
                if event.key == pygame.K_DOWN:
                    snake.y_shift = 10
                    snake.x_shift = 0
                if event.key == pygame.K_RIGHT:
                    snake.y_shift = 0
                    snake.x_shift = 10
                if event.key == pygame.K_LEFT:
                    snake.y_shift = 0
                    snake.x_shift = -10
        screen.fill('black')
        snake.render()
        clock.tick(fps)
        pygame.display.flip()
