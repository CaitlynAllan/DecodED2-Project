import random

from pygame import Vector2
from pygame.locals import K_SPACE, KEYDOWN

from src.entity import Entity
# If we have more colors, consider a colors.py
from src.entities.player import Player
from src.entities.bullet import Bullet

from src.entities.enemy import Enemy
from src.constants import MAX_PER_ROW, ROW_GAP, SCREEN_W, TOTAL_GRID_SQUARES, INITIAL_NUM_ENEMIES, BULLET_COOLDOWN

BLACK = (0, 0, 0)


def generate_enemies():
    enemy_list = []
    coords_check = []
    OFFSET = 50

    NUM_ROWS = TOTAL_GRID_SQUARES // MAX_PER_ROW
    COL_GAP = SCREEN_W // MAX_PER_ROW

    for i in range(NUM_ROWS):
        coords_check.append([0 for x in range(MAX_PER_ROW)])

    for num in range(INITIAL_NUM_ENEMIES):
        rand_row = random.randint(0, NUM_ROWS - 1)
        rand_col = random.randint(0, MAX_PER_ROW - 1)

        # This loop is done to ensure that randomly initialised coordinates do not repeat
        while True:
            rand_row = random.randint(0, NUM_ROWS - 1)
            rand_col = random.randint(0, MAX_PER_ROW - 1)
            if coords_check[rand_row][rand_col] == 0:
                coords_check[rand_row][rand_col] = 1
                break

        enemy_coords = Vector2(OFFSET + (rand_col * COL_GAP), OFFSET + (rand_row * ROW_GAP))
        enemy_list.append(Enemy(enemy_coords))

    return enemy_list


class SpaceInvaders:
    """Game implementation of Space Invaders"""
    entitys: list[Entity] = []

    # TODO set up game player object, aliens etc
    def __init__(self):
        self.player = Player()
        self.entitys.append(self.player)
        for enemy in generate_enemies():
            self.entitys.append(enemy)
        
        self.bullet_timer = 0

    def update(self, delta, events):
        # Keep track of bullet cooldown
        if (self.bullet_timer + delta >= BULLET_COOLDOWN):
            self.bullet_timer = self.bullet_timer + delta - BULLET_COOLDOWN
        else:
            self.bullet_timer += delta
       
        for event in events:
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.entitys.append(Bullet(self.player.position))

        # Loop through game objects and remove ones which are expired.      
        # We are iterating backwards here
        for i in range(len(self.entitys) - 1, -1, -1):
            obj = self.entitys[i]
            obj.update(delta, events, self.entitys)
            if obj.expired:
                del self.entitys[i]

    def render(self, display):
        display.fill(BLACK)
        for obj in self.entitys:
            obj.render(display)