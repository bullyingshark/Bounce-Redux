import pygame
from game_constants import WHITE, BUTTON_HOVER


class Button:
    def __init__(self, x, y, image=None, hover_image=None, width=None, height=None, text=None, background_image=None):
        self.x = x
        self.y = y
        self.text = text
        self.hovered = False
        self.font = pygame.font.SysFont(None, 36)

        # For image buttons
        self.image = image
        self.hover_image = hover_image

        # For buttons with background image
        self.background_image = background_image

        # For text buttons
        if width is not None and height is not None:
            self.width = width
            self.height = height
            self.rect = pygame.Rect(x, y, width, height)
        elif image is not None:
            self.rect = self.image.get_rect(topleft=(x, y))
            self.width = self.rect.width
            self.height = self.rect.height
        else:
            raise ValueError("Either (width, height) or image must be provided")

    def draw(self, surface):
        if self.background_image:  # Button with background image and text
            # Scale background image to fit button size
            scaled_bg = pygame.transform.scale(self.background_image, (self.width, self.height))
            surface.blit(scaled_bg, self.rect)

            # Add a border when hovered
            if self.hovered:
                pygame.draw.rect(surface, BUTTON_HOVER, self.rect, 3)  # 3px border

            # Draw text if provided
            if self.text:
                text_surf = self.font.render(self.text, True, WHITE)
                text_rect = text_surf.get_rect(center=self.rect.center)
                surface.blit(text_surf, text_rect)

        elif self.image:  # Image button
            current_image = self.hover_image if self.hovered and self.hover_image else self.image
            surface.blit(current_image, self.rect)
        else:  # Text button
            # Draw button background
            button_color = BUTTON_HOVER if self.hovered else (150, 150, 250)
            pygame.draw.rect(surface, button_color, self.rect)
            pygame.draw.rect(surface, WHITE, self.rect, 2)  # Border

            # Draw text
            if self.text:
                text_surf = self.font.render(self.text, True, WHITE)
                text_rect = text_surf.get_rect(center=self.rect.center)
                surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click