import pygame
from game_constants import COIN_WIDTH, COIN_HEIGHT, YELLOW


class Coin:
    def __init__(self, x, y, width=None, height=None, image=None):
        self.pos = [x, y]
        self.width = width if width is not None else COIN_WIDTH
        self.height = height if height is not None else COIN_HEIGHT
        self.collected = False

        # Устанавливаем изображение
        if image:
            self.image = pygame.transform.scale(image, (self.width, self.height))
        else:
            # Создаем изображение по умолчанию
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(YELLOW)
            # Добавляем простой узор для монеты
            center_x, center_y = self.width // 2, self.height // 2
            radius = min(self.width, self.height) // 3
            pygame.draw.circle(self.image, (255, 255, 150), (center_x, center_y), radius)

    def get_rect(self):
        """Возвращает прямоугольник для проверки коллизий"""
        return pygame.Rect(
            self.pos[0] - self.width // 2,
            self.pos[1] - self.height // 2,
            self.width,
            self.height
        )

    def draw(self, surface, camera_x, camera_y=0):
        """Отрисовывает монету на экране"""
        if not self.collected:
            screen_x = self.pos[0] - camera_x - self.width // 2
            screen_y = self.pos[1] - camera_y - self.height // 2

            # Проверяем, находится ли монета в пределах экрана
            if (-self.width <= screen_x <= surface.get_width() and
                    -self.height <= screen_y <= surface.get_height()):
                surface.blit(self.image, (screen_x, screen_y))

    def collect(self):
        """Собирает монету"""
        self.collected = True
        return True

    def is_collected(self):
        """Проверяет, собрана ли монета"""
        return self.collected

    def reset(self):
        """Сбрасывает состояние монеты"""
        self.collected = False