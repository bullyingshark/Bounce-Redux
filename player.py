import pygame
from game_constants import TILE_SIZE, GRAVITY, JUMP_POWER, MOVE_SPEED, RED


class Player:
    def __init__(self, x, y, image):
        self.pos = [x, y]
        self.initial_pos = [x, y]
        self.checkpoint_pos = None
        self.vel = [0, 0]
        self.image = image
        self.on_ground = False
        self.lives = 3
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.flash_timer = 0
        self.flashing = False

    def update(self, platforms):
        # Применяем гравитацию
        self.vel[1] += GRAVITY

        # Перемещение по оси X
        self.pos[0] += self.vel[0]
        self.vel[0] = 0  # Сброс движения по X после перемещения
        player_rect = self.get_rect()
        for platform in platforms:
            if player_rect.colliderect(platform):
                if self.pos[0] < platform.left:
                    self.pos[0] = platform.left - TILE_SIZE // 2
                elif self.pos[0] > platform.right:
                    self.pos[0] = platform.right + TILE_SIZE // 2
                player_rect = self.get_rect()

        # Перемещение по оси Y
        self.pos[1] += self.vel[1]
        player_rect = self.get_rect()
        self.on_ground = False
        for platform in platforms:
            if player_rect.colliderect(platform):
                if self.vel[1] > 0:
                    self.pos[1] = platform.top - TILE_SIZE // 2
                    self.vel[1] = 0
                    self.on_ground = True
                elif self.vel[1] < 0:
                    self.pos[1] = platform.bottom + TILE_SIZE // 2
                    self.vel[1] = 0
                player_rect = self.get_rect()

        # Обновление состояния неуязвимости
        if self.invulnerable:
            self.invulnerable_timer -= 1
            self.flash_timer -= 1

            if self.flash_timer <= 0:
                self.flashing = not self.flashing
                self.flash_timer = 5

            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                self.flashing = False

    def move(self, direction):
        self.vel[0] = direction * MOVE_SPEED

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

    def draw(self, surface, camera_x, camera_y=0):
        screen_x = self.pos[0] - camera_x
        screen_y = self.pos[1] - camera_y

        if self.invulnerable and self.flashing:
            return

        surface.blit(self.image, (screen_x - TILE_SIZE // 2, screen_y - TILE_SIZE // 2))

    def collides_with(self, rect):
        return self.get_rect().colliderect(rect)

    def take_damage(self):
        if not self.invulnerable:
            self.lives -= 1
            self.invulnerable = True
            self.invulnerable_timer = 90
            return True
        return False

    def is_dead(self):
        return self.lives <= 0

    def reset_position(self):
        """Сбрасывает позицию на начальную точку"""
        self.pos = self.initial_pos.copy()
        self.vel = [0, 0]

    def reset_to_checkpoint(self, checkpoint_pos):
        """Сбрасывает позицию на активную контрольную точку"""
        self.pos = checkpoint_pos.copy()
        self.vel = [0, 0]