import pygame
from models import Trial
import config


def get_card_rect(trial: Trial, config):
    card_width = config.CARD_WIDTH
    card_height = config.CARD_HEIGHT
    x = (config.SCREEN_WIDTH - card_width) // 2

    if trial.position == "TOP":
        y = config.TOP_Y
    else:
        y = config.BOTTOM_Y

    return pygame.Rect(x, y, card_width, card_height)


def draw_card(surface, trial: Trial, config, card_color=None):
    card_rect = get_card_rect(trial, config)
    color = card_color or config.CARD_COLOR

    pygame.draw.rect(surface, color, card_rect)

    font = pygame.font.Font(config.FONT_NAME, config.FONT_SIZE)
    text = f"{trial.letter}{trial.number}"
    text_surface = font.render(text, True, config.TEXT_COLOR)
    text_rect = text_surface.get_rect(center=card_rect.center)

    surface.blit(text_surface, text_rect)


def draw_feedback_icon(surface, trial: Trial, is_correct, config):
    card_rect = get_card_rect(trial, config)
    center_x = card_rect.right + 55
    center_y = card_rect.centery

    if is_correct:
        color = config.CORRECT_COLOR
        points = [
            (center_x - 22, center_y),
            (center_x - 8, center_y + 18),
            (center_x + 25, center_y - 24),
        ]
        pygame.draw.lines(surface, color, False, points, 8)
    else:
        color = config.WRONG_COLOR
        pygame.draw.line(
            surface,
            color,
            (center_x - 22, center_y - 22),
            (center_x + 22, center_y + 22),
            8,
        )
        pygame.draw.line(
            surface,
            color,
            (center_x + 22, center_y - 22),
            (center_x - 22, center_y + 22),
            8,
        )


def draw_timer(surface, remaining_time, config):
    font = pygame.font.Font(config.FONT_NAME, 36)

    text_surface = font.render(f"Tempo: {remaining_time}", True, config.TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, 35))

    surface.blit(text_surface, text_rect)


def draw_results(surface, score, correct_answers, wrong_answers, config):
    font_big = pygame.font.Font(config.FONT_NAME, 48)
    font = pygame.font.Font(config.FONT_NAME, 32)

    total_answers = correct_answers + wrong_answers
    if total_answers > 0:
        accuracy = correct_answers / total_answers * 100
    else:
        accuracy = 0

    lines = [
        ("Risultati", font_big),
        (f"Punteggio: {score}", font),
        (f"Corrette: {correct_answers}", font),
        (f"Sbagliate: {wrong_answers}", font),
        (f"Accuratezza: {accuracy:.1f}%", font),
        ("Premi R per rigiocare", font),
    ]

    y = 120
    for text, current_font in lines:
        text_surface = current_font.render(text, True, config.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, y))
        surface.blit(text_surface, text_rect)
        y += 60
