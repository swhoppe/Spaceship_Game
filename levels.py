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
0.0: SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 180, ConstX()),
1.0: CommandGroup(
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 300, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 300, gentle_sine)),
2.0: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 180, sine_pattern),
4.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 180, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*3), 300, crazy_sine)),
6.0: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 180, sine_pattern),
8.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*4), 180, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 300, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 300, gentle_sine)),
10.0: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*6), 180, sine_pattern),
12.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 180, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*4), 360, crazy_sine)),
14.0: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*8), 180, sine_pattern),
16.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*4), 180, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 300, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*7), 300, crazy_sine)),
18.0: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 180, sine_pattern),
20.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 180, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*3), 360, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*7), 360, gentle_sine)),
22.0: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*6), 180, sine_pattern),
24.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*8), 180, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 360, crazy_sine)),
26.0: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 180, sine_pattern),
28.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 180, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 360, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 360, crazy_sine)),
30.0: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*4), 180, sine_pattern),
32.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*8), 180, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, tenth*3), 120, gentle_sine)),
34.0: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*2), 180, sine_pattern),
36.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*6), 180, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*2), 360, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*8), 360, crazy_sine)),
38.0: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*4), 180, sine_pattern),
45.0: None
}

level_2_seq = {
0.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 180, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 3), 120, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, 2 * GAME_HEIGHT / 3), 150, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 360, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 360, crazy_sine)),
5.0: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 150, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 3), 300, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, 2 * GAME_HEIGHT / 3), 180, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*4), 360, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*6), 360, gentle_sine)),
10.0: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 120, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 4), 180, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, 2 * GAME_HEIGHT / 3), 150, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, 3 * GAME_HEIGHT / 4), 180, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, 4 * GAME_HEIGHT / 5), 120, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*2), 420, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*5), 420, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*8), 420, crazy_sine)),
15.0: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, GAME_HEIGHT / 2), 120, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 4), 180, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, 2 * GAME_HEIGHT / 3), 150, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, 3 * GAME_HEIGHT / 4), 120, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, 4 * GAME_HEIGHT / 5), 60, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 384, tenth*3), 420, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 384, tenth*7), 420, crazy_sine)),
20.0: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, rng.uniform(1, 10, 1)[0]*tenth), 60, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, rng.uniform(1, 10, 1)[0]*tenth), 120, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, rng.uniform(1, 10, 1)[0]*tenth), 90, gentle_sine),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, rng.uniform(1, 10, 1)[0]*tenth), 150, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, rng.uniform(1, 10, 1)[0]*tenth), 60, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 420, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 420, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 420, crazy_sine)),
25.0: None
}

level_3_seq = {
1.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*2), 180, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*4), 180, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*6), 180, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*8), 180, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*1), 420, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*5), 420, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*9), 420, crazy_sine)),
2.0: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 102, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 - 64), 102, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 + 64), 102, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 - 128), 102, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 + 128), 102, gentle_sine),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 - 172), 102, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 + 172), 102, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 480, crazy_sine)),
8.3333: CommandGroup(
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 480, crazy_sine)),
12.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 180, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 - 64), 180, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 + 64), 180, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 - 128), 180, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 + 128), 180, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 - 172), 180, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 + 172), 180, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 120, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 120, gentle_sine)),
18.3333: CommandGroup(
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*3), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*7), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 480, crazy_sine)),
24.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 180, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 - 64), 180, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 + 64), 180, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 - 128), 180, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 + 128), 180, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 - 172), 180, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 + 172), 180, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*2), 150, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*8), 150, sine_pattern)),
34.0: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 132, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 - 64), 132, gentle_sine),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 + 64), 132, gentle_sine),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 - 128), 132, gentle_sine),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 + 128), 132, gentle_sine),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 - 172), 132, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 + 172), 132, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*1), 120, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*9), 120, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 384, tenth*3), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 384, tenth*7), 480, crazy_sine)),
54.0: None
}

level_4_seq = {
2.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 180, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*3), 180, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*5), 180, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*7), 180, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*9), 180, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 420, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*2), 420, crazy_sine)),
8.0: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, GAME_HEIGHT / 2), 132, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 - 64), 132, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, GAME_HEIGHT/2 + 64), 132, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 - 128), 132, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 384, GAME_HEIGHT/2 + 128), 132, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 - 172), 132, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 512, GAME_HEIGHT/2 + 172), 132, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*1), 150, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*9), 150, gentle_sine)),
10.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 180, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*7), 180, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*5), 180, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*3), 180, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth), 180, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 420, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 420, crazy_sine)),
16.6667: CommandGroup(
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*3), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*7), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 480, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 120, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 120, sine_pattern)),
26.6667: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 180, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*3), 180, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*5), 180, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*7), 180, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*9), 180, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*4), 120, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*6), 120, crazy_sine)),
34.6667: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 180, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*7), 180, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*5), 180, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*3), 180, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth), 180, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 480, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 150, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 150, gentle_sine)),
50.0: None
}

level_5_seq = {
2.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 60, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 480, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 60, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 480, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*3), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*5), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*7), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*9), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*3), 60, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*5), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*7), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*9), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*3), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*5), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*7), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*9), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*3), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*5), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*7), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*9), 60, ConstX())),
13.3333: CommandGroup(
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*3), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*7), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 480, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 120, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 120, gentle_sine)),
33.3333: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 60, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 480, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*3), 60, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*7), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*9), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*3), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*5), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*7), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*9), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*3), 60, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 512, tenth*5), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*7), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*9), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*3), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*5), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*7), 60, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 640, tenth*9), 60, crazy_sine)),
50.0: None
}

level_6_seq = {
1.0: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, tenth*2), 60, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, tenth*4), 60, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, tenth*6), 60, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, tenth*8), 60, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 480, crazy_sine)),
5.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 360, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 120, gentle_sine)),
7.5: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 600, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 480, crazy_sine)),
10.0: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 360, gentle_sine),
12.5: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 600, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 150, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 150, sine_pattern)),
12.6667: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, tenth*2), 60, ConstX()),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, tenth*4), 60, gentle_sine),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, tenth*6), 60, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 256, tenth*8), 60, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 384, tenth*3), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 384, tenth*7), 480, crazy_sine)),
15.0: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 360, gentle_sine),
17.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 360, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 120, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 120, crazy_sine)),
25.0: CommandGroup(
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, tenth*2), 90, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 90, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, tenth*6), 90, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 90, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 480, crazy_sine)),
30.0: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 360, gentle_sine),
32.5: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 600, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 120, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 120, sine_pattern)),
35.0: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 360, gentle_sine),
37.5: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 600, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 480, crazy_sine)),
40.0: SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 360, gentle_sine),
45.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 360, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 120, crazy_sine)),
50.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 60, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 128, tenth*7), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 60, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 480, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 480, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*3), 60, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*7), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*9), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*3), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*5), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*7), 60, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*9), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth), 60, sine_pattern),
        SpawnCommand(shooting_saucer, (GAME_WIDTH + 512, tenth*3), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*5), 60, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*7), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*9), 60, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 640, tenth), 60, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*3), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*5), 60, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 640, tenth*7), 60, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 640, tenth*9), 60, gentle_sine)),
63.3333: SpawnCommand(big_saucer, (GAME_WIDTH + 256, tenth*5), 60, ConstX()),
66.6667: None
}

level_7_seq = {
1.0: CommandGroup(
        SpawnCommand(big_saucer, (GAME_WIDTH + 128, tenth*2), 60, gentle_sine),
        SpawnCommand(big_saucer, (GAME_WIDTH + 256, tenth*4), 60, gentle_sine),
        SpawnCommand(big_saucer, (GAME_WIDTH + 128, tenth*6), 60, ConstX()),
        SpawnCommand(big_saucer, (GAME_WIDTH + 256, tenth*8), 60, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
5.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 360, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 120, sine_pattern)),
7.5: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 600, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 540, crazy_sine)),
10.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 360, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 150, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 150, gentle_sine)),
12.5: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 600, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 540, crazy_sine)),
15.8333: CommandGroup(
        SpawnCommand(big_saucer, (GAME_WIDTH + 128, tenth*2), 60, ConstX()),
        SpawnCommand(big_saucer, (GAME_WIDTH + 256, tenth*4), 60, sine_pattern),
        SpawnCommand(big_saucer, (GAME_WIDTH + 128, tenth*6), 60, sine_pattern),
        SpawnCommand(big_saucer, (GAME_WIDTH + 256, tenth*8), 60, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*3), 120, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*7), 120, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 540, crazy_sine)),
20.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 360, sine_pattern),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
21.6667: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 600, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 150, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 150, sine_pattern)),
25.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 360, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*7), 540, crazy_sine)),
25.8333: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth), 600, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 150, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 150, crazy_sine)),
31.6667: CommandGroup(
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*7), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 540, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 120, crazy_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 120, crazy_sine)),
41.6667: None
}

level_8_seq = {
    # Opening squeeze columns + mini harassers right away
1.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*1), 300, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*1), 300, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*1), 300, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 300, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*9), 300, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*9), 300, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 256, tenth*5), 540, crazy_sine)),
6.6667: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*2), 300, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*2), 300, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*2), 300, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*8), 300, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*8), 300, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*8), 300, gentle_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 540, crazy_sine)),
13.3333: CommandGroup(
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 128, tenth*3), 300, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*3), 240, ConstX()),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 384, tenth*3), 300, gentle_sine),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 128, tenth*7), 300, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*7), 240, ConstX()),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 384, tenth*7), 300, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 512, tenth*3), 180, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 512, tenth*7), 180, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
    # Columns meet -- fast shooters and minis clog the middle
20.0: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*4), 180, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 180, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*6), 180, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*4), 180, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 512, tenth*5), 180, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*6), 180, gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*8), 540, crazy_sine)),
    # Second squeeze -- faster, tighter, with mini swarm
30.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*1), 420, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*2), 420, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*1), 420, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*2), 420, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 420, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*8), 420, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 384, tenth*9), 420, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 512, tenth*8), 420, ConstX()),
        SpawnCommand(mini_saucer,  (GAME_WIDTH + 128, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer,  (GAME_WIDTH + 128, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,  (GAME_WIDTH + 128, tenth*7), 540, crazy_sine)),
36.6667: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*3), 240, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 180, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*7), 240, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 180, gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
43.3333: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*2), 120, gentle_sine),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*5), 120, ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*8), 120, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 180, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 180, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 540, crazy_sine)),
53.3333: None
}

level_9_seq = {
    # Opening screen with mini chaos running interference
1.0: CommandGroup(
        SpawnCommand(big_saucer,  (GAME_WIDTH + 128, tenth*2), 90, gentle_sine),
        SpawnCommand(big_saucer,  (GAME_WIDTH + 256, tenth*4), 90, ConstX()),
        SpawnCommand(big_saucer,  (GAME_WIDTH + 128, tenth*6), 90, gentle_sine),
        SpawnCommand(big_saucer,  (GAME_WIDTH + 256, tenth*8), 90, ConstX()),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
    # Boss enters
5.0: SpawnCommand(boss_1, (GAME_WIDTH + 512, tenth*5), 60, ConstX()),
    # Harassment wave -- fast shooters added to make camping impossible
8.3333: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*1), 120, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 150, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*3), 120, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*7), 120, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 150, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*9), 120, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 540, crazy_sine)),
    # Reinforce the screen
16.6667: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*3), 90, sine_pattern),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*5), 90, ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*7), 90, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
25.0: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*2), 150, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 150, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*6), 150, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 150, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*7), 540, crazy_sine)),
    # Final screen reinforcement -- all enemy types at once
33.3333: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*2), 120, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 150, sine_pattern),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*6), 120, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 150, sine_pattern),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 384, tenth*4), 120, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 384, tenth*6), 120, gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*8), 540, crazy_sine)),
43.3333: CommandGroup(
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*7), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*8), 540, crazy_sine),
        SpawnCommand(mini_saucer, (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
50.0: None
}

level_10_seq = {
    # Wave 1: dense basic wall with minis hidden inside
1.0: CommandGroup(
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*1), 240, sine_pattern),
        SpawnCommand(mini_saucer,  (GAME_WIDTH + 128, tenth*2), 540, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*3), 240, gentle_sine),
        SpawnCommand(mini_saucer,  (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*5), 240, ConstX()),
        SpawnCommand(mini_saucer,  (GAME_WIDTH + 128, tenth*6), 540, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*7), 240, ConstX()),
        SpawnCommand(mini_saucer,  (GAME_WIDTH + 128, tenth*8), 540, crazy_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 128, tenth*9), 240, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*1), 240, gentle_sine),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*3), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 180, sine_pattern),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*7), 240, ConstX()),
        SpawnCommand(basic_saucer, (GAME_WIDTH + 256, tenth*9), 240, gentle_sine)),
    # Wave 2: shooting flood + fast shooters mixed in + minis
13.3333: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*1), 180, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 180, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*3), 180, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 180, sine_pattern),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*5), 180, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 180, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*7), 180, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 180, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*9), 180, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 540, crazy_sine)),
    # Wave 2b: big saucers + fast shooters + mini swarm
20.0: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*2), 120, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 180, crazy_sine),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 256, tenth*4), 120, ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*6), 120, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 180, crazy_sine),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 256, tenth*8), 120, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
    # "Breather" -- still has fast shooters and minis, just fewer big threats
31.6667: CommandGroup(
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 128, tenth*3), 360, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 180, sine_pattern),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 128, tenth*7), 360, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
    # Wave 3: two bosses with fast escort and full mini screen
40.0: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 512, tenth*3), 90, gentle_sine),
        SpawnCommand(boss_1,               (GAME_WIDTH + 512, tenth*7), 90, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 150, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*5), 120, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 150, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
    # Final harassment -- everything at once while bosses are alive
50.0: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*1), 180, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*4), 180, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*7), 180, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 180, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 180, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 180, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 540, crazy_sine)),
70.0: None
}

# ── LEVEL 11 ──────────────────────────────────────────────────────────────────
# Theme: Three-front pressure. Big saucers anchor lanes while fast shooters and
# minis deny safe corridors. First level with three simultaneous bosses.
level_11_seq = {
    # Opening: staggered big saucers across all three vertical lanes
1.0: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*2), 120, gentle_sine),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 256, tenth*5), 120, ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*8), 120, gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
    # Fast shooters flood the gap left by bigs
8.3333: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*1), 210, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 210, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*5), 210, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 210, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*9), 210, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 540, crazy_sine)),
    # Dense shooting wall
16.6667: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*1), 180, sine_pattern),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*2), 180, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*3), 180, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*4), 180, sine_pattern),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*5), 180, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*6), 180, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*7), 180, sine_pattern),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*8), 180, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*9), 180, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 540, crazy_sine)),
    # Breather - but minis keep coming
26.6667: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*3), 150, sine_pattern),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*7), 150, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 180, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
    # Three bosses enter together
36.6667: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*2), 90, gentle_sine),
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*5), 90, ConstX()),
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*8), 90, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*1), 180, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*9), 180, sine_pattern)),
    # Harassment while bosses are alive
46.6667: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*2), 180, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*5), 180, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*8), 180, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*7), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
    # Final push - full mini screen + shooters while bosses remain
60.0: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*2), 210, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 210, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*6), 210, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 210, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 540, crazy_sine)),
80.0: None
}

# ── LEVEL 12 ──────────────────────────────────────────────────────────────────
# Theme: No rest. Short gaps between waves, bosses arrive in two separate pairs,
# fast shooters are now the baseline filler enemy throughout.
level_12_seq = {
    # Dense mixed opening - fast shooters from the start
1.0: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*1), 240, sine_pattern),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 256, tenth*2), 240, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*3), 240, ConstX()),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 256, tenth*4), 240, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*5), 240, gentle_sine),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 256, tenth*6), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*7), 240, sine_pattern),
        SpawnCommand(basic_saucer,         (GAME_WIDTH + 256, tenth*8), 240, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*9), 240, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 540, crazy_sine)),
    # Big saucers as shields for shooters behind them
7.5: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*2), 150, ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*5), 150, gentle_sine),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*8), 150, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*2), 150, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*5), 150, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*8), 150, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
    # First boss pair - escorted by fast shooters immediately
15.0: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*3), 120, sine_pattern),
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*7), 120, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*1), 180, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 180, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*9), 180, gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*8), 540, crazy_sine)),
    # Filler while first bosses are still alive
25.0: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*2), 210, sine_pattern),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*4), 210, ConstX()),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*6), 210, sine_pattern),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 256, tenth*8), 210, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 540, crazy_sine)),
    # Second boss pair arrives before the first pair may be dead
35.0: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*2), 90, gentle_sine),
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*8), 90, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*4), 180, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*6), 180, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*9), 540, crazy_sine)),
    # Full-screen denial
46.6667: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*2), 120, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 210, sine_pattern),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*5), 120, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 210, ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*8), 120, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*9), 210, gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 540, crazy_sine)),
    # Third boss - solo but with maximum escort
58.3333: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 768, tenth*5), 120, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 240, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 240, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*7), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
    # Last gasp while boss still lives
71.6667: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*1), 240, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*3), 240, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*5), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*7), 240, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*9), 240, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 540, crazy_sine)),
90.0: None
}

# ── LEVEL 13 ──────────────────────────────────────────────────────────────────
# Theme: Total war. Four bosses total across the level, back-to-back mini screens,
# fast shooters as the default enemy, and no true gaps anywhere.
level_13_seq = {
    # Wall of fast shooters immediately — no warmup
0.0: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*1), 300, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 300, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*3), 300, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 300, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*5), 300, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 300, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*7), 300, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 300, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*9), 300, gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 540, crazy_sine)),
    # Big saucers + hidden fast shooters behind them
6.6667: CommandGroup(
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*1), 180, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*1), 180, ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*3), 180, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*3), 180, sine_pattern),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*5), 180, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*5), 180, ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*7), 180, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*7), 180, sine_pattern),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 128, tenth*9), 180, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 384, tenth*9), 180, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*8), 540, crazy_sine)),
    # First boss - arrives early, players are still worn down from opening
13.3333: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 768, tenth*5), 120, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 240, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
    # Reinforce before boss might be dead
20.0: CommandGroup(
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*2), 240, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 240, gentle_sine),
        SpawnCommand(shooting_saucer,      (GAME_WIDTH + 128, tenth*6), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 240, gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 540, crazy_sine)),
    # Second boss + escort while first may still be alive
28.3333: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*3), 120, gentle_sine),
        SpawnCommand(boss_1,               (GAME_WIDTH + 640, tenth*7), 120, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*1), 240, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*9), 240, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*8), 540, crazy_sine)),
    # Full mini screen + fast shooters - maximum clutter
38.3333: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*1), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*3), 240, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*5), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*7), 240, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*9), 240, ConstX()),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*7), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*8), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 256, tenth*9), 540, crazy_sine)),
    # Third boss + big saucer formation
50.0: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 768, tenth*5), 150, gentle_sine),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 256, tenth*2), 180, ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 256, tenth*4), 180, sine_pattern),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 256, tenth*6), 180, ConstX()),
        SpawnCommand(big_saucer,           (GAME_WIDTH + 256, tenth*8), 180, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 512, tenth*3), 240, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 512, tenth*7), 240, gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
    # Never-ending harassment while boss 3 is alive
61.6667: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*2), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 240, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*6), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 240, sine_pattern),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 540, crazy_sine)),
    # Fourth and final boss - everything at maximum
75.0: CommandGroup(
        SpawnCommand(boss_1,               (GAME_WIDTH + 768, tenth*3), 150, sine_pattern),
        SpawnCommand(boss_1,               (GAME_WIDTH + 768, tenth*7), 150, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 240, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*5), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 240, gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*7), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 128, tenth*9), 540, crazy_sine)),
90.0: CommandGroup(
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*1), 240, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*2), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*3), 240, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*4), 240, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*5), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*6), 240, gentle_sine),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*7), 240, sine_pattern),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 256, tenth*8), 240, ConstX()),
        SpawnCommand(fast_shooting_saucer, (GAME_WIDTH + 128, tenth*9), 240, gentle_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*1), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*2), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*3), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*4), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*5), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*6), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*7), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*8), 540, crazy_sine),
        SpawnCommand(mini_saucer,          (GAME_WIDTH + 384, tenth*9), 540, crazy_sine)),
100.0: None
}

class GameLevel:
    def __init__(self, program, background):
        self.program = program
        self.background = background
        self.over = False
        self.triggered = {k: False for k in self.program}

    def reset(self):
        self.over = False
        self.triggered = {k: False for k in self.program}

    def update(self, timer):
        for key in self.program:
            if self.triggered[key] == False and timer >= key:
                self.triggered[key] = True
                if self.program[key] is not None:
                    self.program[key].execute()
        
        if timer >= max(self.program.keys()):
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

class GameLevel:
    def __init__(self, program, background):
        self.program = program
        self.background = background
        self.over = False
        self.triggered = {k: False for k in self.program}

    def reset(self):
        self.over = False
        self.triggered = {k: False for k in self.program}

    def update(self, timer):
        for key in self.program:
            if self.triggered[key] == False and timer >= key:
                self.triggered[key] = True
                if self.program[key] is not None:
                    self.program[key].execute()
        
        if timer >= max(self.program.keys()):
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