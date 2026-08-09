import pygame
import os

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 560
FPS = 60
TILE_SIZE = 56
# Добавляем размеры для монет и врагов
# Заменяем COIN_SIZE на отдельные параметры ширины и высоты
COIN_WIDTH = int(TILE_SIZE * 0.5)
COIN_HEIGHT = int(TILE_SIZE * 1.3)
ENEMY_S_WIDTH = int(TILE_SIZE * 0.6)
ENEMY_S_HEIGHT = int(TILE_SIZE * 1)
ENEMY_M_WIDTH = int(TILE_SIZE * 1.3)
ENEMY_M_HEIGHT = int(TILE_SIZE * 1.3)
LIFE_BONUS_SIZE = int(TILE_SIZE * 0.8)
CHECKPOINT_SIZE = int(TILE_SIZE * 0.9)

GRAVITY = 0.45
JUMP_POWER = -13
MOVE_SPEED = 5
# Обновляем пороговые значения для прокрутки по горизонтали и вертикали
SCROLL_THRESHOLD_X = 300
SCROLL_THRESHOLD_Y = 200
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

# Создаем фоновое изображение
# Используем более высокий размер для поддержки вертикальной прокрутки
background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT * 2))
# Создаем градиент от светло-голубого к более темному для глубины
for y in range(SCREEN_HEIGHT * 2):
    # Вычисляем цвет на основе позиции y
    blue_value = max(100, 240 - int(y / (SCREEN_HEIGHT * 2) * 140))
    background_image.fill((174, 206, blue_value), pygame.Rect(0, y, SCREEN_WIDTH, 1))

static_enemy_image = load_image("img/thorn@2x.png", RED)
moving_enemy_image = load_image("img/dyn_thorn@2x.png", BLUE)
heart_image = load_image("img/gbar_life@2x.png", RED)  # Изображение для отображения жизней UI
coin_ui_image = load_image("img/gbar_ring@2x.png", RED)  # Изображение для отображения колец UI
# Добавляем изображение для бонуса жизни
life_bonus_image = load_image("img/life@2x.png", GREEN)  # Используем красный цвет как заглушку


# Масштабируем изображения если нужно
ball_image = pygame.transform.scale(ball_image, (TILE_SIZE, TILE_SIZE))
brick_image = pygame.transform.scale(brick_image, (TILE_SIZE, TILE_SIZE))
coin_image = pygame.transform.scale(coin_image, (COIN_WIDTH, COIN_HEIGHT))
static_enemy_image = pygame.transform.scale(static_enemy_image, (ENEMY_S_WIDTH, ENEMY_S_HEIGHT))
moving_enemy_image = pygame.transform.scale(moving_enemy_image, (ENEMY_M_WIDTH, ENEMY_M_HEIGHT))
if heart_image:
    heart_image = pygame.transform.scale(heart_image, (TILE_SIZE, TILE_SIZE))
# Масштабируем изображение бонуса жизни
if life_bonus_image:
    life_bonus_image = pygame.transform.scale(life_bonus_image, (LIFE_BONUS_SIZE, LIFE_BONUS_SIZE))