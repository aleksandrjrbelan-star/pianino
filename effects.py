from settings import WHITE, GREY, BLACK
from pygame import draw

def draw_key_effect(screen, rect, is_pressed=False):
    base_color = GREY if not is_pressed else WHITE

    border_color = BLACK

    draw.rect(screen, base_color, rect,border_radius=8)
    draw.rect(screen, border_color, rect, 2,border_radius=8)
