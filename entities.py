import pygame
import numpy as np
from assets import *
from groups import *
from input import joysticks

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
        if self.max_level == 0:
            return
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
        self.crash_damage = start_hp
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
            self.mask = pygame.mask.from_surface(self.rotated_image)
            self.rect = self.rotated_image.get_rect(center=self.rect.center)

        # collision with enemy
        if isinstance(self.parent, Player):
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
    
        if isinstance(self.parent, Enemy):
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

# effect factor functions
def create_gum_splat(location, duration):
    return EffectSprite(gum_splat_img, location, duration)

def create_lava_splat(location, duration):
    return EffectSprite(lava_splat_img, location, duration)