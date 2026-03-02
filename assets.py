import pygame
from constants import *
from display import screen

# load fonts
try:
    font_lg = pygame.font.SysFont('Consolas', 40)
    font_md = pygame.font.SysFont('Consolas', 30)
except:
    font_lg = pygame.font.Font(None, 40) 
    font_md = pygame.font.Font(None, 30) 

# load images

# background images
nebula_1_img = pygame.transform.scale(pygame.image.load("images/nebula_1.png").convert_alpha(), (GAME_WIDTH, GAME_HEIGHT))
nebula_2_img = pygame.transform.scale(pygame.image.load("images/nebula_2.png").convert_alpha(), (GAME_WIDTH, GAME_HEIGHT))
nebula_3_img = pygame.transform.scale(pygame.image.load("images/nebula_3.png").convert_alpha(), (GAME_WIDTH, GAME_HEIGHT))
nebula_4_img = pygame.transform.scale(pygame.image.load("images/nebula_4.png").convert_alpha(), (GAME_WIDTH, GAME_HEIGHT))
nebula_5_img = pygame.transform.scale(pygame.image.load("images/nebula_5.png").convert_alpha(), (GAME_WIDTH, GAME_HEIGHT))
nebula_6_img = pygame.transform.scale(pygame.image.load("images/nebula_6.jpg").convert_alpha(), (GAME_WIDTH, GAME_HEIGHT))
nebula_7_img = pygame.transform.scale(pygame.image.load("images/nebula_7.jpg").convert_alpha(), (GAME_WIDTH, GAME_HEIGHT))

# stars
stars_near_img = pygame.transform.scale(pygame.image.load("images/stars_near.png").convert_alpha(), (GAME_WIDTH*2, GAME_HEIGHT))
stars_mid_img = pygame.transform.scale(pygame.image.load("images/stars_mid.png").convert_alpha(), (GAME_WIDTH*2, GAME_HEIGHT))
stars_far_img = pygame.transform.scale(pygame.image.load("images/stars_far.png").convert_alpha(), (GAME_WIDTH*2, GAME_HEIGHT))

# ship images
basic_ship_img = pygame.transform.scale(pygame.image.load("images/ship_1_render_1.png").convert_alpha(), (256, 256))
gabes_ship_img = pygame.transform.scale(pygame.image.load("images/gabes_ship_1.1.png").convert_alpha(), (256, 256))
gabes_ship_glam_img = pygame.transform.scale(pygame.image.load("images/gabes_ship_1.1_glam.png").convert_alpha(), (1028, 1028))
anikas_ship_img = pygame.transform.scale(pygame.image.load("images/anikas_ship_1.png").convert_alpha(), (256, 256))
anikas_ship_glam_img =  pygame.transform.scale(pygame.image.load("images/anikas_ship_1_glam.png").convert_alpha(), (1028, 1028))
aletheas_ship_img = pygame.transform.scale(pygame.image.load("images/aletheas_ship_2.png").convert_alpha(), (256, 256))
aletheas_ship_glam_img = pygame.transform.scale(pygame.image.load("images/aletheas_ship_2_glam.png").convert_alpha(), (1028, 1028))
noeys_ship_img = pygame.transform.scale(pygame.image.load("images/noeys_ship_2.png").convert_alpha(), (256, 256))
noeys_ship_glam_img = pygame.transform.scale(pygame.image.load("images/noeys_ship_2_glam.png").convert_alpha(), (1028, 1028))

# parts images
engine_icon_0 = pygame.transform.scale(pygame.image.load("images/engine_icon_0.png").convert_alpha(), (256, 256))
armor_icon_0 = pygame.transform.scale(pygame.image.load("images/armor_icon_0.png").convert_alpha(), (256, 256))

# enemy images
saucer_1_img = pygame.transform.scale(pygame.image.load("images/saucer_1.png").convert_alpha(), (128, 128))
saucer_1_big_img = pygame.transform.scale(pygame.image.load("images/saucer_1.png").convert_alpha(), (256, 256))
saucer_1_mini_img = pygame.transform.scale(pygame.image.load("images/saucer_1.png").convert_alpha(), (64, 64))
saucer_2_img = pygame.transform.scale(pygame.image.load("images/saucer_2.png").convert_alpha(), (128, 128))
saucer_2_boss_img = pygame.transform.scale(pygame.image.load("images/saucer_2.png").convert_alpha(), (512, 512))

# projectile images
# player
sm_laser_bolt_img = pygame.transform.scale(pygame.image.load("images/sm_laser_bolt_2.png").convert_alpha(), (32, 32))
gumball_img = pygame.transform.scale(pygame.image.load("images/gumball.png").convert_alpha(), (32, 32))
lava_ball_img = pygame.transform.scale(pygame.image.load("images/lava_ball.png").convert_alpha(), (64, 64))
beam_laser_img = pygame.image.load("images/beam_laser_proj.png").convert_alpha()
ice_ray_img = pygame.image.load("images/ice_ray_proj.png").convert_alpha()
mine_img = pygame.image.load("images/mine.png").convert_alpha()
rocket_img = pygame.transform.scale(pygame.image.load("images/rocket.png").convert_alpha(), (64, 64))

sm_laser_icon = pygame.transform.scale(pygame.image.load("images/sm_laser_icon_0.png").convert_alpha(), (256, 256))
gum_blaster_icon = pygame.transform.scale(pygame.image.load("images/gum_blaster_icon_0.png").convert_alpha(), (256, 256))
lava_blaster_icon = pygame.transform.scale(pygame.image.load("images/lava_blaster_icon_0.png").convert_alpha(), (256, 256))
beam_laser_icon = pygame.transform.scale(pygame.image.load("images/beam_laser_icon_0.png").convert_alpha(), (256, 256))
ice_ray_icon = pygame.transform.scale(pygame.image.load("images/ice_ray_icon_0.png").convert_alpha(), (256, 256))

#enemy
enemy_laser_bolt_img = pygame.transform.scale(pygame.image.load("images/enemy_laser_bolt.png").convert_alpha(), (32, 32))