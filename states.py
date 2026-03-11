import pygame
from pygame.locals import *
from functools import partial

#locals
from utils import *
from constants import *
from assets import *
from ui import *
from input import *
from levels import *
from groups import *

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
        
    def update(self, dt):
        pass

    def draw(self, surface):
        pass

class Splash(State):
    def __init__(self):
        super().__init__()
        self.timer = 0
        self.next_state = 'main_menu'
    
    def update(self, dt):
        if self.timer < 1:
            self.timer += dt
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

    def update(self, dt):
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
    
    def update(self, dt):
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
        self.tile_width = None

    def reset(self, *args):
        self.tile_width = GAME_WIDTH / len(self.players) 
        for player in self.players:
            player.tile_surface = pygame.Surface((self.tile_width, GAME_HEIGHT), pygame.SRCALPHA)

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
            player.ready = False
            player.active_submenu = player.submenu_states['default']

            for submenu in player.submenu_states.values():
                if submenu.button_group:
                    submenu.button_group.selected_index = None

    def update(self, dt):
        for player in self.players:
            player.active_submenu.update(dt)
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

        # star motion speed
        self.near_speed = 60 # pixels per second
        self.mid_speed = 30
        self.far_speed = 20
    
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
    
    def update(self, dt):
        self.level_timer += dt

        self.level.update(self.level_timer)
        players['active'].update(self.boundary, dt)
        projectiles.update(self.boundary, dt)
        enemies.update(self.boundary, dt)
        effects.update(dt)
        
        self.star_motion_timer += dt

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

        surface.blit(stars_far_img, (-((self.star_motion_timer * self.far_speed) % 2560), 0))
        surface.blit(stars_mid_img, (-((self.star_motion_timer * self.mid_speed) % 2560), 0))
        surface.blit(stars_near_img, (-((self.star_motion_timer * self.near_speed) % 2560), 0))

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