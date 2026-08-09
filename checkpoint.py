import pygame
from game_constants import CHECKPOINT_SIZE

class Checkpoint:
    def __init__(self, x, y, inactive_image=None, active_image=None):
        self.pos = [x, y]
        self.is_active = False
        self.inactive_image = inactive_image
        self.active_image = active_image

        # Default size is smaller than tile size
        self.size = CHECKPOINT_SIZE

    def get_rect(self):
        return pygame.Rect(
            self.pos[0] - self.size // 2,
            self.pos[1] - self.size // 2,
            self.size,
            self.size
        )

    def activate(self):
        self.is_active = True

    def draw(self, surface, camera_x):
        screen_x = self.pos[0] - camera_x
        # Only draw if within screen bounds
        if 0 <= screen_x <= surface.get_width() + self.size:
            image = self.active_image if self.is_active else self.inactive_image
            if image:
                # Scale the image to be square and the correct size
                scaled_image = pygame.transform.scale(image, (self.size, self.size))
                surface.blit(scaled_image, (screen_x - self.size // 2, self.pos[1] - self.size // 2))
            else:
                # Fallback rendering if images aren't available
                color = (0, 255, 0) if self.is_active else (255, 165, 0)  # Green if active, orange if not
                pygame.draw.rect(
                    surface,
                    color,
                    (screen_x - self.size // 2, self.pos[1] - self.size // 2, self.size, self.size)
                )
                # Draw a flag on top
                flag_color = (255, 255, 255)
                pygame.draw.polygon(
                    surface,
                    flag_color,
                    [
                        (screen_x - self.size // 4, self.pos[1] - self.size // 3),
                        (screen_x + self.size // 4, self.pos[1] - self.size // 4),
                        (screen_x - self.size // 4, self.pos[1] - self.size // 6)
                    ]
                )
                # Draw the pole
                pygame.draw.rect(
                    surface,
                    (100, 100, 100),
                    (screen_x - self.size // 4, self.pos[1] - self.size // 2, 4, self.size)
                )