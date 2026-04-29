import pygame
from models import Trial

def draw_card(surface, trial: Trial, config):
    card_width = config["card_width"]
    card_height = config["card_height"]
    x = (config["screen_width"] - card_width) // 2

    if trial.position == "TOP":
        y = config["top_y"]
    else:
        y = config["bottom_y"]

    card_rect = pygame.Rect(x, y, card_width, card_height)
    pygame.draw.rect(surface, config['card_color'], card_rect)

    font = pygame.font.Font(config['font_name'], config['font_size'])
    text = f"{trial.letter}{trial.number}"
    text_surface = font.render(text, True, config['text_color'])
    text_rect = text_surface.get_rect(center=card_rect.center)

    surface.blit(text_surface, text_rect)
