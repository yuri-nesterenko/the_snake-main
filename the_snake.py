from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Словарь для навигации
DIRECTION_MAPPING = {
    (LEFT, pygame.K_UP): UP,
    (LEFT, pygame.K_DOWN): DOWN,
    (RIGHT, pygame.K_UP): UP,
    (RIGHT, pygame.K_DOWN): DOWN,
    (UP, pygame.K_LEFT): LEFT,
    (UP, pygame.K_RIGHT): RIGHT,
    (DOWN, pygame.K_LEFT): LEFT,
    (DOWN, pygame.K_RIGHT): RIGHT,
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 215, 0)

# Цвет змейки
SNAKE_COLOR = (178, 223, 138)

# Цвет камней
STONE_COLOR = (139, 69, 19)

# Скорость движения змейки:
SPEED = 15

# Количество камней на поле:
STONE_COUNT = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка-камнеломка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Исходный класс для всех объектов."""

    def __init__(self, position: tuple[int, int] = None):
        """Инициализирует объект с заданной позицией."""
        self.position = position if position else (
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self, surface: pygame.Surface):
        """Абстрактный метод для отрисовки объекта."""


class Apple(GameObject):
    """Класс для съедобного яблока(бонус)"""

    def __init__(self, stones: list = None):
        """Инициализирует яблоко со случайной позицией."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.stones = stones if stones is not None else []
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию для яблока."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if not any(
                self.position == stone.position for stone in self.stones
            ):
                break

    def draw(self, surface: pygame.Surface = None):
        """Отрисовывает яблоко на игровом поле."""
        surface = surface or screen
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, APPLE_COLOR, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Stone(GameObject):
    """Класс для камня."""

    def __init__(self, existing_positions: list = None):
        """Инициализирует камень со случайной позицией."""
        super().__init__()
        self.body_color = STONE_COLOR
        self.existing_positions = (
            existing_positions if existing_positions else []
        )
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию для камня."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in self.existing_positions:
                break

    def draw(self, surface: pygame.Surface = None):
        """Отрисовывает камень на игровом поле."""
        surface = surface or screen
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, STONE_COLOR, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self, stones: list = None):
        """Инициализирует змейку на стартовой позиции."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.stones = stones if stones is not None else []
        self.reset()
        self.last = None

    def reset(self):
        """Перезагружает змейку на стартовую позицию и шафлит камни."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        for stone in self.stones:
            stone.randomize_position()

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)

        self.positions.insert(0, new_position)
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def draw(self, surface: pygame.Surface = None):
        """Отрисовывает змейку на игровом поле."""
        surface = surface or screen
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, SNAKE_COLOR, rect)
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect, 1)

        head_rect = pygame.Rect(
            self.get_head_position(), (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, SNAKE_COLOR, head_rect)
        pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake: Snake) -> bool:
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        elif event.type == pygame.KEYDOWN:
            new_dir = DIRECTION_MAPPING.get((snake.direction, event.key))
            if new_dir is not None:
                snake.next_direction = new_dir
    return True


def main():
    """Основная функция инициализации игры"""
    pygame.init()

    stones = [Stone() for _ in range(STONE_COUNT)]
    snake = Snake(stones)
    apple = Apple(stones)

    while any(apple.position == stone.position for stone in stones):
        apple.randomize_position()

    running = True
    while running:
        clock.tick(SPEED)

        running = handle_keys(snake)
        if not running:
            break

        snake.update_direction()
        snake.move()

        head_pose = snake.get_head_position()
        if (
            head_pose in snake.positions[1:]
            or any(head_pose == stone.position for stone in stones)
        ):
            pygame.time.delay(500)

            stones = [Stone() for _ in range(STONE_COUNT)]
            snake = Snake(stones)
            apple = Apple(stones)

            while any(apple.position == stone.position for stone in stones):
                apple.randomize_position()

            continue

        if head_pose == apple.position:
            snake.length += 1
            apple.randomize_position()
            while (
                apple.position in snake.positions
                or any(apple.position == stone.position for stone in stones)
            ):
                apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        for stone in stones:
            stone.draw()
        apple.draw()
        snake.draw()
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
