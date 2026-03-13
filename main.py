# libraries
import pygame, copy, time
from pygame.locals import * # allows use of terms like JOYAXISMOTION w/o leading `pygame.`.
import numpy as np

# locals
from constants import *
from assets import *
from display import screen
from groups import *
from input import * # initializes joysticks and random number generator
from entities import *
from physics import *
from components import *
from levels import *
from utils import *
from states import *

# instance players
# player_1 = Player(players, 'player_1', noeys_ship_img, None, copy.copy(player_engine), copy.copy(player_armor), create_weapon_list())
# player_1.glam_image = noeys_ship_glam_img
player_2 = Player(players, 'player_2', gabes_ship_img, None, copy.copy(player_engine), copy.copy(player_armor), create_weapon_list())
player_2.glam_image = gabes_ship_glam_img
player_3 = Player(players, 'player_3', anikas_ship_img, None, copy.copy(player_engine), copy.copy(player_armor), create_weapon_list())
player_3.glam_image = anikas_ship_glam_img
player_4 = Player(players, 'player_4', aletheas_ship_img, None, copy.copy(player_engine), copy.copy(player_armor), create_weapon_list())
player_4.glam_image = aletheas_ship_glam_img
player_5 = Player(players, 'player_4', basic_ship_img, None, copy.copy(player_engine), copy.copy(player_armor), create_weapon_list())

# assign controllers
for i, player in enumerate(players['all']):
    player.controller_number = i 

class Game:
    def __init__(self, screen, states, start_state):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.screen = screen

        self.boundary = self.surface.get_rect()
        self.inflated_boundary = self.boundary.inflate(0, BOUNDARY_MARGIN)

        self.states = states
        self.state = self.states[start_state]

        self.running = True

        # fr indep
        self.prev_time = None
        self.dt = None

    def change_state(self, new_state):
        self.state.over = False # reset state for future use
        self.state = self.states[new_state]
        self.state.reset(self.boundary)

    def quit(self):
        self.running = False

    def run(self):
        self.prev_time = time.time()

        while self.running:
            
            current_time = time.time()
            self.dt = min(current_time - self.prev_time, 0.05) # cap dt at 50ms, FR at 20fps
            self.prev_time = current_time

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.state.handle_input(events)
            self.state.update(self.dt)
            self.state.draw(self.surface)
            self.scaled_surface = pygame.transform.scale(self.surface, screen.get_size())
            self.screen.blit(self.scaled_surface, (0, 0))

            if self.state.over:
                self.change_state(self.state.next_state)
            if self.state.quit:
                self.running = False

            pygame.display.update()

            self.clock.tick(FRAMERATE_SET) #set FPS

        pygame.quit()

game = Game(screen, states, 'splash')

game.run()