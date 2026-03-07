import copy, random
from constants import *
from utils import rng
from assets import*
from groups import *
from entities import *
from components import *
from physics import *

class EnemyGenerator:
    def __init__(self, image, base_hp, weapon):
        self.image = image
        self.base_hp = base_hp
        self.weapon = weapon
    
    def generate(self, position, speed, move_pattern):
        scaled_hp = self.base_hp * len(players['all']) / 2
        return Enemy(enemies,
            f"enemy_{len(enemies)}+1", 
            self.image, 
            scaled_hp, 
            position, 
            speed,
            move_pattern,
            self.weapon)
    
class SpawnCommand:
    def __init__(self, generator, *args, **kwargs):
        self.generator = generator
        self.args = args
        self.kwargs = kwargs
    
    def execute(self):
        self.generator.generate(*self.args, **self.kwargs)

class CommandGroup:
    def __init__(self, *commands):
        self.commands = commands
    
    def execute(self):
        for command in self.commands:
            command.execute()

basic_saucer = EnemyGenerator(saucer_1_img, 100, None)
mini_saucer = EnemyGenerator(saucer_1_mini_img, 50, None)
big_saucer = EnemyGenerator(saucer_1_big_img, 2000, None)
shooting_saucer = EnemyGenerator(saucer_2_img, 100, copy.copy(enemy_laser_template))
fast_shooting_saucer = EnemyGenerator(saucer_2_img, 100, copy.copy(enemy_fast_laser_template))
boss_1 = EnemyGenerator(saucer_2_boss_img, 10000, copy.copy(enemy_laser_template))

tenth = GAME_HEIGHT/10

level_1_seq = {
    # Original solo spawns, but minis start appearing to harass
    0: SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 3, ConstX()),
    60: CommandGroup(
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 5, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 5, gentle_sine)),
    120: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 3, sine_pattern),
    240: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 3, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*3), 5, crazy_sine)),
    360: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 3, sine_pattern),
    480: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 3, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 5, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 5, gentle_sine)),
    600: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 3, sine_pattern),
    720: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 3, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*4), 6, crazy_sine)),
    840: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 3, sine_pattern),
    960: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 3, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 5, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*7), 5, crazy_sine)),
    1080: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 3, sine_pattern),
    1200: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 3, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*3), 6, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*7), 6, gentle_sine)),
    1320: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 3, sine_pattern),
    1440: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 3, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 6, crazy_sine)),
    1560: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 3, sine_pattern),
    1680: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 3, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 6, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 6, crazy_sine)),
    1800: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 3, sine_pattern),
    1920: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 3, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, tenth*3), 2, gentle_sine)),
    2040: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 3, sine_pattern),
    2160: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 3, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*2), 6, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*8), 6, crazy_sine)),
    2280: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 3, sine_pattern),
    2700: None
}

level_2_seq = {
    0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 3, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 3), 2, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, 2 * GAME_HEIGHT / 3), 2.5, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 6, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 6, crazy_sine)),
    300: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 2.5, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 3), 5, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, 2 * GAME_HEIGHT / 3), 3, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*4), 6, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*6), 6, gentle_sine)),
    600: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 2, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 4), 3, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, 2 * GAME_HEIGHT / 3), 2.5, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, 3 * GAME_HEIGHT / 4), 3, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, 4 * GAME_HEIGHT / 5), 2, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*2), 7, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*5), 7, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*8), 7, crazy_sine)),
    900: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, GAME_HEIGHT / 2), 2, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 4), 3, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, 2 * GAME_HEIGHT / 3), 2.5, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, 3 * GAME_HEIGHT / 4), 2, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, 4 * GAME_HEIGHT / 5), 1, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 384, tenth*3), 7, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 384, tenth*7), 7, crazy_sine)),
    1200: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, rng.uniform(1, 10, 1)[0]*tenth), 1, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, rng.uniform(1, 10, 1)[0]*tenth), 2, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, rng.uniform(1, 10, 1)[0]*tenth), 1.5, gentle_sine),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, rng.uniform(1, 10, 1)[0]*tenth), 2.5, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, rng.uniform(1, 10, 1)[0]*tenth), 1, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 7, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 7, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 7, crazy_sine)),
    1500: None
}

level_3_seq = {
    60: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*2), 3, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*4), 3, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*6), 3, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*8), 3, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*1), 7, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*5), 7, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*9), 7, crazy_sine)),
    120: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 1.7, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 - 64), 1.7, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 + 64), 1.7, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 - 128), 1.7, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 + 128), 1.7, gentle_sine),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 - 172), 1.7, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 + 172), 1.7, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 8, crazy_sine)),
    500: CommandGroup(
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 8, crazy_sine)),
    720: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 3, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 - 64), 3, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 + 64), 3, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 - 128), 3, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 + 128), 3, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 - 172), 3, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 + 172), 3, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 2, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 2, gentle_sine)),
    1100: CommandGroup(
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*3), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*7), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 8, crazy_sine)),
    1440: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 3, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 - 64), 3, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 + 64), 3, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 - 128), 3, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 + 128), 3, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 - 172), 3, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 + 172), 3, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*2), 2.5, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*8), 2.5, sine_pattern)),
    2040: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 2.2, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 - 64), 2.2, gentle_sine),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 + 64), 2.2, gentle_sine),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 - 128), 2.2, gentle_sine),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 + 128), 2.2, gentle_sine),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 - 172), 2.2, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 + 172), 2.2, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*1), 2, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*9), 2, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 384, tenth*3), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 384, tenth*7), 8, crazy_sine)),
    3240: None
}

level_4_seq = {
    120: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 3, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*3), 3, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*5), 3, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*7), 3, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*9), 3, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 7, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*2), 7, crazy_sine)),
    480: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 2.2, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 - 64), 2.2, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 + 64), 2.2, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 - 128), 2.2, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 + 128), 2.2, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 - 172), 2.2, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 + 172), 2.2, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*1), 2.5, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*9), 2.5, gentle_sine)),
    600: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 3, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*7), 3, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*5), 3, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*3), 3, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth), 3, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 7, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 7, crazy_sine)),
    1000: CommandGroup(
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*3), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*7), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 8, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 2, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 2, sine_pattern)),
    1600: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 3, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*3), 3, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*5), 3, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*7), 3, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*9), 3, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*4), 2, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*6), 2, crazy_sine)),
    2080: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 3, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*7), 3, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*5), 3, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*3), 3, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth), 3, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 8, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 2.5, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 2.5, gentle_sine)),
    3000: None
}

level_5_seq = {
    120: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 1, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 8, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 1, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 8, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*3), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*5), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*7), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*9), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*3), 1, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*5), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*7), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*9), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*3), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*5), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*7), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*9), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*3), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*5), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*7), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*9), 1, ConstX())),
    800: CommandGroup(
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*3), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*7), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 8, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 2, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 2, gentle_sine)),
    2000: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 1, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 8, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*3), 1, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*7), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*9), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*3), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*5), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*7), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*9), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*3), 1, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 512, tenth*5), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*7), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*9), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*3), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*5), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*7), 1, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 640, tenth*9), 1, crazy_sine)),
    3000: None
}

level_6_seq = {
    60: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, tenth*2), 1, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, tenth*4), 1, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, tenth*6), 1, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, tenth*8), 1, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 8, crazy_sine)),
    300: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 6, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 2, gentle_sine)),
    450: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 10, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 8, crazy_sine)),
    600: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 6, gentle_sine),
    750: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 10, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 2.5, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 2.5, sine_pattern)),
    760: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, tenth*2), 1, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, tenth*4), 1, gentle_sine),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, tenth*6), 1, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, tenth*8), 1, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 384, tenth*3), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 384, tenth*7), 8, crazy_sine)),
    900: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 6, gentle_sine),
    1020: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 6, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 2, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 2, crazy_sine)),
    1500: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, tenth*2), 1.5, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 1.5, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, tenth*6), 1.5, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 1.5, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 8, crazy_sine)),
    1800: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 6, gentle_sine),
    1950: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 10, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 2, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 2, sine_pattern)),
    2100: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 6, gentle_sine),
    2250: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 10, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 8, crazy_sine)),
    2400: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 6, gentle_sine),
    2700: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 6, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 2, crazy_sine)),
    3000: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 1, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, tenth*7), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 1, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 8, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 8, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*3), 1, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*7), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*9), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*3), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*5), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*7), 1, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*9), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth), 1, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 512, tenth*3), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*5), 1, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*7), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*9), 1, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 640, tenth), 1, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*3), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*5), 1, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 640, tenth*7), 1, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*9), 1, gentle_sine)),
    3800: SpawnCommand(big_saucer, (GAME_WIDTH + 256, tenth*5), 1, ConstX()),
    4000: None
}

level_7_seq = {
    60: CommandGroup(
        SpawnCommand(big_saucer, (GAME_WIDTH + 128, tenth*2), 1, gentle_sine),
        SpawnCommand(big_saucer, (GAME_WIDTH + 256, tenth*4), 1, gentle_sine),
        SpawnCommand(big_saucer, (GAME_WIDTH + 128, tenth*6), 1, ConstX()),
        SpawnCommand(big_saucer, (GAME_WIDTH + 256, tenth*8), 1, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 9, crazy_sine)),
    300: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 6, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 2, sine_pattern)),
    450: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 10, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 9, crazy_sine)),
    600: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 6, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 2.5, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 2.5, gentle_sine)),
    750: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 10, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 9, crazy_sine)),
    950: CommandGroup(
        SpawnCommand(big_saucer, (GAME_WIDTH + 128, tenth*2), 1, ConstX()),
        SpawnCommand(big_saucer, (GAME_WIDTH + 256, tenth*4), 1, sine_pattern),
        SpawnCommand(big_saucer, (GAME_WIDTH + 128, tenth*6), 1, sine_pattern),
        SpawnCommand(big_saucer, (GAME_WIDTH + 256, tenth*8), 1, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*3), 2, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*7), 2, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 9, crazy_sine)),
    1200: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 6, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 9, crazy_sine)),
    1300: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 10, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 2.5, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 2.5, sine_pattern)),
    1500: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 6, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*3), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*7), 9, crazy_sine)),
    1550: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 10, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 2.5, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 2.5, crazy_sine)),
    1900: CommandGroup(
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*3), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*7), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 9, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 2, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 2, crazy_sine)),
    2500: None
}

level_8_seq = {
    # Opening squeeze columns + mini harassers right away
    60: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*1), 5, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*1), 5, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*1), 5, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 5, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*9), 5, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*9), 5, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*5), 9, crazy_sine)),
    400: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*2), 5, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*2), 5, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*2), 5, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*8), 5, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*8), 5, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*8), 5, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 9, crazy_sine)),
    800: CommandGroup(
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 128, tenth*3), 5, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*3), 4, ConstX()),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 384, tenth*3), 5, gentle_sine),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 128, tenth*7), 5, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*7), 4, ConstX()),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 384, tenth*7), 5, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 512, tenth*3), 3, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 512, tenth*7), 3, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 9, crazy_sine)),
    # Columns meet -- fast shooters and minis clog the middle
    1200: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*4), 3, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 3, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*6), 3, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*4), 3, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 512, tenth*5), 3, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*6), 3, gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*2), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*8), 9, crazy_sine)),
    # Second squeeze -- faster, tighter, with mini swarm
    1800: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*1), 7, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*2), 7, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*1), 7, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*2), 7, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 7, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*8), 7, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*9), 7, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*8), 7, ConstX()),
        SpawnCommand(mini_saucer,  (GAME_WIDTH + 128, tenth*3), 9, crazy_sine),
        SpawnCommand(mini_saucer,  (GAME_WIDTH + 128, tenth*5), 9, crazy_sine),
        SpawnCommand(mini_saucer,  (GAME_WIDTH + 128, tenth*7), 9, crazy_sine)),
    2200: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*3), 4, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 3, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*7), 4, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 3, gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 9, crazy_sine)),
    2600: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*2), 2, gentle_sine),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*5), 2, ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*8), 2, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 3, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 3, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 9, crazy_sine)),
    3200: None
}

level_9_seq = {
    # Opening screen with mini chaos running interference
    60: CommandGroup(
        SpawnCommand(big_saucer,  (GAME_WIDTH + 128, tenth*2), 1.5, gentle_sine),
        SpawnCommand(big_saucer,  (GAME_WIDTH + 256, tenth*4), 1.5, ConstX()),
        SpawnCommand(big_saucer,  (GAME_WIDTH + 128, tenth*6), 1.5, gentle_sine),
        SpawnCommand(big_saucer,  (GAME_WIDTH + 256, tenth*8), 1.5, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 9, crazy_sine)),
    # Boss enters
    300: SpawnCommand(boss_1, (GAME_WIDTH + 512, tenth*5), 1, ConstX()),
    # Harassment wave -- fast shooters added to make camping impossible
    500: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*1), 2, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 2.5, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*3), 2, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*7), 2, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 2.5, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*9), 2, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 9, crazy_sine)),
    # Reinforce the screen
    1000: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*3), 1.5, sine_pattern),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*5), 1.5, ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*7), 1.5, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 9, crazy_sine)),
    1500: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*2), 2.5, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 2.5, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*6), 2.5, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 2.5, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*3), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*7), 9, crazy_sine)),
    # Final screen reinforcement -- all enemy types at once
    2000: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*2), 2, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 2.5, sine_pattern),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*6), 2, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 2.5, sine_pattern),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 384, tenth*4), 2, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 384, tenth*6), 2, gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*8), 9, crazy_sine)),
    2600: CommandGroup(
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*3), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*7), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 9, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 9, crazy_sine)),
    3000: None
}

level_10_seq = {
    # Wave 1: dense basic wall with minis hidden inside
    60: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*1), 4, sine_pattern),
        SpawnCommand(mini_saucer,  (GAME_WIDTH + 128, tenth*2), 9, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 4, gentle_sine),
        SpawnCommand(mini_saucer,  (GAME_WIDTH + 128, tenth*4), 9, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 4, ConstX()),
        SpawnCommand(mini_saucer,  (GAME_WIDTH + 128, tenth*6), 9, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 4, ConstX()),
        SpawnCommand(mini_saucer,  (GAME_WIDTH + 128, tenth*8), 9, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 4, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*1), 4, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*3), 4, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 3, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*7), 4, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*9), 4, gentle_sine)),
    # Wave 2: shooting flood + fast shooters mixed in + minis
    800: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*1), 3, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 3, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*3), 3, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 3, sine_pattern),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*5), 3, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 3, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*7), 3, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 3, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*9), 3, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 9, crazy_sine)),
    # Wave 2b: big saucers + fast shooters + mini swarm
    1200: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*2), 2, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 3, crazy_sine),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 256, tenth*4), 2, ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*6), 2, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 3, crazy_sine),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 256, tenth*8), 2, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 9, crazy_sine)),
    # "Breather" -- still has fast shooters and minis, just fewer big threats
    1900: CommandGroup(
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 128, tenth*3), 6, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 3, sine_pattern),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 128, tenth*7), 6, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 9, crazy_sine)),
    # Wave 3: two bosses with fast escort and full mini screen
    2400: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 512, tenth*3), 1.5, gentle_sine),
        SpawnCommand(boss_1,               (GAME_WIDTH + 512, tenth*7), 1.5, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 2.5, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*5), 2,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 2.5, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 9, crazy_sine)),
    # Final harassment -- everything at once while bosses are alive
    3000: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*1), 3, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*4), 3, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*7), 3, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 3, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 3, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 3, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*4), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*6), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 9, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 9, crazy_sine)),
    4200: None
}

# ── LEVEL 11 ──────────────────────────────────────────────────────────────────
# Theme: Three-front pressure. Big saucers anchor lanes while fast shooters and
# minis deny safe corridors. First level with three simultaneous bosses.
level_11_seq = {
    # Opening: staggered big saucers across all three vertical lanes
    60: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*2), 2,   gentle_sine),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 256, tenth*5), 2,   ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*8), 2,   gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 9,   crazy_sine)),
    # Fast shooters flood the gap left by bigs
    500: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*1), 3.5, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 3.5, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*5), 3.5, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 3.5, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*9), 3.5, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 9,   crazy_sine)),
    # Dense shooting wall
    1000: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*1), 3,   sine_pattern),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*2), 3,   gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*3), 3,   ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*4), 3,   sine_pattern),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*5), 3,   gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*6), 3,   ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*7), 3,   sine_pattern),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*8), 3,   gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*9), 3,   ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 9,   crazy_sine)),
    # Breather - but minis keep coming
    1600: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*3), 2.5, sine_pattern),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*7), 2.5, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 3,   ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 9,   crazy_sine)),
    # Three bosses enter together
    2200: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*2), 1.5, gentle_sine),
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*5), 1.5, ConstX()),
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*8), 1.5, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*1), 3,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*9), 3,   sine_pattern)),
    # Harassment while bosses are alive
    2800: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*2), 3,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*5), 3,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*8), 3,   ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*3), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*7), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 9,   crazy_sine)),
    # Final push - full mini screen + shooters while bosses remain
    3600: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*2), 3.5, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 3.5, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*6), 3.5, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 3.5, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*4), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*6), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 9,   crazy_sine)),
    4800: None
}

# ── LEVEL 12 ──────────────────────────────────────────────────────────────────
# Theme: No rest. Short gaps between waves, bosses arrive in two separate pairs,
# fast shooters are now the baseline filler enemy throughout.
level_12_seq = {
    # Dense mixed opening - fast shooters from the start
    60: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*1), 4,   sine_pattern),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 256, tenth*2), 4,   gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*3), 4,   ConstX()),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 256, tenth*4), 4,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*5), 4,   gentle_sine),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 256, tenth*6), 4,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*7), 4,   sine_pattern),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 256, tenth*8), 4,   gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*9), 4,   ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 9,   crazy_sine)),
    # Big saucers as shields for shooters behind them
    450: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*2), 2.5, ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*5), 2.5, gentle_sine),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*8), 2.5, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*2), 2.5, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*5), 2.5, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*8), 2.5, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 9,   crazy_sine)),
    # First boss pair - escorted by fast shooters immediately
    900: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*3), 2,   sine_pattern),
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*7), 2,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*1), 3,   gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 3,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*9), 3,   gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*2), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*8), 9,   crazy_sine)),
    # Filler while first bosses are still alive
    1500: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*2), 3.5, sine_pattern),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*4), 3.5, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*6), 3.5, sine_pattern),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*8), 3.5, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 9,   crazy_sine)),
    # Second boss pair arrives before the first pair may be dead
    2100: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*2), 1.5, gentle_sine),
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*8), 1.5, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*4), 3,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*6), 3,   sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*9), 9,   crazy_sine)),
    # Full-screen denial
    2800: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*2), 2,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 3.5, sine_pattern),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*5), 2,   gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 3.5, ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*8), 2,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*9), 3.5, gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*4), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*6), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 9,   crazy_sine)),
    # Third boss - solo but with maximum escort
    3500: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 768, tenth*5), 2,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 4,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 4,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 4,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 4,   sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*3), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*7), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 9,   crazy_sine)),
    # Last gasp while boss still lives
    4300: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*1), 4,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 4,   gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*5), 4,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 4,   gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*9), 4,   sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*4), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*6), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 9,   crazy_sine)),
    5400: None
}

# ── LEVEL 13 ──────────────────────────────────────────────────────────────────
# Theme: Total war. Four bosses total across the level, back-to-back mini screens,
# fast shooters as the default enemy, and no true gaps anywhere.
level_13_seq = {
    # Wall of fast shooters immediately — no warmup
    0: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*1), 5,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 5,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*3), 5,   gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 5,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*5), 5,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 5,   gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*7), 5,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 5,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*9), 5,   gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 9,   crazy_sine)),
    # Big saucers + hidden fast shooters behind them
    400: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*1), 3,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*1), 3,   ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*3), 3,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*3), 3,   sine_pattern),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*5), 3,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*5), 3,   ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*7), 3,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*7), 3,   sine_pattern),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*9), 3,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*9), 3,   ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*2), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*4), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*6), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*8), 9,   crazy_sine)),
    # First boss - arrives early, players are still worn down from opening
    800: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 768, tenth*5), 2,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 4,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 4,   ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 9,   crazy_sine)),
    # Reinforce before boss might be dead
    1200: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*2), 4,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 4,   gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*6), 4,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 4,   gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 9,   crazy_sine)),
    # Second boss + escort while first may still be alive
    1700: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*3), 2,   gentle_sine),
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*7), 2,   gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*1), 4,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 4,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*9), 4,   sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*2), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*8), 9,   crazy_sine)),
    # Full mini screen + fast shooters - maximum clutter
    2300: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*1), 4,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*3), 4,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*5), 4,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*7), 4,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*9), 4,   ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*2), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*3), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*4), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*6), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*7), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*8), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*9), 9,   crazy_sine)),
    # Third boss + big saucer formation
    3000: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 768, tenth*5), 2.5, gentle_sine),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 256, tenth*2), 3,   ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 256, tenth*4), 3,   sine_pattern),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 256, tenth*6), 3,   ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 256, tenth*8), 3,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 512, tenth*3), 4,   gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 512, tenth*7), 4,   gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 9,   crazy_sine)),
    # Never-ending harassment while boss 3 is alive
    3700: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*2), 4,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 4,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*6), 4,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 4,   sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*4), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*6), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 9,   crazy_sine)),
    # Fourth and final boss - everything at maximum
    4500: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 768, tenth*3), 2.5, sine_pattern),
        SpawnCommand(boss_1,               (GAME_WIDTH + 768, tenth*7), 2.5, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 4,   gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 4,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 4,   gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*3), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*7), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 9,   crazy_sine)),
    5400: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*1), 4,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 4,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*3), 4,   gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 4,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*5), 4,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 4,   gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*7), 4,   sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 4,   ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*9), 4,   gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*4), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*6), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 9,   crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 9,   crazy_sine)),
    6000: None
}

class GameLevel:
    def __init__(self, program, background):
        self.program = program
        self.background = background
        self.over = False

    def update(self, timer):
        if timer in self.program:
            if self.program[timer] is not None:
                self.program[timer].execute()
            if timer == max(self.program.keys()):
                self.over = True

game_levels = [
    GameLevel(level_1_seq, nebula_1_img),
    GameLevel(level_2_seq, nebula_2_img),
    GameLevel(level_3_seq, nebula_3_img),
    GameLevel(level_4_seq, nebula_4_img),
    GameLevel(level_5_seq, nebula_5_img),
    GameLevel(level_6_seq, nebula_6_img),
    GameLevel(level_7_seq, nebula_7_img),
    GameLevel(level_8_seq, nebula_3_img),   # recycled backgrounds for 8-10
    GameLevel(level_9_seq, nebula_5_img),
    GameLevel(level_10_seq, nebula_7_img),
    GameLevel(level_11_seq, nebula_1_img),
    GameLevel(level_12_seq, nebula_4_img),
    GameLevel(level_13_seq, nebula_7_img)
]