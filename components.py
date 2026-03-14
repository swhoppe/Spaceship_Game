from dataclasses import dataclass
from typing import Any

from assets import *
from entities import *
from physics import *

@dataclass
class ComponentConfig:
    name: str
    icon: Any
    upgrade_costs: list

@dataclass
class EngineConfig(ComponentConfig):
    speed_scheme: list    # engine speed values

@dataclass
class ArmorConfig(ComponentConfig):
    hp_scheme: list    # hp values

@dataclass
class WeaponConfig(ComponentConfig):
    proj_image: Any
    reload_time_scheme: list
    projectile_speed_scheme: list
    damage_scheme: list
    freeze_scheme: list
    recoil_scheme: list
    impact_radius_scheme: list
    impact_magnitude_scheme: list
    detonable: bool

class Component:
    def __init__(self, config):
        self.name = config.name
        self.icon = config.icon
        self.upgrade_costs = config.upgrade_costs
        self.upgrade_level = 0
        self.max_upgrade_level = len(self.upgrade_costs)
        self.specs = {"level": self.upgrade_level}
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
    def __init__(self, config):
        super().__init__(config)
        self.speed_scheme = config.speed_scheme

        assert len(self.upgrade_costs)+1 == len(self.speed_scheme), 'Scheme-list length mismatch.'

        self.update()
        
    def update(self):
        self.speed = self.speed_scheme[self.upgrade_level]
        self.specs = {'level': self.upgrade_level, "speed": self.speed}
    
    def push_upgrade_update(self):
        self.parent.move_speed = self.speed

player_engine_config = EngineConfig(
    name='ENGINE',
    icon=engine_icon_0,
    upgrade_costs=[2000, 2500, 3000, 3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 12000],
    speed_scheme=[360, 480, 600, 720, 840, 960, 1080, 1200, 1320, 1440, 1560, 1680, 1800]
)

player_engine = Engine(player_engine_config)

class Armor(Component):
    def __init__(self, config):
        super().__init__(config)
        self.hp_scheme = config.hp_scheme

        assert len(self.upgrade_costs)+1==len(self.hp_scheme), 'Scheme-list length mismatch.'

        self.update()

    def update(self):
        self.max_hp = self.hp_scheme[self.upgrade_level]
        self.specs = {'level': self.upgrade_level, 'max health': self.max_hp}

    def push_upgrade_update(self):
        self.parent.max_hp = self.max_hp
        self.parent.hp_bar.max_level = self.max_hp

player_armor_config = ArmorConfig(
    name='ARMOR',
    icon=armor_icon_0,
    upgrade_costs=[1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 7000],
    hp_scheme=[200, 300, 400, 500, 700, 900, 1200, 1500, 1900, 2300, 2800, 3500, 4000]
)

player_armor = Armor(player_armor_config)
    
class Weapon(Component):
    def __init__(self, config, move_pattern, impact_sprite):
        super().__init__(config)
        self.proj_img = config.proj_image
        self.reload_time_scheme = config.reload_time_scheme
        self.projectile_speed_scheme = config.projectile_speed_scheme
        self.damage_scheme = config.damage_scheme
        
        self.freeze_scheme = config.freeze_scheme
        self.recoil_scheme = config.recoil_scheme
        self.impact_radius_scheme = config.impact_radius_scheme
        self.impact_magnitude_scheme = config.impact_magnitude_scheme
        self.detonable = config.detonable
        
        self.recoil = None
        self.impact = None

        self.move_pattern = move_pattern

        self.impact_sprite_img = impact_sprite

        self.parent = None

        assert len(self.upgrade_costs)+1 == len(self.reload_time_scheme), 'Scheme-list length mismatch.'
        assert len(self.upgrade_costs)+1 == len(self.projectile_speed_scheme), 'Scheme-list length mismatch.'
        assert len(self.upgrade_costs)+1 == len(self.damage_scheme), 'Scheme-list length mismatch.'
        if self.freeze_scheme:
            assert len(self.upgrade_costs)+1 == len(self.freeze_scheme), 'Scheme-list length mismatch.'
        if self.recoil_scheme:
            assert len(self.upgrade_costs)+1 == len(self.recoil_scheme), 'Scheme-list length mismatch.'
        if self.impact_radius_scheme:
            assert len(self.upgrade_costs)+1 == len(self.impact_radius_scheme), 'Scheme-list length mismatch.'
            assert len(self.upgrade_costs)+1 == len(self.impact_magnitude_scheme), 'Scheme-list length mismatch.'

        self.update()

    def update(self):
        self.reload_time = self.reload_time_scheme[self.upgrade_level]
        self.reload_timer = self.reload_time
        self.proj_move_pattern = self.move_pattern
        self.proj_speed = self.projectile_speed_scheme[self.upgrade_level]
        self.damage = self.damage_scheme[self.upgrade_level]

        if self.freeze_scheme:
            self.freeze = self.freeze_scheme[self.upgrade_level]
        else:
            self.freeze = None
        if self.recoil_scheme:
            self.recoil = Recoil(np.array([-1, 0]), self.recoil_scheme[self.upgrade_level])
        if self.impact_magnitude_scheme:
            self.impact = Impact(self.impact_radius_scheme[self.upgrade_level], 
                                 self.impact_magnitude_scheme[self.upgrade_level])

        self.specs = {'level': self.upgrade_level, 
                      'load time': self.reload_time,
                      'speed': self.projectile_speed_scheme[self.upgrade_level],
                      'damage': self.damage,
                      'freeze time': self.freeze}

    def shoot(self, start_location, parent):
        new_projectile = Projectile(self.proj_img, start_location, self.proj_move_pattern, self.proj_speed, self.damage, self.impact_sprite_img, self.impact, self.detonable, parent)
        new_projectile.freeze = self.freeze
        projectiles.add(new_projectile)
        if self.recoil:
            self.recoil.apply(parent)

    def set_level(self, level):
        self.upgrade_level = level
        self.update()

bolt_laser_config = WeaponConfig(
    name='BOLT LASER',
    icon=sm_laser_icon,
    upgrade_costs=[500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000],
    proj_image=sm_laser_bolt_img,
    reload_time_scheme=[0.5, 0.45, 0.417, 0.367, 0.333, 0.3, 0.25, 0.217, 0.167, 0.133, 0.1, 0.05, 0.017],
    projectile_speed_scheme=[900, 900, 900, 900, 960, 960, 960, 1020, 1020, 1020, 1080, 1080, 1080],
    damage_scheme=[10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 14, 15],
    freeze_scheme=None,
    recoil_scheme=[0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 80, 110, 150],
    impact_radius_scheme=None,
    impact_magnitude_scheme=None,
    detonable=False
)

gum_blaster_config = WeaponConfig(
    name='GUM BLASTER',
    icon=gum_blaster_icon,
    upgrade_costs=[500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000],
    proj_image=gumball_img,
    reload_time_scheme=[1.667, 1.583, 1.5, 1.417, 1.333, 1.25, 1.167, 1.083, 1.0, 0.917, 0.833, 0.75, 0.667],
    projectile_speed_scheme=[300, 300, 300, 300, 360, 360, 360, 420, 420, 420, 480, 480, 480],
    damage_scheme=[15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 20],
    freeze_scheme=[5]*13,
    recoil_scheme=[i*30 for i in range(13)],
    impact_radius_scheme=None,
    impact_magnitude_scheme=None,
    detonable=False
)

lava_blaster_config = WeaponConfig(
    name='LAVA BLASTER',
    icon=lava_blaster_icon,
    upgrade_costs=[500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000],
    proj_image=lava_ball_img,
    reload_time_scheme=[3.333, 3.167, 3.0, 2.833, 2.667, 2.5, 2.333, 2.167, 2.0, 1.833, 1.667, 1.5, 1.333],
    projectile_speed_scheme=[300, 300, 300, 360, 360, 360, 420, 420, 420, 480, 480, 480, 540],
    damage_scheme=[25, 25, 30, 30, 35, 35, 40, 40, 45, 45, 50, 50, 55],
    freeze_scheme=[6]*13,
    recoil_scheme=[i*40 for i in range(13)],
    impact_radius_scheme=None,
    impact_magnitude_scheme=None,
    detonable=False
)

beam_laser_config = WeaponConfig(
    name='BEAM LASER',
    icon=beam_laser_icon,
    upgrade_costs=[500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000],
    proj_image=beam_laser_img,
    reload_time_scheme=[.01667]*13,
    projectile_speed_scheme=[3840]*13,
    damage_scheme=[i*0.3 for i in range(1, 14)],
    freeze_scheme=None,
    recoil_scheme=None,
    impact_radius_scheme=None,
    impact_magnitude_scheme=None,
    detonable=False
)


ice_ray_config = WeaponConfig(
    name='ICE RAY',
    icon=ice_ray_icon,
    upgrade_costs=[500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000],
    proj_image=ice_ray_img,
    reload_time_scheme=[0.01667]*13,
    projectile_speed_scheme=[3840]*13,
    damage_scheme=[i*0.2 for i in range(1, 14)],
    freeze_scheme=[0.02]*13,
    recoil_scheme=None,
    impact_radius_scheme=None,
    impact_magnitude_scheme=None,
    detonable=False
)

mine_launcher_config = WeaponConfig(
    name='MINE LAUNCHER',
    icon=None,
    upgrade_costs=[500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000],
    proj_image=mine_img,
    reload_time_scheme=[5.0, 4.833, 4.667, 4.5, 4.333, 4.167, 4.0, 3.833, 3.667, 3.5, 3.333, 3.167, 3.0],
    projectile_speed_scheme=[0]*13,
    damage_scheme=[35 + i*5 for i in range(13)],
    freeze_scheme=None,
    recoil_scheme=None,
    impact_radius_scheme=[250 + i*12 for i in range(13)],
    impact_magnitude_scheme=[750 + i*75 for i in range(13)],
    detonable=True
)

rockets_config = WeaponConfig(
    name='ROCKETS',
    icon=None,
    upgrade_costs=[1000 + i*500 for i in range(12)],
    proj_image=rocket_img,
    reload_time_scheme=[3.333, 3.167, 3.0, 2.833, 2.667, 2.5, 2.333, 2.167, 2.0, 1.833, 1.667, 1.5, 1.333],
    projectile_speed_scheme=[900]*13,
    damage_scheme=[25 + i*5 for i in range(1, 14)],
    freeze_scheme=None,
    recoil_scheme=None,
    impact_radius_scheme=[250 + i*15 for i in range(13)],
    impact_magnitude_scheme=[500 + i*100 for i in range(13)],
    detonable=True
)

def create_weapon_list():
    """Creates a fresh set of weapons for a player"""
    return np.array([
        Weapon(bolt_laser_config, ConstX(), None),
        Weapon(gum_blaster_config, ConstX(), create_gum_splat),
        Weapon(lava_blaster_config, ConstX(), create_lava_splat),
        Weapon(beam_laser_config, TrackParent(), None),
        Weapon(ice_ray_config, TrackParent(), None),
        Weapon(mine_launcher_config, ConstX(), None),
        Weapon(rockets_config, GuidedMissile(), None)
    ])

enemy_laser_config = WeaponConfig(
    name='BOLT LASER',
    icon=sm_laser_icon,
    upgrade_costs=[500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000],
    proj_image=enemy_laser_bolt_img,
    reload_time_scheme=[1.5 - i*0.1 for i in range(13)],
    projectile_speed_scheme=[-x for x in [900, 900, 900, 900, 960, 960, 960, 1020, 1020, 1020, 1080, 1080, 1080]],
    damage_scheme=[10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 14, 15],
    freeze_scheme=None,
    recoil_scheme=None,
    impact_radius_scheme=None,
    impact_magnitude_scheme=None,
    detonable=False
)

#enemy
enemy_laser_template = Weapon(enemy_laser_config, ConstX(), None)
enemy_fast_laser_template = Weapon(enemy_laser_config, ConstX(), None)
enemy_fast_laser_template.set_level(10)