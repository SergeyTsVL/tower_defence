import pygame
# import keyboard


class Grid:
    """
    Отвечает за сетку, где игрок может размещать башни.
    """
    def __init__(self, game):
        """
        Инициализирует сетку.
        :param game:
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.available_spots = self.settings.tower_positions
        self.towers = []

    def update(self):
        """
        Может использоваться для обновления сетки.
        :return:
        """
        pass

    def draw(self):
        """
         Отображает сетку на экране.
        :return:
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            for spot in self.available_spots:
                pygame.draw.circle(self.screen, (0, 255, 0), spot, 15, 2)
                pygame.draw.circle(self.screen, (128, 0, 0), spot, 10, 10)
        else:
            None


    def place_tower(self, tower=None):
        """
        Размещает башню на сетке.
        :param tower:
        :return:
        """
        grid_pos = self.get_grid_position(tower.position)
        if grid_pos in self.available_spots and not any(tower.rect.collidepoint(grid_pos) for tower in self.towers):
            self.towers.append(tower)
            return True
        return False

    def remove_tower(self, tower):
        """
        Удаляет башню с сетки.
        :param tower:
        :return:
        """
        if tower in self.towers:
            self.towers.remove(tower)

    def get_grid_position(self, mouse_pos):
        """
        Возвращает позицию сетки, ближайшую к позиции курсора.
        Получаем координаты клетки сетки по положению мыши

        Args:
            mouse_pos (tuple): координаты мыши (x, y).

        Returns:
            tuple: центр нажатой клетки сетки.
        """
        grid_x = mouse_pos[0] // 64 * 64 + 32
        grid_y = mouse_pos[1] // 64 * 64 + 32
        return grid_x, grid_y

    def is_spot_available(self, grid_pos):
        """
        Проверяет, доступно ли место для размещения башни.
        :param grid_pos:
        :return:
        """
        return grid_pos in self.available_spots and all(not tower.rect.collidepoint(grid_pos) for tower in self.towers)
