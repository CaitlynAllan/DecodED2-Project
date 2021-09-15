import pygame
from pygame.math import Vector2
from src.entities.enemy import Enemy
from src.entity import Entity
from src.constants import PLAYER_BULLET_COOLDOWN, PLAYER_START_VECTOR, PLAYER_SPEED, PLAYER_HEALTH, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_BULLET_SPEED
from src.entities.bullet import Bullet

class Player(Entity):
    move_direction: int
    speed: int
    health: int

    def __init__(self):
        super().__init__(PLAYER_START_VECTOR.x, PLAYER_START_VECTOR.y, PLAYER_WIDTH, PLAYER_HEIGHT, 'res/player.png')
        self.move_direction = 0
        self.health = PLAYER_HEALTH
        self.speed = PLAYER_SPEED
        self.shooting = False
        self.bullet_cooldown = PLAYER_BULLET_COOLDOWN

    def move_left(self):
        self.move_direction = -1
        
    def move_right(self):
        self.move_direction = 1

    def stop_moving(self):
        self.move_direction = 0

    def shoot(self):
        if self.bullet_cooldown == PLAYER_BULLET_COOLDOWN and not self.expired:
            self.shooting = True

    def tick(self, delta: int, objects: 'list'):
        self.velocity.x = self.speed * self.move_direction

        # Cooldown refresher
        if self.bullet_cooldown >= PLAYER_BULLET_COOLDOWN:
            self.bullet_cooldown = PLAYER_BULLET_COOLDOWN
        else:
            self.bullet_cooldown += delta
        
        # Shoot a bullet
        if self.shooting:
            objects.append(Bullet(Vector2(self.x, self.y), PLAYER_BULLET_SPEED, KILL_PLAYER = False))
        
            self.shooting = False
            self.bullet_cooldown = 0

        for obj in objects:
            if isinstance(obj, Bullet) and obj.kill_player == True and self.colliderect(obj):
                self.health -= 1
                obj.kill()

            if isinstance(obj, Enemy) and self.colliderect(obj):
                self.health = 0

        
        if (self.health <= 0):
            self.kill()
        
