from assets import *
from utils import *

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