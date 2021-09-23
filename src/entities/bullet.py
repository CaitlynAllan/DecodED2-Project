from src.constants import SCREEN_H
from src.entity import Entity

<<<<<<< HEAD
# Represents the bullet entity, spawned both by the player and enemy class

class Bullet(Entity):
    def __init__(self, player_position, bullet_speed, KILL_PLAYER=True):
        super().__init__(player_position.x + 12, player_position.y, 30, 30, 'res/bullet.png')

        self.velocity.y = -1 * bullet_speed
        self.kill_player = KILL_PLAYER
        if self.kill_player:
            self.velocity.y *= -1 
    
    def tick(self, delta, objects):
        # Despawn the bullet when it crosses boundaries
=======
# Represents the bullet entity, spawned by player and enemy class

class Bullet(Entity):
    def __init__(self, player_position, bullet_spped, KILL_PLAYER=True):
        super().__init__(player_position.x + 12, player_position.y, 30, 30, 'res/bullet.png')

        self.velocity.y = -1 * bullet_spped
        self.kill_player = KILL_PLAYER
        if self.kill_player:
            self.velocity.y *= -1

    def tick(self, delta, objects):

>>>>>>> 4d9195a0859f3057dff8e8cba0d6a489eab3e5e4
        if self.y < 0 or self.y > SCREEN_H:
            self.kill()

