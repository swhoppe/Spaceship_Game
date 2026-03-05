import numpy as np
import pygame

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