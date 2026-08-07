import pygame
from game_constants import TILE_SIZE, GRAVITY, JUMP_POWER, MOVE_SPEED, RED


class Player:
    def __init__(self, x, y, image):
        self.pos = [x, y]
        self.initial_pos = [x, y]  # Сохраняем начальную позицию
        self.vel = [0, 0]
        self.image = image
        self.on_ground = False
        self.lives = 3  # Добавляем счетчик жизней
        self.invulnerable = False  # Флаг неуязвимости после получения урона
        self.invulnerable_timer = 0  # Таймер неуязвимости
        self.flash_timer = 0  # Для мигания при неуязвимости
        self.flashing = False  # Состояние мигания

    def update(self, platforms):
        # Гравитация
        self.vel[1] += GRAVITY
        self.pos[1] += self.vel[1]

        # Получаем прямоугольник игрока для проверки коллизий
        player_rect = self.get_rect()

        # Сброс статуса на земле
        self.on_ground = False

        # Проверка столкновений с платформами
        for platform in platforms:
            if player_rect.colliderect(platform):
                # Падение на платформу сверху
                if self.vel[1] > 0 and player_rect.bottom - platform.top <= TILE_SIZE:
                    self.pos[1] = platform.top - TILE_SIZE // 2
                    self.vel[1] = 0
                    self.on_ground = True
                # Прыжок в платформу снизу
                elif self.vel[1] < 0 and platform.bottom - player_rect.top <= TILE_SIZE:
                    self.pos[1] = platform.bottom + TILE_SIZE // 2
                    self.vel[1] = 0
                # Столкновение сбоку
                elif player_rect.right - platform.left <= 5 and player_rect.right > platform.left:
                    self.pos[0] = platform.left - TILE_SIZE // 2
                elif platform.right - player_rect.left <= 5 and player_rect.left < platform.right:
                    self.pos[0] = platform.right + TILE_SIZE // 2

        # Обновление состояния неуязвимости
        if self.invulnerable:
            self.invulnerable_timer -= 1
            self.flash_timer -= 1

            if self.flash_timer <= 0:
                self.flashing = not self.flashing
                self.flash_timer = 5  # Скорость мигания

            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                self.flashing = False

    def move(self, direction):
        self.pos[0] += direction * MOVE_SPEED

    def jump(self):
        if self.on_ground:
            self.vel[1] = JUMP_POWER
            self.on_ground = False

    def get_rect(self):
        return pygame.Rect(
            self.pos[0] - TILE_SIZE // 2,
            self.pos[1] - TILE_SIZE // 2,
            TILE_SIZE,
            TILE_SIZE
        )

    def draw(self, surface, camera_x):
        screen_x = self.pos[0] - camera_x

        # Если неуязвим и должен мигать, не отрисовываем
        if self.invulnerable and self.flashing:
            return

        surface.blit(self.image, (screen_x - TILE_SIZE // 2, self.pos[1] - TILE_SIZE // 2))

    def collides_with(self, rect):
        return self.get_rect().colliderect(rect)

    def take_damage(self):
        # Если игрок не неуязвим, уменьшаем количество жизней
        if not self.invulnerable:
            self.lives -= 1
            self.invulnerable = True
            self.invulnerable_timer = 90  # ~1.5 секунды неуязвимости при 60 FPS
            return True
        return False

    def is_dead(self):
        return self.lives <= 0

    # Добавляем метод для возврата на начальную позицию
    def reset_position(self):
        self.pos = self.initial_pos.copy()
        self.vel = [0, 0]