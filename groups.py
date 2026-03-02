import pygame

all_players = pygame.sprite.Group()
active_players = pygame.sprite.Group()
players = {'all': all_players, 'active' : active_players}
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
effects = pygame.sprite.Group()