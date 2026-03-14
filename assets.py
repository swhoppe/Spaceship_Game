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

# image loader
def load_image(path, size=None):
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img

# background images
nebula_1_img = load_image("images/nebula_1.png", (GAME_WIDTH, GAME_HEIGHT))
nebula_2_img = load_image("images/nebula_2.png", (GAME_WIDTH, GAME_HEIGHT))
nebula_3_img = load_image("images/nebula_3.png", (GAME_WIDTH, GAME_HEIGHT))
nebula_4_img = load_image("images/nebula_4.png", (GAME_WIDTH, GAME_HEIGHT))
nebula_5_img = load_image("images/nebula_5.png", (GAME_WIDTH, GAME_HEIGHT))
nebula_6_img = load_image("images/nebula_6.jpg", (GAME_WIDTH, GAME_HEIGHT))
nebula_7_img = load_image("images/nebula_7.jpg", (GAME_WIDTH, GAME_HEIGHT))

# stars
stars_near_img = load_image("images/stars_near.png", (GAME_WIDTH*2, GAME_HEIGHT))
stars_mid_img = load_image("images/stars_mid.png", (GAME_WIDTH*2, GAME_HEIGHT))
stars_far_img = load_image("images/stars_far.png", (GAME_WIDTH*2, GAME_HEIGHT))

# ship images
basic_ship_img = load_image("images/ship_1_render_1.png", (256, 256))
gabes_ship_img = load_image("images/gabes_ship_1.1.png", (256, 256))
gabes_ship_glam_img = load_image("images/gabes_ship_1.1_glam.png", (1028, 1028))
anikas_ship_img = load_image("images/anikas_ship_1.png", (256, 256))
anikas_ship_glam_img =  load_image("images/anikas_ship_1_glam.png", (1028, 1028))
aletheas_ship_img = load_image("images/aletheas_ship_2.png", (256, 256))
aletheas_ship_glam_img = load_image("images/aletheas_ship_2_glam.png", (1028, 1028))
noeys_ship_img = load_image("images/noeys_ship_2.png", (256, 256))
noeys_ship_glam_img = load_image("images/noeys_ship_2_glam.png", (1028, 1028))

# parts images
engine_icon_0 = load_image("images/engine_icon_0.png", (256, 256))
armor_icon_0 = load_image("images/armor_icon_0.png", (256, 256))

# enemy images
saucer_1_img = load_image("images/saucer_1.png", (128, 128))
saucer_1_big_img = load_image("images/saucer_1.png", (256, 256))
saucer_1_mini_img = load_image("images/saucer_1.png", (64, 64))
saucer_2_img = load_image("images/saucer_2.png", (128, 128))
saucer_2_boss_img = load_image("images/saucer_2.png", (512, 512))

# projectile images
# player
sm_laser_bolt_img = load_image("images/sm_laser_bolt_2.png", (32, 32))
gumball_img = load_image("images/gumball.png", (32, 32))
lava_ball_img = load_image("images/lava_ball.png", (64, 64))
beam_laser_img = load_image("images/beam_laser_proj.png")
ice_ray_img = load_image("images/ice_ray_proj.png")
mine_img = load_image("images/mine.png")
rocket_img = load_image("images/rocket.png")

sm_laser_icon = load_image("images/sm_laser_icon_0.png", (256, 256))
gum_blaster_icon = load_image("images/gum_blaster_icon_0.png", (256, 256))
lava_blaster_icon = load_image("images/lava_blaster_icon_0.png", (256, 256))
beam_laser_icon = load_image("images/beam_laser_icon_0.png", (256, 256))
ice_ray_icon = load_image("images/ice_ray_icon_0.png", (256, 256))

#enemy
enemy_laser_bolt_img = load_image("images/enemy_laser_bolt.png", (32, 32))

# effect images
gum_splat_img = load_image("images/gum_splat.png", (64, 64))
lava_splat_img = load_image("images/lava_splat.png", (128, 128))