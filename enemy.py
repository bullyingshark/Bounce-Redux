import pygame
from game_constants import TILE_SIZE, RED, GREEN, ENEMY_WIDTH, ENEMY_HEIGHT


class Enemy:
    def __init__(self, x, y, image=None, enemy_type="static"):
        self.pos = [x, y]
        self.enemy_type = enemy_type

        # Создаем изображение врага, если оно не предоставлено
        if image:
            self.image = image
        else:
            # Статичный враг - красный квадрат, движущийся - зеленый
            color = RED if enemy_type == "static" else GREEN
            self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
            self.image.fill(color)

            # Добавляем детали для различения врагов
            if enemy_type == "static":
                # Рисуем X на статичном враге
                pygame.draw.line(self.image, (0, 0, 0), (0, 0), (ENEMY_WIDTH, ENEMY_HEIGHT), 2)
                pygame.draw.line(self.image, (0, 0, 0), (0, ENEMY_HEIGHT), (ENEMY_WIDTH, 0), 2)
            else:
                # Рисуем стрелки на движущемся враге
                pygame.draw.line(self.image, (0, 0, 0), (ENEMY_WIDTH // 2, 5), (ENEMY_WIDTH // 2, ENEMY_HEIGHT - 5), 2)
                pygame.draw.polygon(self.image, (0, 0, 0),
                                   [(ENEMY_WIDTH // 2 - 5, 10), (ENEMY_WIDTH // 2, 5), (ENEMY_WIDTH // 2 + 5, 10)])
                pygame.draw.polygon(self.image, (0, 0, 0),
                                   [(ENEMY_WIDTH // 2 - 5, ENEMY_HEIGHT - 10), (ENEMY_WIDTH // 2, ENEMY_HEIGHT - 5),
                                    (ENEMY_WIDTH // 2 + 5, ENEMY_HEIGHT - 10)])

    def get_rect(self):
        return pygame.Rect(
            self.pos[0] - ENEMY_WIDTH // 2,
            self.pos[1] - ENEMY_HEIGHT // 2,
            ENEMY_WIDTH,
            ENEMY_HEIGHT
        )

    def draw(self, surface, camera_x):
        screen_x = self.pos[0] - camera_x
        # Отрисовываем, только если враг находится в пределах экрана
        if 0 <= screen_x <= surface.get_width() + ENEMY_WIDTH:
            surface.blit(self.image, (screen_x - ENEMY_WIDTH // 2, self.pos[1] - ENEMY_HEIGHT // 2))


class MovingEnemy(Enemy):
    def __init__(self, x, y, move_distance, speed=1, image=None):
        super().__init__(x, y, image, "moving")
        self.initial_y = y
        self.move_distance = move_distance  # Максимальное расстояние движения вверх/вниз
        self.speed = speed  # Скорость движения
        self.direction = 1  # 1 - вниз, -1 - вверх

    def update(self):
        # Обновляем позицию
        self.pos[1] += self.speed * self.direction

        # Меняем направление при достижении крайних точек
        if self.pos[1] >= self.initial_y + self.move_distance:
            self.direction = -1
        elif self.pos[1] <= self.initial_y - self.move_distance:
            self.direction = 1