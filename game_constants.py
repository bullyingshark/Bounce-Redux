import pygame
import os

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 560
FPS = 60
TILE_SIZE = 56
# Добавляем размеры для монет и врагов
COIN_SIZE = int(TILE_SIZE * 1.2)
ENEMY_S_WIDTH = int(TILE_SIZE * 0.6)
ENEMY_S_HEIGHT = int(TILE_SIZE * 0.9)
ENEMY_M_WIDTH = int(TILE_SIZE * 1.3)
ENEMY_M_HEIGHT = int(TILE_SIZE * 1.3)

GRAVITY = 0.45
JUMP_POWER = -13
MOVE_SPEED = 5
SCROLL_THRESHOLD = 300
ENEMY_MOVE_SPEED = 2
ENEMY_MOVE_DISTANCE = 100

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MENU_BG = (68, 204, 255)
BUTTON_COLOR = (150, 150, 250)
BUTTON_HOVER = (200, 200, 255)


# Функция для загрузки изображений
def load_image(name, fallback_color=None):
    try:
        if os.path.exists(name):
            image = pygame.image.load(name)
            return image
        else:
            print(f"Файл изображения не найден: {name}")
    except pygame.error as e:
        print(f"Не удалось загрузить изображение: {name}")
        print(f"Ошибка: {e}")

    # Создаем заглушку
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    if fallback_color:
        surface.fill(fallback_color)
    else:
        # Шахматная текстура как заглушка
        check_size = TILE_SIZE // 2
        for y in range(2):
            for x in range(2):
                color = WHITE if (x + y) % 2 == 0 else BLACK
                pygame.draw.rect(surface, color, (x * check_size, y * check_size, check_size, check_size))

    return surface


# Загрузка текстур
ball_image = load_image("img/ball_small@2x.png", RED)
brick_image = load_image("img/ui_ground_block@2x.png", (200, 100, 50))
coin_image = load_image("img/ring_small@2x.png", YELLOW)

# Создаем фоновое изображение просто как поверхность с цветом
background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background_image.fill((174, 206, 240))

static_enemy_image = load_image("img/thorn@2x.png", RED)
moving_enemy_image = load_image("img/dyn_thorn@2x.png", GREEN)
heart_image = load_image("img/gbar_life@2x.png", RED)  # Изображение для отображения жизней UI
coin_ui_image = load_image("img/gbar_ring@2x.png", RED)  # Изображение для отображения колец UI

# Масштабируем изображения если нужно
ball_image = pygame.transform.scale(ball_image, (TILE_SIZE, TILE_SIZE))
brick_image = pygame.transform.scale(brick_image, (TILE_SIZE, TILE_SIZE))
coin_image = pygame.transform.scale(coin_image, (COIN_SIZE, COIN_SIZE))
static_enemy_image = pygame.transform.scale(static_enemy_image, (ENEMY_S_WIDTH, ENEMY_S_HEIGHT))
moving_enemy_image = pygame.transform.scale(moving_enemy_image, (ENEMY_M_WIDTH, ENEMY_M_HEIGHT))
if heart_image:
    heart_image = pygame.transform.scale(heart_image, (TILE_SIZE, TILE_SIZE))