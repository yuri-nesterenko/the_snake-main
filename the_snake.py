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
        pass


class Apple(GameObject):
    """Класс для съедобного яблока(бонус)"""

    def __init__(self, stones: list = None):
        """Инициализирует яблоко со случайной позицией."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.stones = stones if stones else []
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
        self.stones = stones if stones else []
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
        if (
            new_position in self.positions[:-1]
            or any(new_position == stone.position for stone in self.stones)
        ):
            self.reset()
            return False

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

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
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
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
    return True


def main():
    """Основная функция инициализации игры"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Змейка-камнеломка')
    clock = pygame.time.Clock()

    stones = [Stone() for _ in range(20)]
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
        if not snake.move():
            continue

        if snake.get_head_position() == apple.position:
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
