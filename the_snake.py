import sys
from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BLACK_COLOR = (0, 0, 0)

BOARD_BACKGROUND_COLOR = BLACK_COLOR

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

MAX_ATTEMPTS = 1000

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Общий класс для всех игровых объектов."""

    def __init__(self, position=SCREEN_CENTER, body_color=BLACK_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод заглушка."""

    def draw_rect(self, position):
        """Метод отрисовки клетки."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс игрового объекта яблоко."""

    def __init__(self, position=None, body_color=APPLE_COLOR):
        super().__init__(position, body_color)
        self.randomize_position()

    def randomize_position(self, positions=None):
        """Метод для рандома позиции яблока."""
        max_attempts = MAX_ATTEMPTS
        for _ in range(max_attempts):
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position = (x, y)
            # Проверка на то, что яблоко не окажется внутри змейки при спавне
            if positions is None or position not in positions:
                self.position = position
                return

        raise RuntimeError('Не удалось разместить яблоко.')

    def draw(self):
        """Метод, отвечающий за отрисовку яблока."""
        self.draw_rect(self.position)


class Snake(GameObject):
    """Класс игрового объекта змейка."""

    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR,
                 lenght=1, direction=RIGHT):
        super().__init__(position, body_color)
        self.length = lenght
        self.positions = [self.position]
        self.direction = direction
        self.next_direction = None
        self.last = None

    def get_head_position(self) -> tuple:
        """Метод, возвращающий положение головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод, отвечающий за движение змейки."""
        dx, dy = self.direction
        sx, sy = self.get_head_position()
        self.positions.insert(
            0,
            (
                (sx + (dx * GRID_SIZE)) % SCREEN_WIDTH,
                (sy + (dy * GRID_SIZE)) % SCREEN_HEIGHT,
            ),
        )

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def update_direction(self):
        """Метод, изменяющий напрвление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Метод, отрисовывабщий змейку."""
        for position in self.positions[:-1]:
            self.draw_rect(position)
        # Отрисовка головы змейки
        self.draw_rect(self.get_head_position())
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Метод, сбрасывающий змейку в исходное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Функция, считывающая нажатие 'стрелочек' на клавиатуре."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция."""
    pg.init()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[3:]:
            with open('scores.txt', 'a', encoding='utf-8') as f:
                f.write(f'Счёт {snake.length}')

            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position()

        elif snake.get_head_position() == apple.position:
            apple.randomize_position(snake.positions)
            snake.length += 1

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
