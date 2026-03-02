# libraries
import os, sys, pygame, random, math, copy
from pygame.locals import * # allows use of terms like JOYAXISMOTION w/o leading `pygame.`.
import numpy as np
from functools import partial

# locals
from constants import *
from assets import *
from display import screen
from groups import *

# setup random number generator
rng = np.random.default_rng()

def draw_text(surface, font, text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def draw_multiline_text(surface, font, text, color, x, y):
    lines = text.splitlines()
    y_offset = 0
    for line in lines:
        draw_text(surface, font, line, color, x, y+y_offset)
        y_offset += font.get_linesize()
    return y_offset

# load controllers
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name())

class Button:
    def __init__(self, text, action):
        self.rect = pygame.Rect((0, 0), BUTTON_SIZE)
        self.text = text
        self.action = action
        self.parent = None

    def draw(self, surface, x, y, color):
        self.rect.centerx, self.rect.top = x, y
        pygame.draw.rect(surface, color, self.rect, 3, border_radius=15)
        draw_text(surface, font_md, self.text, (255, 255, 255), self.rect.centerx, self.rect.centery)

class ButtonGroup:
    def __init__(self, buttons):
        self.buttons = buttons
        self.selected_index = None
        self.colors = BUTTON_COLORS
    
    def navigate(self, direction):
        if direction == "up":
            if self.selected_index == None:
                self.selected_index = len(self.buttons) - 1
            else:
                self.selected_index = (self.selected_index - 1) % len(self.buttons)
        if direction == "down":
            if self.selected_index == None:
                self.selected_index = 0
            else:
                self.selected_index = (self.selected_index + 1) % len(self.buttons)

    def execute_selected(self):
        if self.selected_index is not None:
            self.buttons[self.selected_index].action()

    def clear_selection(self):
        self.selected_index = None

    def draw(self, surface, header):
        center_x = surface.get_rect().centerx
        for i, button in enumerate(self.buttons):
            y_pos = header + (i * 55)
            if i == self.selected_index:
                color = self.colors['selected']
            else:
                color = self.colors['deselected']
            button.draw(surface, center_x, y_pos, color)

class StatusBar(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, max_level):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        self.max_level = float(max_level)
        self.level = float(max_level)

class Health(StatusBar):
    def __init__(self, x, y, w, h, max_hp):
        super().__init__(x, y, w, h, max_hp)

    def update(self):
        ratio = self.level / self.max_level
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, "red", (0, 0, self.rect.width, self.rect.height))
        pygame.draw.rect(self.image, "green", (0, 0, self.rect.width * ratio, self.rect.height))

class Player(pygame.sprite.Sprite):
    def __init__(self, groups_dict, name, image, controller_number, engine, armor, weapon_list):
        super().__init__(*groups_dict.values())
        self.groups = groups_dict
        self.name = name
        self.components = []

        #image, mask, and rectangle
        self.image = image
        self.glam_image = None
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()

        self.controller_number = controller_number
        self.motion = np.array([0, 0])
        self.engine = engine
        self.components.append(self.engine)
        self.move_speed = self.engine.speed

        #health
        self.armor = armor
        self.components.append(self.armor)
        self.max_hp = self.armor.max_hp
        self.hp = self.max_hp
        self.hp_bar = Health(self.rect.left, self.rect.bottom - 10, 64, 5, self.hp)

        #weapon
        self.weapon_list = weapon_list
        for weapon in self.weapon_list:
            weapon.parent = self
            self.components.append(weapon)
        self.active_weapon_indices = [0, 1]
        self.active_weapons = self.weapon_list[self.active_weapon_indices]

        #credits
        self.credits = 10000
        self.credits_txt_surf = font_lg.render(f"{self.credits:,.0f}", True, (0, 255, 0))
        self.credits_txt_rect = self.credits_txt_surf.get_rect()

        #assign self as parent for each component
        for component in self.components:
            component.parent = self

    def update_credits_text(self):
        self.credits_txt_surf = font_lg.render(f"{self.credits:,.0f}", True, (0, 255, 0))
        self.credits_txt_rect = self.credits_txt_surf.get_rect()

    def update(self, boundary):
        inflated_boundary = boundary.inflate(0, BOUNDARY_MARGIN)
        self.rect.move_ip(self.motion)

        # clamp movement to bounds    
        self.rect.clamp_ip(inflated_boundary)

        for weapon in self.active_weapons:
            if weapon.reload_timer < weapon.reload_time:
                weapon.reload_timer += 1

        self.hp_bar.level = self.hp
        self.hp_bar.update()
        self.hp_bar.rect.y = self.rect.y
        self.hp_bar.rect.clamp_ip(boundary)
        self.hp_bar.rect.x = self.rect.centerx - self.hp_bar.rect.width/2

        self.update_credits_text()

        if self.hp <= 0:
            self.remove(players['active'])

    def upgrade_component(self, component):
        if component.can_upgrade and self.credits >= component.upgrade_costs[component.upgrade_level]:
            self.credits -= component.upgrade_costs[component.upgrade_level]
            self.update_credits_text()
            component.upgrade()

        else:
            self.rumble(25, 25, 100)

    def change_weapon(self, slot, new_index):
        self.active_weapon_indices[slot] = new_index
        self.active_weapons = self.weapon_list[self.active_weapon_indices]
    
    def draw(self, surface):
        # draw image
        surface.blit(self.image, self.rect)
        # draw hp_bar
        surface.blit(self.hp_bar.image, (self.hp_bar.rect))

    def shoot(self, weapon_index):
        weapon = self.weapon_list[weapon_index]
        if weapon.reload_timer == weapon.reload_time:  
            weapon.shoot(self.rect.center, self)
            weapon.reload_timer = 0

    def reset_for_level(self, position):
        self.hp = self.max_hp
        self.add(self.groups['active'])
        (self.rect.left, self.rect.centery) = position

    def rumble(self, low, high, duration):
        if self.controller_number is not None and self.controller_number < len(joysticks):
                joysticks[self.controller_number].rumble(low, high, duration)

    def go_to_submenu(self, submenu_name):
        new_submenu = self.submenu_states[submenu_name]
        new_submenu.prev_state = self.active_submenu
        self.active_submenu = new_submenu
    
    def go_back_submenu(self):
        self.active_submenu = self.active_submenu.prev_state

class MovePattern:
    def __init__(self):
        self.directed = False

    def init_state(self, obj):
        pass

    def __call__(self, obj):
        NotImplementedError     

class SinePattern(MovePattern):
    def __init__(self, amplitude, rate):
        super().__init__()
        self.amplitude = amplitude
        self.rate = rate

    def __call__(self, obj):
        return np.array([obj.speed, (self.amplitude * math.sin((obj.tof * self.rate / 100)+math.pi/2))])

class ConstX(MovePattern):
    def __init__(self):
        super().__init__()

    def __call__(self, obj):
        return np.array([obj.speed, 0])
    
class TrackParent(MovePattern):
    def __init__(self):
        super().__init__()

    def init_state(self, obj):
        obj.last_y_pos = obj.parent.rect.y
    
    def __call__(self, obj):
        delta_y = obj.parent.rect.y - obj.last_y_pos
        obj.last_y_pos = obj.parent.rect.y
        return np.array([obj.speed, delta_y])
    
class GuidedMissile(MovePattern):
    def __init__(self):
        super().__init__()
        self.directed = True

    def __call__(self, obj):
        if enemies:
            vectors = np.empty((len(enemies), 2))
            for i, enemy in enumerate(enemies):
                vectors[i] = np.array(enemy.rect.center) - np.array(obj.rect.center)
            norms = np.linalg.norm(vectors, axis=1)
            min_index = np.argmin(norms)
            target_vector = vectors[min_index]
            target_norm = np.linalg.norm(target_vector) + 0.00001 # to avoid div by 0
            normed_target = target_vector / target_norm
            return normed_target * obj.speed
        else:
            return np.array([obj.speed, 0])
    
sine_pattern = SinePattern(5, 2)
gentle_sine = SinePattern(2, 2)
crazy_sine = SinePattern(8, 3)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, name, image, start_hp, start_position, speed, move_pattern, weapon):
        super().__init__(group)
        self.name = name
        self.image = image
        self.rect = image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.start_position = start_position
        self.x = float(self.start_position[0])
        self.rect.center = self.start_position
        self.move_pattern = move_pattern
        self.speed = - speed
        self.velocity = np.array([self.speed, 0])
        self.freeze_timer = 0
        self.kill_bonus = start_hp / 4
        self.hp = start_hp
        self.hp_bar = Health(self.rect.left, self.rect.bottom - 10, 64, 5, self.hp)
        self.crash_damage = start_hp * 0.5
        self.weapon = weapon
        self.tof = 0 # time of flight

    def freeze(self, time):
        self.freeze_timer = time
    
    def update(self, boundary):
        self.velocity = self.move_pattern(self)

        if self.freeze_timer != 0:
            self.freeze_timer -= 1
        else:
            self.tof += 1
            self.rect.move_ip(int(self.velocity[0]), int(self.velocity[1]))
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > GAME_HEIGHT:
            self.rect.bottom = GAME_HEIGHT

        if self.hp <=0:
            self.kill()
        if self.rect.x < 0 - self.rect.width:
            self.kill()
        
        for player in players['active']:
            if player.mask.overlap(self.mask, (self.rect[0] - player.rect[0], self.rect[1] - player.rect[1])):
                player.hp -= self.crash_damage
                player.rumble(0.7, 0.8, 100)
                player.credits += self.kill_bonus
                self.kill()
        
        self.hp_bar.level = self.hp
        self.hp_bar.update()
        self.hp_bar.rect.y = self.rect.y
        self.hp_bar.rect.clamp_ip(boundary)
        self.hp_bar.rect.x = self.rect.centerx - self.hp_bar.rect.width/2

        if self.weapon:
            if self.weapon.reload_timer < self.weapon.reload_time:
                self.weapon.reload_timer += 1
            else:
                self.shoot()
    
    def shoot(self):
        self.weapon.shoot(self.rect.center, self)
        self.weapon.reload_timer = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.hp_bar.image, (self.hp_bar.rect))

class Projectile(pygame.sprite.Sprite):
    def __init__(self, image, start_location, move_pattern, speed, damage, impact_sprite_img, parent):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.start_location = start_location
        self.rect.center = start_location
        self.x = float(start_location[0])
        self.y = float(start_location[1])
        self.move_pattern = move_pattern
        self.speed = speed
        self.damage = damage
        self.parent = parent
        self.freeze = None
        self.impact_sprite = impact_sprite_img
        self.move_pattern.init_state(self)
    
    def impact(self):
        if self.impact_sprite != None:
            effects.add(self.impact_sprite(self.rect.center, self.freeze))

    def update(self, boundary):
        # motion
        self.velocity = self.move_pattern(self)
        self.rect.move_ip(self.velocity[0], self.velocity[1])

        # image rotation
        if self.move_pattern.directed:
            x, y = self.velocity
            angle = np.arctan2(-y, x) * 180 / np.pi
            self.rotated_image = pygame.transform.rotate(self.image, angle)
            self.rect = self.rotated_image.get_rect(center=self.rect.center)

        # collision with enemy
        if self.parent in players["all"]:
            for enemy in enemies:        
                if enemy.mask.overlap(self.mask, (self.rect[0] - enemy.rect[0], self.rect[1] - enemy.rect[1])):
                    enemy.hp -= self.damage
                    self.parent.credits += self.damage
                    if enemy.hp <= 0:
                        self.parent.credits += enemy.kill_bonus
                    if self.freeze != None:
                        enemy.freeze_timer = self.freeze
                    self.impact()
                    self.kill()
    
        if self.parent in enemies:
            for player in players['active']:
                if player.mask.overlap(self.mask, (self.rect[0] - player.rect[0], self.rect[1] - player.rect[1])):
                    player.hp -= self.damage
                    player.rumble(0.2, 0.4, 40)
                    self.impact()
                    self.kill()

        # kill once off screen
        if not boundary.colliderect(self.rect):
            self.kill()

    def draw(self, surface):
        if self.move_pattern.directed:
            surface.blit(self.rotated_image, self.rect)
        else:
            surface.blit(self.image, self.rect)

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

engine_upgrade_scheme = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
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

armor_upgrade_scheme = [200, 300, 400, 500, 700, 900, 1200, 1500, 1900, 2300, 2800, 3500]
armor_upgrade_costs = [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 7000, 8000]

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

class EffectSprite(pygame.sprite.Sprite):
    def __init__(self, image, start_location, duration):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = start_location
        self.start_location = start_location
        self.duration = duration
        effects.add(self)
    
    def update(self):
        self.duration -= 1
        if self.duration <= 0: self.kill()

def create_gum_splat(location, duration):
    return EffectSprite(gum_splat_img, location, duration)

def create_lava_splat(location, duration):
    return EffectSprite(lava_splat_img, location, duration)

# effect images
gum_splat_img = pygame.transform.scale(pygame.image.load("images/gum_splat.png").convert_alpha(), (64, 64))
lava_splat_img = pygame.transform.scale(pygame.image.load("images/lava_splat.png").convert_alpha(), (128, 128))

# weapons

# weapon upgrade schemes
sm_laser_upgrade_costs = [500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000]
sm_laser_reload_time_scheme = [int(30 - x * 2.4) for x in range(13)]
sm_laser_projectile_speed_scheme = [15, 15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18]
sm_laser_damage_scheme = [10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 14, 15]
sm_laser_enemy_reload_time_scheme = [150 - i*10 for i in range(13)]

gumball_upgrade_costs = [500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000]
gumball_reload_time_scheme = [100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40]
gumball_projectile_speed_scheme = [5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8]
gumball_damage_scheme = [15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 20]

lava_ball_upgrade_costs = [500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000]
lava_ball_reload_time_scheme = [200, 190, 180, 170, 160, 150, 140, 130, 120, 110, 100, 90, 80]
lava_ball_projectile_speed_scheme = [5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9]
lava_ball_damage_scheme = [25, 25, 30, 30, 35, 35, 40, 40, 45, 45, 50, 50, 55]

beam_laser_upgrade_costs = [500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000]
beam_laser_reload_time_scheme = [1]*13
beam_laser_projectile_speed_scheme = [64]*13
beam_laser_damage_scheme = [i*0.3 for i in range(1, 14)]

ice_ray_upgrade_costs = [500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000]
ice_ray_reload_time_scheme = [0]*13
ice_ray_projectile_speed_scheme = [64]*13
ice_ray_damage_scheme = [i*0.2 for i in range(1, 14)]

mine_launcher_upgrade_costs = [500, 500, 750, 750, 1000, 1000, 1250, 1250, 1500, 1500, 2000, 3000]
mine_launcher_reload_time_scheme = [300 - i*10 for i in range(13)]
mine_launcher_speed_scheme = [0]*13
mine_launcher_damage_scheme = [50 + i*5 for i in range(1, 14)]

rocket_launcher_upgrade_costs = [1000 + i*500 for i in range(12)]
rocket_launcher_reload_time_scheme = [200 - i*10 for i in range(13)]
rocket_launcher_speed_scheme = [15]*13
rocket_launcher_damage_scheme = [25 + i*5 for i in range(1, 14)]

def create_weapon_list():
    """Creates a fresh set of weapons for a player"""
    return np.array([
        Weapon('BOLT LASER', sm_laser_bolt_img, sm_laser_icon, sm_laser_reload_time_scheme, sm_laser_projectile_speed_scheme, ConstX(), sm_laser_damage_scheme, sm_laser_upgrade_costs, None, None),
        Weapon('GUM BLASTER', gumball_img, gum_blaster_icon, gumball_reload_time_scheme, gumball_projectile_speed_scheme, ConstX(), gumball_damage_scheme, gumball_upgrade_costs, create_gum_splat, 300),
        Weapon('LAVA BLASTER', lava_ball_img, lava_blaster_icon, lava_ball_reload_time_scheme, lava_ball_projectile_speed_scheme, ConstX(), lava_ball_damage_scheme, lava_ball_upgrade_costs, create_lava_splat, 300),
        Weapon('BEAM LASER', beam_laser_img, beam_laser_icon, beam_laser_reload_time_scheme, beam_laser_projectile_speed_scheme, TrackParent(), beam_laser_damage_scheme, beam_laser_upgrade_costs, None, None),
        Weapon('ICE RAY', ice_ray_img, ice_ray_icon, ice_ray_reload_time_scheme, ice_ray_projectile_speed_scheme, TrackParent(), ice_ray_damage_scheme, ice_ray_upgrade_costs, None, 1),
        Weapon('MINE LAUNCHER', mine_img, None, mine_launcher_reload_time_scheme, mine_launcher_speed_scheme, ConstX(), mine_launcher_damage_scheme, mine_launcher_upgrade_costs, None, None),
        Weapon('ROCKETS', rocket_img, None, rocket_launcher_reload_time_scheme, rocket_launcher_speed_scheme, GuidedMissile(), rocket_launcher_damage_scheme, rocket_launcher_upgrade_costs, None, None)
    ])

#enemy
enemy_laser_template = Weapon('BOLT LASTER', enemy_laser_bolt_img, sm_laser_icon, sm_laser_reload_time_scheme, [-x for x in sm_laser_projectile_speed_scheme], ConstX(), sm_laser_damage_scheme, sm_laser_upgrade_costs, None, None)
enemy_fast_laser_template = Weapon('BOLT LASTER', enemy_laser_bolt_img, sm_laser_icon, sm_laser_enemy_reload_time_scheme, [-x for x in sm_laser_projectile_speed_scheme], ConstX(), sm_laser_damage_scheme, sm_laser_upgrade_costs, None, None)
enemy_fast_laser_template.set_level(10)

# instance players
# player_1 = Player(players, 'player_1', noeys_ship_img, None, copy.copy(player_engine), copy.copy(player_armor), create_weapon_list())
# player_1.glam_image = noeys_ship_glam_img
player_2 = Player(players, 'player_2', gabes_ship_img, None, copy.copy(player_engine), copy.copy(player_armor), create_weapon_list())
player_2.glam_image = gabes_ship_glam_img
# player_3 = Player(players, 'player_3', anikas_ship_img, None, copy.copy(player_engine), copy.copy(player_armor), create_weapon_list())
# player_3.glam_image = anikas_ship_glam_img
# player_4 = Player(players, 'player_4', aletheas_ship_img, None, copy.copy(player_engine), copy.copy(player_armor), create_weapon_list())
# player_4.glam_image = aletheas_ship_glam_img
# player_5 = Player(players, 'player_4', basic_ship_img, None, copy.copy(player_engine), copy.copy(player_armor), create_weapon_list())

# assign controllers
for i, player in enumerate(players['all']):
    player.controller_number = i 

class EnemyGenerator:
    def __init__(self, image, hp, weapon):
        self.image = image
        self.hp = hp
        self.weapon = weapon
    
    def generate(self, position, speed, move_pattern):
        return Enemy(enemies,
            f"enemy_{len(enemies)}+1", 
            self.image, 
            self.hp, 
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

basic_saucer = EnemyGenerator(saucer_1_img, 100 * len(players['all'])/2, None)
mini_saucer = EnemyGenerator(saucer_1_mini_img, 50 * len(players['all'])/2, None)
big_saucer = EnemyGenerator(saucer_1_big_img, 2000 * len(players['all'])/2, None)
shooting_saucer = EnemyGenerator(saucer_2_img, 100 * len(players['all'])/2, copy.copy(enemy_laser_template))
fast_shooting_saucer = EnemyGenerator(saucer_2_img, 100 * len(players['all'])/2, copy.copy(enemy_fast_laser_template))
boss_1 = EnemyGenerator(saucer_2_boss_img, 10000 * len(players['all'])/2, copy.copy(enemy_laser_template))

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

# level play programs:
# random:
# def random_enemies(enemy_list, spawn_delay, timer):
#     enemy_selector = (timer // spawn_delay) % len(enemy_list)
#     if timer % spawn_delay == 0:
#         enemy_list[enemy_selector].generate((GAME_WIDTH + 128, rng.uniform(64, GAME_HEIGHT-64, 1)[0]), rng.uniform(3, 6.0, 1)[0])

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
]

class State:
    def __init__(self):
        self.over = False
        self.quit = False
        self.prev_state = None
        self.next_state = None
    
    def reset(self, *args):
        pass

    def handle_input(self, events):
        pass
        
    def update(self):
        pass

    def draw(self, surface):
        pass

class Splash(State):
    def __init__(self):
        super().__init__()
        self.timer = 0
        self.next_state = 'main_menu'
    
    def update(self):
        if self.timer < 60:
            self.timer += 1
        else:
            self.over = True

    def draw(self, surface):
        draw_text(surface, font_lg, 'spaceship game', (255, 255, 255), GAME_WIDTH//2, GAME_HEIGHT//2)

vertical_input = {(0, -1): "down", (0, 1): "up"}
horizontal_input = {(-1, 0): "left", (1, 0): "right"}

class Menu(State):
    def __init__(self, input_dict):
        super().__init__()
        self.input_dict = input_dict
        self.icon = None
        self.top_margin = 100

class MainMenu(Menu):
    def __init__(self, input_dict):
        super().__init__(input_dict)
        self.button_group = ButtonGroup([
        Button('start', lambda: self.go_to('game_play')),
        Button('upgrades', lambda: self.go_to('upgrade_menu')),
        Button('exit', self.quit_game)]
    )

    def handle_input(self, events):
        for event in events:
            if event.type == JOYHATMOTION and event.joy == 0:
                hat_motion = joysticks[0].get_hat(0)
                if hat_motion in self.input_dict:
                    direction = self.input_dict[hat_motion]
                    self.button_group.navigate(direction)
                
            if event.type == JOYBUTTONDOWN and event.joy == 0 and event.button == 0:
                self.button_group.execute_selected()

    def draw (self, surface):
        surface.fill('black')
        self.button_group.draw(surface, self.top_margin)

    def go_to(self, next_state):
        self.next_state = next_state
        self.over = True

    def quit_game(self):
        self.quit = True 

class SubMenu(Menu):
    def __init__(self, input_dict, button_group, player, component):
        super().__init__(input_dict)
        self.button_group = button_group
        self.player = player
        self.component = component
        if self.component and self.component.icon:
            self.icon = self.component.icon
        else:
            self.icon = player.image
        for button in self.button_group.buttons:
            button.parent = self
            if button.action == 'upgrade_weapon':
                button.action = self.upgrade_current

    def change_component(self, new_component):
        self.component = new_component
        if self.component.icon:
            self.icon = self.component.icon
        else:
            self.icon = None

    def update(self):
        if self.player.submenu_states_rev[self.player.active_submenu] == 'ready':
            self.player.ready = True
        else:
            self.player.ready = False

    def handle_input(self, event):
        if self.player.controller_number < len(joysticks):
            hat_motion = joysticks[self.player.controller_number].get_hat(0)
            if hat_motion in self.input_dict:
                direction = self.input_dict[hat_motion]
                self.button_group.navigate(direction)
            
        if event.type == JOYBUTTONDOWN and event.joy == self.player.controller_number and event.button == 0:
            self.button_group.execute_selected()
    
    def draw(self, surface):
        surface_rect = surface.get_rect()
        center_line = surface_rect.centerx
        surface.fill('black')
        header = 0

        if self.icon:
            icon_rect = self.icon.get_rect()
            icon_rect.centerx = center_line
            surface.blit(self.icon, icon_rect)
            header = max(icon_rect.height, self.top_margin)

        self.player.credits_txt_rect.centerx = center_line
        self.player.credits_txt_rect.top = header
        surface.blit(self.player.credits_txt_surf, self.player.credits_txt_rect)
        header += font_lg.get_linesize() + 20

        if self.component:
            header += draw_multiline_text(surface, font_md, self.component.stat_block, 'white', center_line, header)
        
        safe_header = min(header, surface_rect.height - 150)
        self.button_group.draw(surface, safe_header)

        if self.player.ready:
            banner = pygame.Surface((surface_rect.width, 50), pygame.SRCALPHA)
            banner.fill((0, 0, 0, 150))
            surface.blit(banner, (0, surface_rect.height//2 - 25))
            draw_text(surface, font_lg, "READY!", (255, 255, 255), center_line, surface_rect.height//2)

        border = surface.get_rect().inflate(-5, -5)
        pygame.draw.rect(surface, (50, 50, 50), border, 3, 15)

    def upgrade_current(self):
        if self.component:
            self.player.upgrade_component(self.component)

class SelectionMenu(Menu):
    def __init__(self, input_dict, player, option_list, current_selection, slot):
        super().__init__(input_dict)
        self.player = player
        self.option_list = option_list
        self.selected_index = current_selection
        self.component = self.option_list[self.selected_index]
        self.slot = slot
        self.button_group = None
    
    def update(self):
        self.component = self.option_list[self.selected_index]

    def handle_input(self, event):
        if self.player.controller_number < len(joysticks):
            hat_motion = joysticks[self.player.controller_number].get_hat(0)
            if hat_motion in self.input_dict:
                direction = sum(hat_motion)
                self.selected_index = (self.selected_index + direction) % len(self.option_list)
                self.component = self.option_list[self.selected_index]

        if event.type == JOYBUTTONDOWN and event.joy == self.player.controller_number and event.button == 0:
            self.confirm_selection()
            self.player.go_back_submenu()

    def draw(self, surface):
        surface_rect = surface.get_rect()
        center_line = surface_rect.centerx
        surface.fill('black')
        header = 0

        if self.component.icon:
            self.icon = self.component.icon
            self.icon_rect = self.icon.get_rect()
            self.icon_rect.centerx = center_line
            surface.blit(self.icon, self.icon_rect)
            header = max(self.icon_rect.height, self.top_margin)

        if self.component:
            header += draw_multiline_text(surface, font_md, self.component.stat_block, 'white', center_line, header)

        border = surface.get_rect().inflate(-5, -5)
        pygame.draw.rect(surface, (50, 50, 50), border, 3, 15)

    def confirm_selection(self):
        self.component = self.option_list[self.selected_index]
        self.prev_state.change_component(self.option_list[self.selected_index])
        self.player.change_weapon(self.slot, self.selected_index)

class UpgradeMenu(Menu):
    def __init__(self, input_dict, player_list):
        super().__init__(input_dict)
        self.next_state = 'game_play'
        self.players = player_list
        self.tile_width = GAME_WIDTH / len(self.players) 

        for player in self.players:
            player.tile_surface = pygame.Surface((self.tile_width, GAME_HEIGHT), pygame.SRCALPHA)
            player.ready = False
            
            default_submenu = SubMenu(vertical_input, ButtonGroup([
                Button('engine', partial(player.go_to_submenu, 'engine')),
                Button('armor', partial(player.go_to_submenu, 'armor')),
                Button('weapon 1', partial(player.go_to_submenu, 'primary_weapon')),
                Button('weapon 2', partial(player.go_to_submenu, 'secondary_weapon')),
                Button('ready!', partial(player.go_to_submenu, 'ready'))
                ]), player, None)
            
            default_submenu.icon = player.image
            
            engine_submenu = SubMenu(vertical_input, ButtonGroup([
                Button('upgrade', partial(player.upgrade_component, player.engine)),
                Button('done', partial(player.go_to_submenu, 'default'))
                ]), player, player.engine)
            
            armor_submenu = SubMenu(vertical_input, ButtonGroup([
                Button('upgrade', partial(player.upgrade_component, player.armor)),
                Button('done', partial(player.go_to_submenu, 'default'))
                ]), player, player.armor)
            
            primary_weapon_submenu = SubMenu(vertical_input, ButtonGroup([
                Button('change', partial(player.go_to_submenu, 'primary_select')),
                Button('upgrade', 'upgrade_weapon'),
                Button('done', partial(player.go_to_submenu, 'default'))
                ]), player, player.active_weapons[0])
            
            secondary_weapon_submenu = SubMenu(vertical_input, ButtonGroup([
                Button('change', partial(player.go_to_submenu, 'secondary_select')),
                Button('upgrade', 'upgrade_weapon'),
                Button('done', partial(player.go_to_submenu, 'default'))
                ]), player, player.active_weapons[1])
            
            primary_weapon_select = SelectionMenu(horizontal_input, player, player.weapon_list, player.active_weapon_indices[0], slot=0)

            secondary_weapon_select = SelectionMenu(horizontal_input, player, player.weapon_list, player.active_weapon_indices[1], slot=1)
            
            ready_submenu = SubMenu(vertical_input, ButtonGroup([
                Button('back', partial(player.go_to_submenu, 'default'))
                ]), player, None)
            
            ready_submenu.icon = player.glam_image
            
            player.submenu_states = {
                'default': default_submenu,
                'engine': engine_submenu,
                'armor': armor_submenu,
                'primary_weapon': primary_weapon_submenu,
                'secondary_weapon': secondary_weapon_submenu,
                'primary_select': primary_weapon_select,
                'secondary_select': secondary_weapon_select,
                'ready': ready_submenu
            }

            player.submenu_states_rev = {v: k for k, v in player.submenu_states.items()}

            player.active_submenu = player.submenu_states['default']

    def reset(self, *args):
        for player in self.players:
            player.active_submenu = player.submenu_states['default']
            for submenu in player.submenu_states.values():
                if submenu.button_group:
                    submenu.button_group.selected_index = None

    def update(self):
        for player in self.players:
            player.active_submenu.update()
        if all(player.ready for player in self.players):
            self.over = True
        
    def handle_input(self, events):
        for event in events:
            for player in players["all"]:
                if player.controller_number < len(joysticks):
                    if event.type in (JOYHATMOTION, JOYBUTTONDOWN):
                        if event.joy == player.controller_number:
                            player.active_submenu.handle_input(event)

    def draw(self, surface):
        for i, player in enumerate(players["all"]):
            
            player.active_submenu.draw(player.tile_surface)
            surface.blit(player.tile_surface, (i*self.tile_width, 0))

class GamePlay(State):
    def __init__(self):
        super().__init__()
        self.next_state = 'upgrade_menu'
        self.level = None
        self.level_timer = None
        self.star_motion_timer = 0
    
    def reset(self, boundary):
        self.level = game_levels.pop(0)
        self.level_timer = 0
        self.boundary = boundary
        
        for i, player in enumerate(players['all']): 
            position = (0, (GAME_HEIGHT / (len(players['all'])+1) * (i+1)))
            player.reset_for_level(position)

    def clear(self):
        enemies.empty()
        projectiles.empty()
        effects.empty()

    def handle_input(self, events):

        for player in players['active']:
            if player.controller_number < len(joysticks):
                joystick = joysticks[player.controller_number]
                
                axis_x = joystick.get_axis(0)
                axis_y = joystick.get_axis(1)
                
                if abs(axis_x) < MOVE_DEADZONE:
                    axis_x = 0
                if abs(axis_y) < MOVE_DEADZONE:
                    axis_y = 0
                
                player.motion = (axis_x * player.move_speed, axis_y * player.move_speed)

                if joystick.get_axis(5) > SHOOT_DEADZONE:
                    player.shoot(player.active_weapon_indices[0])
                if joystick.get_axis(4) > SHOOT_DEADZONE:
                    player.shoot(player.active_weapon_indices[1])
    
    def update(self):
        self.level.update(self.level_timer)
        players['active'].update(self.boundary)
        projectiles.update(self.boundary)
        enemies.update(self.boundary)
        effects.update()
        self.level_timer += 1

        if not players['active']:
            game_levels.insert(0, self.level)
            self.clear()
            self.over = True

        if self.level.over:
            if not enemies:
                self.clear()
                self.over = True
    
    def draw(self, surface):
        surface.blit(self.level.background, (0, 0))

        if self.star_motion_timer > 3 * GAME_WIDTH * 3:
            self.star_motion_timer = 0

        self.star_motion_timer +=1

        surface.blit(stars_far_img, (-(self.star_motion_timer % (GAME_WIDTH*3))/3, 0))
        surface.blit(stars_mid_img, (-(self.star_motion_timer % (GAME_WIDTH*2))/2, 0))
        surface.blit(stars_near_img, (-(self.star_motion_timer % GAME_WIDTH), 0))

        for projectile in projectiles:
            projectile.draw(surface) 

        for player in players['active']:
            player.draw(surface)

        for enemy in enemies:
            enemy.draw(surface)

        effects.draw(surface)

        for i, player in enumerate(players['all']):
            player.credits_txt_rect.topleft = (i * GAME_WIDTH / len(players['all']) + 75, 12)
            surface.blit(player.credits_txt_surf, player.credits_txt_rect)
            surface.blit(pygame.transform.scale(player.image, (64, 64)), (i * GAME_WIDTH / len(players['all']), 0))

states = {
    "splash": Splash(),
    "main_menu": MainMenu(vertical_input),
    "upgrade_menu": UpgradeMenu(vertical_input, players['all']),
    "game_play": GamePlay()
}

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

    def change_state(self, new_state):
        self.state.over = False # reset state for future use
        self.state = self.states[new_state]
        self.state.reset(self.boundary)

    def quit(self):
        self.running = False

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.state.handle_input(events)
            self.state.update()
            self.state.draw(self.surface)
            self.scaled_surface = pygame.transform.scale(self.surface, screen.get_size())
            self.screen.blit(self.scaled_surface, (0, 0))

            if self.state.over:
                self.change_state(self.state.next_state)
            if self.state.quit:
                self.running = False

            pygame.display.update()

            self.clock.tick(60) #set FPS

        pygame.quit()

game = Game(screen, states, 'splash')

current_level = game_levels[0]

game.run()