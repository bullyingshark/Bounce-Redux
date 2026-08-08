import pygame
import sys
from game_constants import *
from player import Player
from button import Button
from enemy import Enemy, MovingEnemy
from game_constants import TILE_SIZE, COIN_SIZE


class Game:
    def __init__(self, screen, clock, level_manager):
        self.screen = screen
        self.clock = clock
        self.level_manager = level_manager
        self.font = pygame.font.SysFont(None, 36)
        self.pause_font = pygame.font.SysFont(None, 72)

        # Load pause menu button images
        try:
            self.resume_img = pygame.image.load("img/dialog_pause_button_resume@2x.png")
            self.restart_img = pygame.image.load("img/dialog_pause_button_restart@2x.png")
            self.menu_img = pygame.image.load("img/dialog_pause_button_menu@2x.png")
            self.pause_btn_img = pygame.image.load("img/gbar_pause@2x.png")
        except pygame.error:
            print("Could not load pause menu button images, using text buttons instead")
            self.resume_img = None
            self.restart_img = None
            self.menu_img = None
            self.pause_btn_img = None

        # Create pause button
        if self.pause_btn_img:
            self.pause_button = Button(SCREEN_WIDTH - 100, 0, image=self.pause_btn_img)
        else:
            self.pause_button = Button(SCREEN_WIDTH - 110, 20, width=100, height=40, text="PAUSE")

        # Load level complete menu button images
        try:
            self.next_lvl_img = pygame.image.load("img/game_dialog_complete_button_next@2x.png")
            self.restart_img = pygame.image.load("img/dialog_pause_button_restart@2x.png")
            self.menu_img = pygame.image.load("img/dialog_pause_button_menu@2x.png")
        except pygame.error:
            print("Could not load level complete button images, using text buttons instead")
            self.resume_img = None
            self.restart_img = None
            self.menu_img = None

        self.level_complete = False  # Добавляем флаг завершения уровня

        # Load level failed menu button images
        try:
            self.retry_img = pygame.image.load("img/game_dialog_failed_button_retry@2x.png")
            self.menu_img = pygame.image.load("img/dialog_pause_button_menu@2x.png")
        except pygame.error:
            print("Could not load pause menu button images, using text buttons instead")
            self.retry_img = None
            self.menu_img = None

    def run(self, level_index):
        # Загружаем выбранный уровень
        level_map = self.level_manager.load_level(level_index)
        if not level_map:
            print(f"Не удалось загрузить уровень с индексом {level_index}")
            return

        # Создаем игровые объекты на основе карты уровня
        platforms = []
        coins = []
        static_enemies = []
        moving_enemies = []
        ball_pos = [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2]  # Позиция по умолчанию

        for y, row in enumerate(level_map):
            for x, tile in enumerate(row):
                if tile == '1':
                    platforms.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif tile == 'C':
                    # Центрируем монету внутри тайла
                    coin_x = x * TILE_SIZE + (TILE_SIZE - COIN_SIZE) // 2
                    coin_y = y * TILE_SIZE + (TILE_SIZE - COIN_SIZE) // 2
                    coins.append(pygame.Rect(coin_x, coin_y, COIN_SIZE, COIN_SIZE))
                elif tile == 'S':
                    ball_pos = [x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2]
                elif tile == 'E':  # Статичный враг
                    enemy_pos = [x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2]
                    static_enemies.append(Enemy(enemy_pos[0], enemy_pos[1], static_enemy_image))
                elif tile == 'M':  # Движущийся враг
                    enemy_pos = [x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2]
                    moving_enemies.append(MovingEnemy(
                        enemy_pos[0],
                        enemy_pos[1],
                        ENEMY_MOVE_DISTANCE,
                        ENEMY_MOVE_SPEED,
                        moving_enemy_image
                    ))

        # Создаем игрока
        player = Player(ball_pos[0], ball_pos[1], ball_image)

        # Переменные игровой логики
        camera_x = 0
        score = 0
        collected_coins = []
        level_completed = False
        game_over = False

        # Создаем кнопки паузы с изображениями, если они загружены, иначе используем текстовые
        if self.resume_img and self.restart_img and self.menu_img:
            pause_buttons = [
                Button(SCREEN_WIDTH // 2 - 180, 150, image=self.resume_img),
                Button(SCREEN_WIDTH // 2 - 180, 250, image=self.restart_img),
                Button(SCREEN_WIDTH // 2 - 180, 350, image=self.menu_img)
            ]
        else:
            pause_buttons = [
                Button(SCREEN_WIDTH // 2 - 100, 200, width=200, height=50, text="CONTINUE"),
                Button(SCREEN_WIDTH // 2 - 100, 280, width=200, height=50, text="RESTART"),
                Button(SCREEN_WIDTH // 2 - 100, 360, width=200, height=50, text="MENU")
            ]

        # Кнопки игры окончена
        game_over_buttons = [
            Button(SCREEN_WIDTH // 2 - 100, 280, width=200, height=50, text="RESTART"),
            Button(SCREEN_WIDTH // 2 - 100, 360, width=200, height=50, text="MENU")
        ]

        # Игровой цикл
        game_running = True
        game_paused = False

        while game_running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused = not game_paused
                    if not game_paused and not game_over:
                        if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                            player.jump()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_click = True

            # Проверка нажатия на кнопку паузы
            self.pause_button.check_hover(mouse_pos)
            if self.pause_button.is_clicked(mouse_pos, mouse_click):
                game_paused = True

            # Обработка паузы
            if game_paused:
                result = self._handle_pause(pause_buttons, mouse_pos, mouse_click, level_index)
                if result == "continue":
                    game_paused = False  # Снимаем игру с паузы
                    continue
                elif result == "quit":
                    return  # Возвращаемся в меню
                else:
                    continue  # Остаемся в паузе

            # Обработка конца игры
            if game_over:
                if self._handle_game_over(game_over_buttons, mouse_pos, mouse_click, level_index):
                    return
                continue

            # Проверка на завершение уровня (все монеты собраны)
            if len(collected_coins) == len(coins) and not level_completed:
                level_completed = True

            if level_completed:
                if self._handle_level_complete(score, mouse_pos, mouse_click, level_index):
                    return
                continue

            # Игровая логика
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.move(-1)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.move(1)
            # Обработка непрерывного прыжка
            if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
                player.jump()

            # Обновляем игрока
            player.update(platforms)

            # Обновляем движущихся врагов
            for enemy in moving_enemies:
                enemy.update()

            # Проверка столкновений с врагами
            for enemy in static_enemies + moving_enemies:
                if player.collides_with(enemy.get_rect()):
                    if player.take_damage():
                        # Возвращаем игрока на начальную позицию
                        player.reset_position()
                        # Проверка, если игрок умер
                        if player.is_dead():
                            game_over = True

            # Сбор монет
            for coin in coins[:]:
                if coin not in collected_coins and player.collides_with(coin):
                    collected_coins.append(coin)
                    score += 10

            # Обновление положения камеры
            camera_x = self._update_camera(player, camera_x, platforms)

            # Отрисовка
            self._draw_game(
                player,
                platforms,
                coins,
                collected_coins,
                static_enemies,
                moving_enemies,
                camera_x,
                score,
                level_index
            )

            # Отрисовка кнопки паузы (поверх игрового интерфейса)
            self.pause_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

    def _handle_pause(self, pause_buttons, mouse_pos, mouse_click, level_index):
        # Обработка кнопок паузы
        for i, button in enumerate(pause_buttons):
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_click):
                if i == 0:  # Continue
                    return "continue"  # Возвращаем строку, чтобы снять игру с паузы
                elif i == 1:  # Restart
                    self.run(level_index)
                    return "quit"  # Возвращаем строку, чтобы выйти из текущего цикла
                elif i == 2:  # Menu
                    return "quit"  # Возвращаем строку, чтобы выйти в меню

        # Заливаем экран цветом MENU_BG
        self.screen.fill(MENU_BG)

        # Создаем панель меню паузы
        # menu_panel = pygame.Surface((400, 400), pygame.SRCALPHA)
        # menu_panel.fill((200, 200, 255, 220))
        # pygame.draw.rect(menu_panel, (100, 100, 200), menu_panel.get_rect(), 4)
        # self.screen.blit(menu_panel, (SCREEN_WIDTH // 2 - 200, 50))

        # Заголовок
        pause_text = self.pause_font.render("PAUSE", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(pause_text, pause_rect)

        # Отрисовка кнопок
        for button in pause_buttons:
            button.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(FPS)
        return None  # Возвращаем None, чтобы остаться в режиме паузы

    def _handle_game_over(self, game_over_buttons, mouse_pos, mouse_click, level_index):
        # Обработка кнопок конца игры
        for i, button in enumerate(game_over_buttons):
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_click):
                if i == 0:  # Restart
                    self.run(level_index)
                    return True
                elif i == 1:  # Menu
                    return True

        # Отрисовка экрана конца игры
        self.screen.fill((MENU_BG), special_flags=pygame.BLEND_RGBA_MULT)
        game_over_text = self.pause_font.render("LEVEL FAILED!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(game_over_text, game_over_rect)

        # Создаем кнопки с изображениями, если они загружены, иначе используем текстовые
        if self.retry_img and self.menu_img:
            retry_button = Button(SCREEN_WIDTH // 2 - 180, 200, image=self.retry_img)
            menu_button = Button(SCREEN_WIDTH // 2 - 180, 300, image=self.menu_img)
        else:
            retry_button = Button(SCREEN_WIDTH // 2 - 100, 320, width=200, height=50, text="RETRY")
            menu_button = Button(SCREEN_WIDTH // 2 - 100, 390, width=200, height=50, text="MENU")

        retry_button.check_hover(mouse_pos)
        menu_button.check_hover(mouse_pos)

        if retry_button.is_clicked(mouse_pos, mouse_click):
            self.run(level_index)  # Перезапуск текущего уровня
            return True

        if menu_button.is_clicked(mouse_pos, mouse_click):
            return True  # Возврат в меню

        retry_button.draw(self.screen)
        menu_button.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(FPS)
        return False

    def _handle_level_complete(self, score, mouse_pos, mouse_click, level_index):
        # Показываем экран завершения уровня
        self.screen.fill(MENU_BG)
        complete_text = self.pause_font.render("LEVEL COMPLETED!", True, WHITE)
        complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(complete_text, complete_rect)

        score_text = self.font.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 180))
        self.screen.blit(score_text, score_rect)

        # Создаем кнопки с изображениями, если они загружены, иначе используем текстовые
        if self.next_lvl_img and self.restart_img and self.menu_img:
            next_button = Button(SCREEN_WIDTH // 2 - 180, 220, image=self.next_lvl_img)
            restart_button = Button(SCREEN_WIDTH // 2 - 180, 320, image=self.restart_img)
            menu_button = Button(SCREEN_WIDTH // 2 - 180, 420, image=self.menu_img)
        else:
            next_button = Button(SCREEN_WIDTH // 2 - 100, 250, width=200, height=50, text="NEXT LEVEL")
            restart_button = Button(SCREEN_WIDTH // 2 - 100, 320, width=200, height=50, text="RESTART")
            menu_button = Button(SCREEN_WIDTH // 2 - 100, 390, width=200, height=50, text="MENU")

        next_button.check_hover(mouse_pos)
        restart_button.check_hover(mouse_pos)
        menu_button.check_hover(mouse_pos)

        if next_button.is_clicked(mouse_pos, mouse_click):
            if level_index + 1 < self.level_manager.get_level_count():
                self.run(level_index + 1)
                return True
            else:
                return True  # Вернуться в меню, если это был последний уровень

        if restart_button.is_clicked(mouse_pos, mouse_click):
            self.run(level_index)  # Перезапуск текущего уровня
            return True

        if menu_button.is_clicked(mouse_pos, mouse_click):
            return True  # Возврат в меню

        next_button.draw(self.screen)
        restart_button.draw(self.screen)
        menu_button.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(FPS)
        return False

    def _update_camera(self, player, camera_x, platforms):
        # Обновление положения камеры
        if player.pos[0] > camera_x + SCREEN_WIDTH - SCROLL_THRESHOLD:
            camera_x = player.pos[0] - (SCREEN_WIDTH - SCROLL_THRESHOLD)
        elif player.pos[0] < camera_x + SCROLL_THRESHOLD:
            camera_x = player.pos[0] - SCROLL_THRESHOLD

        # Ограничение камеры
        max_x = max([platform.right for platform in platforms] + [0])
        max_camera_x = max(0, max_x - SCREEN_WIDTH)
        camera_x = max(0, min(camera_x, max_camera_x))

        return camera_x

    def _draw_game(self, player, platforms, coins, collected_coins, static_enemies, moving_enemies, camera_x, score,
                   level_index):
        self.screen.blit(background_image, (0, 0))

        # Отрисовка платформ
        for platform in platforms:
            if platform.right > camera_x and platform.left < camera_x + SCREEN_WIDTH:
                self.screen.blit(brick_image, (platform.x - camera_x, platform.y))

        # Отрисовка монет
        for coin in coins:
            if coin not in collected_coins and coin.right > camera_x and coin.left < camera_x + SCREEN_WIDTH:
                self.screen.blit(coin_image, (coin.x - camera_x, coin.y))

        # Отрисовка врагов
        for enemy in static_enemies:
            enemy.draw(self.screen, camera_x)

        for enemy in moving_enemies:
            enemy.draw(self.screen, camera_x)

        # Отрисовка персонажа
        player.draw(self.screen, camera_x)

        # Отображение информации
        # Отображаем счет справа от кнопки паузы с пятью нулями вначале
        score_text = self.font.render(f"{score:05d}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topright = (SCREEN_WIDTH - 120, 20)
        self.screen.blit(score_text, score_rect)

        # Отображение названия уровня
        level_text = self.font.render(f"Level: {self.level_manager.get_level_name(level_index)}", True, WHITE)
        self.screen.blit(level_text, (560, 20))

        # Отображение жизней с использованием иконки шарика и текста 'x3'
        lives_text = self.font.render(f"X{player.lives}", True, WHITE)
        # Масштабируем изображение шарика для отображения жизней
        life_ball = pygame.transform.scale(heart_image, (30, 30))
        self.screen.blit(life_ball, (40, 15))
        self.screen.blit(lives_text, (75, 20))

        # Отображение доступных монет на уровне
        #coin_text = self.font.render(":", True, WHITE)
        #self.screen.blit(coin_text, (120, 20))

        # Отображаем маленькие иконки монет, по одной за каждую монету на уровне
        small_coin = pygame.transform.scale(coin_ui_image, (20, 30))
        for i in range(len(coins)):
            coin_status = i < len(collected_coins)  # True если монета собрана
            # Если монета собрана, затемняем её
            coin_alpha = 100 if coin_status else 255
            coin_copy = small_coin.copy()
            coin_copy.set_alpha(coin_alpha)
            self.screen.blit(coin_copy, (200 + i * 25, 15))