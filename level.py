import pygame
from enemy import Enemy
from tower import BasicTower, SniperTower, MoneyTower
import random


enemies_random = random.randint(1, 2)
class Level:
    def __init__(self, game):
        self.game = game
        self.enemies1 = pygame.sprite.Group()
        self.enemies2 = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.waves = [
            [{'path': self.game.settings.enemy_path, 'speed': 1, 'health': 100, 'image_path': 'assets/enemies/basic_enemy.png'}] * 5,
            [{'path': self.game.settings.enemy_path, 'speed': 1.5, 'health': 150, 'image_path': 'assets/enemies/fast_enemy.png'}] * 7,
            [{'path': self.game.settings.enemy_path, 'speed': 0.75, 'health': 200, 'image_path': 'assets/enemies/strong_enemy.png'}] * 4,
        ]
        self.waves2 = [
            [{'path': self.game.settings.enemy_path2, 'speed': 1, 'health': 100, 'image_path': 'assets/enemies/basic_enemy.png'}] * 5,
            [{'path': self.game.settings.enemy_path2, 'speed': 1.5, 'health': 150, 'image_path': 'assets/enemies/fast_enemy.png'}] * 7,
            [{'path': self.game.settings.enemy_path2, 'speed': 0.75, 'health': 200, 'image_path': 'assets/enemies/strong_enemy.png'}] * 4,
        ]
        self.current_wave = 0
        self.current_wave2 = 0
        self.spawned_enemies = 0
        self.spawned_enemies2 = 0
        self.spawn_delay = 1000
        self.last_spawn_time = pygame.time.get_ticks()
        self.all_waves_complete = False
        self.start_next_wave()
        self.font = pygame.font.SysFont("Arial", 24)

    def start_next_wave(self):
        if self.current_wave < len(self.waves2):
            self.spawned_enemies = 0
            self.spawn_next_enemy()
        if self.current_wave2 < len(self.waves2):
            self.spawned_enemies2 = 0
            self.spawn_next_enemy2()

    def spawn_next_enemy(self):
        if self.spawned_enemies < len(self.waves[self.current_wave]):
            enemy_info = self.waves[self.current_wave][self.spawned_enemies]
            new_enemy = Enemy(**enemy_info, game=self.game)
            self.enemies1.add(new_enemy)
            self.spawned_enemies += 1


    def spawn_next_enemy2(self):
        if self.spawned_enemies2 < len(self.waves2[self.current_wave2]):
            enemy_info = self.waves2[self.current_wave2][self.spawned_enemies2]
            new_enemy = Enemy(**enemy_info, game=self.game)
            self.enemies2.add(new_enemy)
            self.spawned_enemies2 += 1

    def attempt_place_tower(self, mouse_pos, tower_type):
        tower_classes = {'basic': BasicTower, 'sniper': SniperTower, 'money': MoneyTower, 'basic_level_2': BasicTower}
        if tower_type in tower_classes and self.game.settings.starting_money >= self.game.settings.tower_cost:
            grid_pos = self.game.grid.get_grid_position(mouse_pos)
            if self.game.grid.is_spot_available(grid_pos):
                self.game.settings.starting_money -= self.game.settings.tower_cost
                new_tower = tower_classes[tower_type](grid_pos, self.game)
                self.towers.add(new_tower)
                print("Tower placed.")
            else:
                print("Invalid position for tower.")
        else:
            print("Not enough money or unknown tower type.")

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.current_wave < len(self.waves) and self.spawned_enemies < len(self.waves[self.current_wave]):
            if current_time - self.last_spawn_time > self.spawn_delay:
                enemy_info = self.waves[self.current_wave][self.spawned_enemies].copy()
                enemy_info['game'] = self.game
                new_enemy = Enemy(**enemy_info)
                self.enemies1.add(new_enemy)
                self.spawned_enemies += 1
                self.last_spawn_time = current_time

        if self.current_wave2 < len(self.waves2) and self.spawned_enemies2 < len(self.waves2[self.current_wave2]):
            if current_time - self.last_spawn_time > self.spawn_delay:
                enemy_info = self.waves2[self.current_wave2][self.spawned_enemies2].copy()
                enemy_info['game'] = self.game
                new_enemy = Enemy(**enemy_info)
                self.enemies2.add(new_enemy)
                self.spawned_enemies2 += 1
                self.last_spawn_time = current_time

        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies1, True, False)
        for bullet in collisions:
            for enemy in collisions[bullet]:
                enemy.take_damage(bullet.damage)

        collisions2 = pygame.sprite.groupcollide(self.bullets, self.enemies2, True, False)
        for bullet in collisions2:
            for enemy in collisions2[bullet]:
                enemy.take_damage(bullet.damage)

        self.enemies1.update()
        self.enemies2.update()
        for tower in self.towers:
            tower.update(self.enemies1, current_time, self.bullets)
        for tower in self.towers:
            tower.update(self.enemies2, current_time, self.bullets)
        self.bullets.update()

        if len(self.enemies1) == 0 and self.current_wave < len(self.waves) - 1:
            self.current_wave += 1
            self.start_next_wave()
        elif len(self.enemies1) == 0 and self.current_wave == len(self.waves) - 1:
            self.all_waves_complete = True

        if len(self.enemies2) == 0 and self.current_wave2 < len(self.waves2) - 1:
            self.current_wave2 += 1
            self.start_next_wave()
        elif len(self.enemies2) == 0 and self.current_wave2 == len(self.waves2) - 1:
            self.all_waves_complete = True
    def draw_path(self, screen):
        pygame.draw.lines(screen, (0, 128, 0), False, self.game.settings.enemy_path, 5)

    def draw_path2(self, screen):
        pygame.draw.lines(screen, (0, 128, 0), False, self.game.settings.enemy_path2, 5)
        for pos in self.game.settings.tower_positions:
            pygame.draw.circle(screen, (128, 0, 0), pos, 0)

    def draw(self, screen):
        self.draw_path(screen)
        self.draw_path2(screen)
        if enemies_random == 1:
            self.enemies1.draw(screen)
        else:
            self.enemies2.draw(screen)
        self.towers.draw(screen)
        self.bullets.draw(screen)
        mouse_pos = pygame.mouse.get_pos()
        for tower in self.towers:
            tower.draw(screen)
            if tower.is_hovered(mouse_pos):
                tower_stats_text = self.font.render(f"Damage: {tower.damage}, Range: {tower.tower_range}", True,
                                                    (255, 255, 255))
                screen.blit(tower_stats_text, (tower.rect.x, tower.rect.y - 20))
