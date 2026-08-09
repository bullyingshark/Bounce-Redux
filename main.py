import pygame
import sys
import os
from game_constants import *
from level_manager import LevelManager
from button import Button
from game import Game

# Init Pygame
pygame.init()

# Window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bounce")
clock = pygame.time.Clock()

# Creating a level manager
level_manager = LevelManager()

# Main menu
def main_menu():
    menu_running = True

    # Uploading images
    try:
        play_img = pygame.image.load("img/menu_button_play@2x.png")
        levels_img = pygame.image.load("img/menu_button_levels@2x.png")
        left_image = pygame.image.load("img/menu_logo@2x.png")
    except pygame.error as e:
        print(f"Error loading menu images: {e}")
        # Fallback to text buttons if images can't be loaded
        play_img = None
        levels_img = None
        left_image = None

    # Creating buttons
    if play_img:
        play_button = Button(SCREEN_WIDTH // 2 + 150, 100, image=play_img)
    else:
        play_button = Button(SCREEN_WIDTH // 2 + 50, 100, width=200, height=50, text="PLAY")

    # Add button Levels
    if levels_img:
        levels_button = Button(SCREEN_WIDTH // 2 + 150, 200, image=levels_img)
    else:
        levels_button = Button(SCREEN_WIDTH // 2 + 50, 200, width=200, height=50, text="LEVELS")

    # Obtain a Rect for the left-hand image and position it
    if left_image:
        left_image_rect = left_image.get_rect(topright=(SCREEN_WIDTH // 2 - 150, 200))

    while menu_running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True

        # Cursor alignment check
        play_button.check_hover(mouse_pos)
        levels_button.check_hover(mouse_pos)

        # Checking the click on the Play button
        if play_button.is_clicked(mouse_pos, mouse_click):
            # Start the first level
            if level_manager.get_level_count() > 0:
                game = Game(screen, clock, level_manager)
                game.run(0)

        # Testing the “Levels” button
        if levels_button.is_clicked(mouse_pos, mouse_click):
            # Level selection menu
            level_select_menu()

        # Drawing
        screen.fill(MENU_BG)

        if left_image:
            screen.blit(left_image, left_image_rect)  # Draw the image on the left

        play_button.draw(screen)
        levels_button.draw(screen)  # Draw the ‘Levels’ button

        pygame.display.flip()
        clock.tick(FPS)


# Level selection menu
def level_select_menu():
    menu_running = True
    levels_per_page = 4
    current_page = 0

    title_font = pygame.font.SysFont(None, 48)
    title_text = title_font.render("SELECT LEVEL", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))

    # Uploading images for buttons
    try:
        back_img = pygame.image.load("img/menu_button_back@2x.png")
        next_img = pygame.image.load("img/menu_button_next@2x.png")
        prev_img = pygame.image.load("img/menu_button_prev@2x.png")
        bg_image = pygame.image.load("img/lselect_level@2x.png")
    except pygame.error as e:
        print(f"Error loading level select menu images: {e}")
        back_img = None
        next_img = None
        prev_img = None

    # Creating buttons with images or text
    if back_img:
        back_button = Button(50, SCREEN_HEIGHT - 90, image=back_img)
    else:
        back_button = Button(50, SCREEN_HEIGHT - 70, width=150, height=50, text="BACK")

    if next_img:
        next_page_button = Button(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 70, image=next_img)
    else:
        next_page_button = Button(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 70, width=150, height=50, text="NEXT PAGE")

    if prev_img:
        prev_page_button = Button(SCREEN_WIDTH - 370, SCREEN_HEIGHT - 70, image=prev_img)
    else:
        prev_page_button = Button(SCREEN_WIDTH - 370, SCREEN_HEIGHT - 70, width=150, height=50, text="PREV PAGE")

    while menu_running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True

        # Button handling
        back_button.check_hover(mouse_pos)
        next_page_button.check_hover(mouse_pos)
        prev_page_button.check_hover(mouse_pos)

        if back_button.is_clicked(mouse_pos, mouse_click):
            menu_running = False

        max_pages = (level_manager.get_level_count() - 1) // levels_per_page + 1

        if next_page_button.is_clicked(mouse_pos, mouse_click) and current_page < max_pages - 1:
            current_page += 1

        if prev_page_button.is_clicked(mouse_pos, mouse_click) and current_page > 0:
            current_page -= 1

        # Creating buttons for the levels on the current page
        level_buttons = []
        start_idx = current_page * levels_per_page
        end_idx = min(start_idx + levels_per_page, level_manager.get_level_count())

        for i in range(start_idx, end_idx):
            row = (i - start_idx) // 2
            col = (i - start_idx) % 2
            x = col * 320 + 320
            y = row * 180 + 120
            level_name = level_manager.get_level_name(i)

            # Creating a button with a background image and text
            button = Button(x, y, width=250, height=150, text=level_name, background_image=bg_image)
            level_buttons.append((button, i))

        # Checking clicks on the level buttons
        for button, level_idx in level_buttons:
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_click):
                game = Game(screen, clock, level_manager)
                game.run(level_idx)
                # When you’ve completed the level, return to the level selection menu

        # Drawing
        screen.fill(MENU_BG)
        screen.blit(title_text, title_rect)

        # Drawing Levels button
        for button, _ in level_buttons:
            button.draw(screen)

        back_button.draw(screen)

        if current_page < max_pages - 1:
            next_page_button.draw(screen)

        if current_page > 0:
            prev_page_button.draw(screen)

        # Displaying the current page number
        page_font = pygame.font.SysFont(None, 24)
        page_text = page_font.render(f"Page {current_page + 1}/{max_pages}", True, WHITE)
        screen.blit(page_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50))

        pygame.display.flip()
        clock.tick(FPS)


# Launch the game
if __name__ == "__main__":
    main_menu()