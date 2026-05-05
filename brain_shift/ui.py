import pygame
from models import Trial
import config

def draw_card(surface, trial: Trial, config):
    card_width = config.CARD_WIDTH
    card_height = config.CARD_HEIGHT
    x = (config.SCREEN_WIDTH - card_width) // 2

    if trial.position == "TOP":
        y = config.TOP_Y
    else:
        y = config.BOTTOM_Y

    card_rect = pygame.Rect(x, y, card_width, card_height)
    pygame.draw.rect(surface, config.CARD_COLOR, card_rect)

    font = pygame.font.Font(config.FONT_NAME, config.FONT_SIZE)
    text = f"{trial.letter}{trial.number}"
    text_surface = font.render(text, True, config.TEXT_COLOR)
    text_rect = text_surface.get_rect(center=card_rect.center)

    surface.blit(text_surface, text_rect)
