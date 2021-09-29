import neat
import pickle
from neat import ParallelEvaluator
import numpy as np
from numpy.lib.ufunclike import isneginf
from pygame.display import update
from trainer_constants import DELTA, GENERATIONS, TRAIN_MODE, TRAINING_THREADS, Action
import pygame
from src.constants import SCREEN_H, SCREEN_W
from src.game import Game
from trainer_util import calculate_inputs, calculate_fitness, input_game

# missing argument here
config: neat.Config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation)

def eval_genome(genome: neat.DefaultGenome, run_fast: bool = False):
    game = Game()
    updates_done = 0
    pygame.init()
    is_ended = False
    display = pygame.display.set_mode((SCREEN_W, SCREEN_H), 0 ,32)
    font = pygame.font.SysFont("Arial", 24)
    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                is_ended = True
                genome.fitness = 0
            if is_ended:
                break
            net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
            game.update(DELTA)
            updates_done += 1
            if (updates_done%128 or not run_fast):
                game.render(display, font)
                pygame.display.update()

            ai_decision = net.activate(calculate_inputs(game))
            action = Action(np.argmax(ai_decision))
            input_game(action, game)

            if game.player.expired:
                genome.fitness = calculate_fitness(game)
                is_ended = True
            
    return genome.fitness

def init_trainer():
    threaded = ParallelEvaluator(TRAINING_THREADS, eval_genome)

    p: neat.Population = neat.Population(config)
    p.add_reporter(neat.Checkpointer(5))

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    best_bot = p.run(threaded.evaluate, GENERATIONS)

    with open('best-bot.pkl', 'wb') as handle:
        pickle.dump(best_bot, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    if TRAIN_MODE:
        init_trainer()

    else:
        with open('best-bot.pkl', 'rb') as f:
            best_bot = pickle.load(f)
            eval_genome(best_bot, run_fast=False)