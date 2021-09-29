from trainer_constants import MIN_MAX_OUTPUT, Action
from src.constants import SCREEN_H, SCREEN_W, PLAYER_HEALTH
from src.entities.bullet import Bullet
from src.entities.enemy import Enemy
from src.game import Game


def calculate_fitness(game: Game) -> int:
    fitness = game.score
    return fitness

def map_input(val: float, max_in: float):
    return val/max_in


def get_closest_entity(entities, game):
    closest_distance = SCREEN_H * SCREEN_W
    closest_entity = [0, 0]
    for entity in entities:
        distance = (game.player.x - entity.x)**2 + (game.player.y - entity.y)**2
        if distance < closest_distance:
            closest_distance = distance
            closest_entity = [map_input(entity.x, SCREEN_W), map_input(entity.y, SCREEN_H)]

    return closest_entity


def calculate_inputs(game: Game):

    player_x = map_input(game.player.x, SCREEN_W)
    
    player_health = map_input(game.player.health, PLAYER_HEALTH)
    
    enemy_bullets = [entity for entity in game.entities if isinstance(entity, Bullet) and entity.kill_player]
    closest_bullet = get_closest_entity(enemy_bullets, game)
    
    player_bullet = [0, 0]
    player_bullets_arr = [entity for entity in game.entities if isinstance(entity, Bullet) and not entity.kill_player]
    if player_bullets_arr:
        player_bullet_obj = player_bullets_arr[-1]
        player_bullet = [map_input(player_bullet_obj.x, SCREEN_W), map_input(player_bullet_obj.y, SCREEN_H)]
    
    enemies = [entity for entity in game.entities if isinstance(entity, Enemy)]
    closest_enemy = get_closest_entity(enemies, game)

    input_arr = [player_x, player_health] + closest_bullet + player_bullet + closest_enemy

    return input_arr


def input_game(action: Action, game: Game):
    if action == Action.MOVE_RIGHT:
        game.player.move_right()
    elif action == Action.MOVE_LEFT:
        game.player.move_left()
    elif action == Action.MOVE_RIGHT_AND_SHOOT:
        game.player.move_right()
        game.player.shoot()
    elif action == Action.MOVE_LEFT_AND_SHOOT:
        game.player.move_left()
        game.player.shoot()
    elif action == Action.SHOOT:
        game.player.shoot()

