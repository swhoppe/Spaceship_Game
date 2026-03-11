from assets import *
from entities import *
from physics import *

class Component:
    def __init__(self, upgrade_costs, icon):
        self.upgrade_level = 0
        self.upgrade_costs = upgrade_costs
        self.max_upgrade_level = len(self.upgrade_costs)
        self.name = None
        self.specs = {"level": self.upgrade_level}
        self.icon = icon
        self.parent = None
    
    @property
    def can_upgrade(self):
        return self.upgrade_level < self.max_upgrade_level
    
    @property
    def upgrade_cost(self):
        return self.upgrade_costs[self.upgrade_level]
    
    def push_upgrade_update(self):
        pass
    
    def upgrade(self):
        self.upgrade_level += 1
        self.update()
        self.push_upgrade_update()

    @property
    def stat_block(self):
        stat_block = f"{self.name}:"
        for key, value in self.specs.items():
            stat_block += f"\n{key}: {value}"
        if self.can_upgrade:
            stat_block += f"\nupgrade cost: {self.upgrade_cost:,.0f}"
        else:
            stat_block += f"\nMAXED!"
        return stat_block

class Engine(Component):
    def __init__(self, upgrade_scheme, upgrade_costs, icon):
        super().__init__(upgrade_costs, icon)
        self.upgrade_scheme = upgrade_scheme
        self.name = "ENGINE"
        self.update()

    def update(self):
        self.speed = self.upgrade_scheme[self.upgrade_level]
        self.specs = {'level': self.upgrade_level, "speed": self.speed}
    
    def push_upgrade_update(self):
        self.parent.move_speed = self.speed

engine_upgrade_scheme = [360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440, 1560, 1680, 1800]
engine_upgrade_costs = [2000, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 12000]        

player_engine = Engine(engine_upgrade_scheme, engine_upgrade_costs, engine_icon_0)

class Armor(Component):
    def __init__(self, upgrade_scheme, upgrade_costs, icon):
        super().__init__(upgrade_costs, icon)
        self.upgrade_scheme = upgrade_scheme
        self.name = "ARMOR"
        self.update()

    def update(self):
        self.max_hp = self.upgrade_scheme[self.upgrade_level]
        self.specs = {'level': self.upgrade_level, 'max health': self.max_hp}

    def push_upgrade_update(self):
        self.parent.max_hp = self.max_hp
        self.parent.hp_bar.max_level = self.max_hp

armor_upgrade_scheme = [200, 300, 400, 500, 700, 900, 1200, 1500, 1900, 2300, 2800, 3500, 4000]
armor_upgrade_costs = [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 7000]

player_armor = Armor(armor_upgrade_scheme, armor_upgrade_costs, armor_icon_0)
    
class Weapon(Component):
    def __init__(self, name, image, icon, reload_time_scheme, projectile_speed_scheme, move_pattern, damage_scheme, upgrade_costs, impact_sprite_img, freeze):
        super().__init__(upgrade_costs, icon)
        self.name = name
        self.proj_img = image
        self.reload_time_scheme = reload_time_scheme
        self.projectile_speed_scheme = projectile_speed_scheme
        self.move_pattern = move_pattern
        self.damage_scheme = damage_scheme
        self.impact_sprite_img = impact_sprite_img
        self.freeze = freeze
        self.parent = None
        self.update()

    def update(self):
        self.reload_time = self.reload_time_scheme[self.upgrade_level]
        self.reload_timer = self.reload_time
        self.proj_move_pattern = self.move_pattern
        self.proj_speed = self.projectile_speed_scheme[self.upgrade_level]
        self.damage = self.damage_scheme[self.upgrade_level]
        self.specs = {'level': self.upgrade_level, 
                      'load time': self.reload_time,
                      'speed': self.projectile_speed_scheme[self.upgrade_level],
                      'damage': self.damage,
                      'freeze time': self.freeze}

    def shoot(self, start_location, parent):
        new_projectile = Projectile(self.proj_img, start_location, self.proj_move_pattern, self.proj_speed, self.damage, self.impact_sprite_img, parent)
        new_projectile.freeze = self.freeze
        projectiles.add(new_projectile)

    def set_level(self, level):
        self.upgrade_level = level
        self.update()

# weapons

# weapon upgrade schemes
sm_laser_upgrade_costs = [500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000]
sm_laser_reload_time_scheme = [0.5, 0.45, 0.417, 0.367, 0.333, 0.3, 0.25, 0.217, 0.167, 0.133, 0.1, 0.05, 0.017]
sm_laser_projectile_speed_scheme = [900, 900, 900, 900, 960, 960, 960, 1020, 1020, 1020, 1080, 1080, 1080]
sm_laser_damage_scheme = [10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 14, 15]
sm_laser_enemy_reload_time_scheme = [2.5, 2.333, 2.167, 2.0, 1.833, 1.667, 1.5, 1.333, 1.167, 1.0, 1.0, 1.0, 1.0]

gumball_upgrade_costs = [500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000]
gumball_reload_time_scheme = [1.667, 1.583, 1.5, 1.417, 1.333, 1.25, 1.167, 1.083, 1.0, 0.917, 0.833, 0.75, 0.667]
gumball_projectile_speed_scheme = [300, 300, 300, 300, 360, 360, 360, 420, 420, 420, 480, 480, 480]
gumball_damage_scheme = [15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 20]

lava_ball_upgrade_costs = [500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000]
lava_ball_reload_time_scheme = [3.333, 3.167, 3.0, 2.833, 2.667, 2.5, 2.333, 2.167, 2.0, 1.833, 1.667, 1.5, 1.333]
lava_ball_projectile_speed_scheme = [300, 300, 300, 360, 360, 360, 420, 420, 420, 480, 480, 480, 540]
lava_ball_damage_scheme = [25, 25, 30, 30, 35, 35, 40, 40, 45, 45, 50, 50, 55]

beam_laser_upgrade_costs = [500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000]
beam_laser_reload_time_scheme = [.01667]*13
beam_laser_projectile_speed_scheme = [3840]*13
beam_laser_damage_scheme = [i*0.3 for i in range(1, 14)]

ice_ray_upgrade_costs = [500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000]
ice_ray_reload_time_scheme = [0]*13
ice_ray_projectile_speed_scheme = [3840]*13
ice_ray_damage_scheme = [i*0.2 for i in range(1, 14)]

mine_launcher_upgrade_costs = [500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000]
mine_launcher_reload_time_scheme = [5.0, 4.833, 4.667, 4.5, 4.333, 4.167, 4.0, 3.833, 3.667, 3.5, 3.333, 3.167, 3.0]
mine_launcher_speed_scheme = [0]*13
mine_launcher_damage_scheme = [50 + i*5 for i in range(1, 14)]

rocket_launcher_upgrade_costs = [1000 + i*500 for i in range(12)]
rocket_launcher_reload_time_scheme = [3.333, 3.167, 3.0, 2.833, 2.667, 2.5, 2.333, 2.167, 2.0, 1.833, 1.667, 1.5, 1.333]
rocket_launcher_speed_scheme = [900]*13
rocket_launcher_damage_scheme = [25 + i*5 for i in range(1, 14)]

def create_weapon_list():
    """Creates a fresh set of weapons for a player"""
    return np.array([
        Weapon('BOLT LASER', sm_laser_bolt_img, sm_laser_icon, sm_laser_reload_time_scheme, sm_laser_projectile_speed_scheme, ConstX(), sm_laser_damage_scheme, sm_laser_upgrade_costs, None, None),
        Weapon('GUM BLASTER', gumball_img, gum_blaster_icon, gumball_reload_time_scheme, gumball_projectile_speed_scheme, ConstX(), gumball_damage_scheme, gumball_upgrade_costs, create_gum_splat, 5.0),
        Weapon('LAVA BLASTER', lava_ball_img, lava_blaster_icon, lava_ball_reload_time_scheme, lava_ball_projectile_speed_scheme, ConstX(), lava_ball_damage_scheme, lava_ball_upgrade_costs, create_lava_splat, 5.0),
        Weapon('BEAM LASER', beam_laser_img, beam_laser_icon, beam_laser_reload_time_scheme, beam_laser_projectile_speed_scheme, TrackParent(), beam_laser_damage_scheme, beam_laser_upgrade_costs, None, None),
        Weapon('ICE RAY', ice_ray_img, ice_ray_icon, ice_ray_reload_time_scheme, ice_ray_projectile_speed_scheme, TrackParent(), ice_ray_damage_scheme, ice_ray_upgrade_costs, None, 0.016667),
        Weapon('MINE LAUNCHER', mine_img, None, mine_launcher_reload_time_scheme, mine_launcher_speed_scheme, ConstX(), mine_launcher_damage_scheme, mine_launcher_upgrade_costs, None, None),
        Weapon('ROCKETS', rocket_img, None, rocket_launcher_reload_time_scheme, rocket_launcher_speed_scheme, GuidedMissile(), rocket_launcher_damage_scheme, rocket_launcher_upgrade_costs, None, None)
    ])

#enemy
enemy_laser_template = Weapon('BOLT LASTER', enemy_laser_bolt_img, sm_laser_icon, sm_laser_reload_time_scheme, [-x for x in sm_laser_projectile_speed_scheme], ConstX(), sm_laser_damage_scheme, sm_laser_upgrade_costs, None, None)
enemy_fast_laser_template = Weapon('BOLT LASTER', enemy_laser_bolt_img, sm_laser_icon, sm_laser_enemy_reload_time_scheme, [-x for x in sm_laser_projectile_speed_scheme], ConstX(), sm_laser_damage_scheme, sm_laser_upgrade_costs, None, None)
enemy_fast_laser_template.set_level(10)