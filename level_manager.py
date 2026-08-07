import pygame
import os


class LevelManager:
    def __init__(self):
        self.levels = []
        self.current_level = None
        self.load_levels()

    def load_levels(self):
        # Сначала ищем файлы уровней в папке levels
        level_dir = "levels"
        try:
            if os.path.exists(level_dir):
                for file in os.listdir(level_dir):
                    if file.endswith(".txt"):
                        level_path = os.path.join(level_dir, file)
                        level_name = file.split(".")[0]
                        # Проверяем, есть ли картинка для превью уровня
                        preview_path = os.path.join(level_dir, f"{level_name}_preview.png")
                        preview = None
                        if os.path.exists(preview_path):
                            try:
                                preview = pygame.image.load(preview_path)
                                preview = pygame.transform.scale(preview, (200, 150))
                            except:
                                print(f"Не удалось загрузить превью для уровня {level_name}")

                        self.levels.append({
                            "name": level_name,
                            "path": level_path,
                            "preview": preview
                        })
        except Exception as e:
            print(f"Ошибка при загрузке уровней: {e}")

        # Если нет файлов уровней, создаем тестовые уровни
        if not self.levels:
            self.create_default_levels()

    def create_default_levels(self):
        default_levels = [
            {
                "name": "Level 1",
                "map": [
                    "111111111111111111111111111111111111",
                    "1                                  1",
                    "1                                  1",
                    "1                                  1",
                    "1        C          C              1",
                    "1       111        111             1",
                    "1                                  1",
                    "1   S        C           C         1",
                    "1  111    E 111         111        1",
                    "111111111111111111111111111111111111"
                ]
            },
            {
                "name": "Level 2",
                "map": [
                    "111111111111111111111111111111111111",
                    "1                                  1",
                    "1                        C         1",
                    "1                       111        1",
                    "1           C                      1",
                    "1          111       M             1",
                    "1                              11111",
                    "1   S                   C          1",
                    "1  1111111111111111111111111111    1",
                    "111111111111111111111111111111111111"
                ]
            },
            {
                "name": "Level 3",
                "map": [
                    "111111111111111111111111111111111111",
                    "1                                  1",
                    "1                                  1",
                    "1  C     C     C     C     C       1",
                    "1 111   111   111   111   111      1",
                    "1     E       M       E            1",
                    "1                                  1",
                    "1   S            111           11111",
                    "1  111                             1",
                    "111111111111111111111111111111111111"
                ]
            }
        ]

        for level in default_levels:
            self.levels.append({
                "name": level["name"],
                "map": level["map"],
                "preview": None
            })

    def load_level(self, index):
        if 0 <= index < len(self.levels):
            level = self.levels[index]
            self.current_level = index

            # Загружаем карту уровня
            if "path" in level:
                try:
                    with open(level["path"], "r") as f:
                        level_map = [line.strip() for line in f.readlines()]
                except:
                    print(f"Ошибка при чтении файла уровня {level['name']}")
                    level_map = None
            else:
                level_map = level.get("map", None)

            return level_map
        return None

    def get_level_count(self):
        return len(self.levels)

    def get_level_name(self, index):
        if 0 <= index < len(self.levels):
            return self.levels[index]["name"]
        return "Unknown Level"

    def get_level_preview(self, index):
        if 0 <= index < len(self.levels):
            return self.levels[index].get("preview", None)
        return None