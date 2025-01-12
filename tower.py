import pygame
from bullet import Bullet
import math
from settings import Settings

A = 0
class Tower(pygame.sprite.Sprite):
    def __init__(self, position, game):
        super().__init__()
        self.position = pygame.math.Vector2(position)
        self.game = game

        self.image = None
        self.rect = None
        self.tower_range = 0
        self.damage = 0
        self.rate_of_fire = 0
        self.last_shot_time = pygame.time.get_ticks()
        self.level = 1
        self.original_image = self.image

    def upgrade_cost(self):
        return 100 * self.level

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovered(mouse_pos):
            level_text = self.game.font.render(f"Level: {self.level}", True, (255, 255, 255))
            upgrade_cost_text = self.game.font.render(f"Upgrade: ${self.upgrade_cost()  }", True, (255, 255, 255))

            level_text_pos = (self.position.x, self.position.y + 20)
            upgrade_cost_pos = (self.position.x, self.position.y + 40)

            screen.blit(level_text, level_text_pos)
            screen.blit(upgrade_cost_text, upgrade_cost_pos)

    def update(self, enemies, current_time, bullets_group):
        for tower in self.game.level.towers:
            if type(tower).__name__ == 'MoneyTower':
                self.game.settings.starting_money += 0.05

        if current_time - self.last_shot_time > self.rate_of_fire:
            target = self.find_target(enemies)
            if target:

                self.rotate_towards_target(target)
                self.shoot(target, bullets_group)
                self.last_shot_time = current_time

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def shoot(self, target, bullets_group):
        pass

    def rotate_towards_target(self, target):
        dx = target.position.x - self.position.x
        dy = target.position.y - self.position.y
        # Вычисляем угол в радианах
        angle_rad = math.atan2(dy, dx)
        # Преобразуем радианы в градусы
        angle_deg = math.degrees(angle_rad)
        angle_deg = -angle_deg - 90
        self.image = pygame.transform.rotate(self.original_image, angle_deg)
        self.rect = self.image.get_rect(center=self.position)

    def find_target(self, enemies):
        nearest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = self.position.distance_to(enemy.position)
            if distance < min_distance and distance <= self.tower_range:
                nearest_enemy = enemy
                min_distance = distance
        return nearest_enemy

    def upgrade(self):
        self.level += 1


class BasicTower(Tower):
    def __init__(self, position, game):
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/basic_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.rate_of_fire = 1000
        self.tower_range = 150
        self.damage = 20
        print(1111111111111)
        # print(pygame.mouse.get_pressed()[0])
        if self.game.selected_tower_type == 'basic_level_2':
            print(2222222222222)
            self.tower_range += 50
            self.damage += 41111
            self.level = 211
    def shoot(self, target, bullets_group):
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)


class SniperTower(Tower):
    def __init__(self, position, game):
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/sniper_tower.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 300
        self.damage = 40
        self.rate_of_fire = 2000

    def find_target(self, enemies):
        healthiest_enemy = None
        max_health = 0
        for enemy in enemies:
            if self.position.distance_to(enemy.position) <= self.tower_range and enemy.health > max_health:
                healthiest_enemy = enemy
                max_health = enemy.health
        return healthiest_enemy

    def shoot(self, target, bullets_group):
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)

class MoneyTower(Tower, Settings):

    def __init__(self, position, game):
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/money_factory.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.damage = 20
        self.settings = Settings()



