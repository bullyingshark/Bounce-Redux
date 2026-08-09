import pygame
from game_constants import TILE_SIZE, RED, GREEN, ENEMY_S_WIDTH, ENEMY_S_HEIGHT, ENEMY_M_WIDTH, ENEMY_M_HEIGHT


class Enemy:
    def __init__(self, x, y, image=None, enemy_type="static"):
        self.pos = [x, y]
        self.enemy_type = enemy_type

        # Set the dimensions based on enemy type
        if enemy_type == "static":
            self.width = ENEMY_S_WIDTH
            self.height = ENEMY_S_HEIGHT
        else:
            self.width = ENEMY_M_WIDTH
            self.height = ENEMY_M_HEIGHT

        # Create an image of the enemy if one has not been provided
        if image:
            self.image = image
        else:
            # Stationary enemy - red square; that moves - green
            color = RED if enemy_type == "static" else GREEN
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(color)

            # Add details to help distinguish between enemies
            if enemy_type == "static":
                # Draw an X on a stationary enemy
                pygame.draw.line(self.image, (0, 0, 0), (0, 0), (self.width, self.height), 2)
                pygame.draw.line(self.image, (0, 0, 0), (0, self.height), (self.width, 0), 2)
            else:
                # Drawing arrows on a moving enemy
                pygame.draw.line(self.image, (0, 0, 0), (self.width // 2, 5), (self.width // 2, self.height - 5), 2)
                pygame.draw.polygon(self.image, (0, 0, 0),
                                    [(self.width // 2 - 5, 10), (self.width // 2, 5), (self.width // 2 + 5, 10)])
                pygame.draw.polygon(self.image, (0, 0, 0),
                                    [(self.width // 2 - 5, self.height - 10), (self.width // 2, self.height - 5),
                                     (self.width // 2 + 5, self.height - 10)])

    def get_rect(self):
        return pygame.Rect(
            self.pos[0] - self.width // 2,
            self.pos[1] - self.height // 2,
            self.width,
            self.height
        )

    def draw(self, surface, camera_x, camera_y=0):
        screen_x = self.pos[0] - camera_x
        screen_y = self.pos[1] - camera_y

        # Only render if the enemy is within the screen boundaries
        if (0 <= screen_x <= surface.get_width() + self.width and
                0 <= screen_y <= surface.get_height() + self.height):
            surface.blit(self.image, (screen_x - self.width // 2, screen_y - self.height // 2))


class MovingEnemy(Enemy):
    def __init__(self, x, y, move_distance, speed=1, image=None, vertical=True):
        super().__init__(x, y, image, "moving")
        self.initial_x = x
        self.initial_y = y
        self.move_distance = move_distance  # Max move distance up/down or left/right
        self.speed = speed  # Speed
        self.direction = 1  # 1 - down/right, -1 - up/left
        self.vertical = vertical  # Vertical movement by default

    def update(self):
        if self.vertical:
            # Updating the position vertically
            self.pos[1] += self.speed * self.direction

            # Change direction when we reach the end points
            if self.pos[1] >= self.initial_y + self.move_distance:
                self.direction = -1
            elif self.pos[1] <= self.initial_y - self.move_distance:
                self.direction = 1
        else:
            # Updating the position horizontally
            self.pos[0] += self.speed * self.direction

            # Change direction when reaching the end points
            if self.pos[0] >= self.initial_x + self.move_distance:
                self.direction = -1
            elif self.pos[0] <= self.initial_x - self.move_distance:
                self.direction = 1