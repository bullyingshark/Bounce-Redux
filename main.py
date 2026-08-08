import pygame
import sys
from game_constants import *
from level_manager import LevelManager
from button import Button
from game import Game

# Инициализация Pygame
pygame.init()

# Окно
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bounce")
clock = pygame.time.Clock()

# Создаем менеджер уровней
level_manager = LevelManager()


# Главное меню
def main_menu():
    menu_running = True

    # Загрузка изображений
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

    # Создание кнопок
    if play_img:
        play_button = Button(SCREEN_WIDTH // 2 + 150, 100, image=play_img)
    else:
        play_button = Button(SCREEN_WIDTH // 2 + 50, 100, width=200, height=50, text="PLAY")

    # Добавляем кнопку Levels
    if levels_img:
        levels_button = Button(SCREEN_WIDTH // 2 + 150, 200, image=levels_img)
    else:
        levels_button = Button(SCREEN_WIDTH // 2 + 50, 200, width=200, height=50, text="LEVELS")

    # Получаем Rect для левого изображения и позиционируем его
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

        # Проверка наведения курсора
        play_button.check_hover(mouse_pos)
        levels_button.check_hover(mouse_pos)

        # Проверка клика на кнопку Play
        if play_button.is_clicked(mouse_pos, mouse_click):
            # Запускаем первый уровень
            if level_manager.get_level_count() > 0:
                game = Game(screen, clock, level_manager)
                game.run(0)

        # Проверка клика на кнопку Levels
        if levels_button.is_clicked(mouse_pos, mouse_click):
            # Переходим в меню выбора уровня
            level_select_menu()

        # Отрисовка
        screen.fill(MENU_BG)

        if left_image:
            screen.blit(left_image, left_image_rect)  # Отображение левого изображения

        play_button.draw(screen)
        levels_button.draw(screen)  # Отрисовываем кнопку Levels

        pygame.display.flip()
        clock.tick(FPS)


# Меню выбора уровней
def level_select_menu():
    menu_running = True
    levels_per_page = 4
    current_page = 0

    title_font = pygame.font.SysFont(None, 48)
    title_text = title_font.render("SELECT LEVEL", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))

    # Загрузка изображений для кнопок
    try:
        back_img = pygame.image.load("img/menu_button_back@2x.png")
        next_img = pygame.image.load("img/menu_button_next@2x.png")
        prev_img = pygame.image.load("img/menu_button_prev@2x.png")
    except pygame.error as e:
        print(f"Error loading level select menu images: {e}")
        back_img = None
        next_img = None
        prev_img = None

    # Создаем кнопки с изображениями или текстом
    if back_img:
        back_button = Button(50, SCREEN_HEIGHT - 70, image=back_img)
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

        # Обработка кнопок
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

        # Создаем кнопки для уровней на текущей странице
        level_buttons = []
        start_idx = current_page * levels_per_page
        end_idx = min(start_idx + levels_per_page, level_manager.get_level_count())

        for i in range(start_idx, end_idx):
            row = (i - start_idx) // 2
            col = (i - start_idx) % 2
            x = col * 320 + 100
            y = row * 180 + 120
            preview = level_manager.get_level_preview(i)
            level_name = level_manager.get_level_name(i)
            level_buttons.append((Button(x, y, width=250, height=150, text=level_name), i))

        # Проверяем клики на кнопках уровней
        for button, level_idx in level_buttons:
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_click):
                game = Game(screen, clock, level_manager)
                game.run(level_idx)
                # После завершения уровня возвращаемся в меню выбора уровней

        # Отрисовка
        screen.fill(MENU_BG)
        screen.blit(title_text, title_rect)

        # Отрисовка кнопок уровней
        for button, _ in level_buttons:
            button.draw(screen)

        back_button.draw(screen)

        if current_page < max_pages - 1:
            next_page_button.draw(screen)

        if current_page > 0:
            prev_page_button.draw(screen)

        # Отображаем номер текущей страницы
        page_font = pygame.font.SysFont(None, 24)
        page_text = page_font.render(f"Page {current_page + 1}/{max_pages}", True, WHITE)
        screen.blit(page_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50))

        pygame.display.flip()
        clock.tick(FPS)


# Запуск игры
if __name__ == "__main__":
    main_menu()