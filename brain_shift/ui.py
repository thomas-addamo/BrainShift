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


def draw_arrow(surface, start, end, color):
    pygame.draw.line(surface, color, start, end, 4)
    if end[0] > start[0]:
        arrow_points = [(end[0], end[1]), (end[0] - 12, end[1] - 8), (end[0] - 12, end[1] + 8)]
    else:
        arrow_points = [(end[0], end[1]), (end[0] + 12, end[1] - 8), (end[0] + 12, end[1] + 8)]
    pygame.draw.polygon(surface, color, arrow_points)


def draw_trial_prompt(surface, trial: Trial, config):
    card_rect = get_card_rect(trial, config)
    font = pygame.font.Font(config.FONT_NAME, 24)
    color = config.MUTED_TEXT_COLOR

    if trial.position == "TOP":
        draw_arrow(
            surface,
            (card_rect.right + 18, card_rect.centery),
            (card_rect.right + 68, card_rect.centery),
            color,
        )
        text_surface = font.render("Il numero è pari?", True, color)
        text_rect = text_surface.get_rect(midleft=(card_rect.right + 82, card_rect.centery))
    else:
        draw_arrow(
            surface,
            (card_rect.left - 18, card_rect.centery),
            (card_rect.left - 68, card_rect.centery),
            color,
        )
        text_surface = font.render("La lettera è vocale?", True, color)
        text_rect = text_surface.get_rect(midright=(card_rect.left - 82, card_rect.centery))

    surface.blit(text_surface, text_rect)


def draw_feedback_icon(surface, is_correct, config):
    center_x = config.SCREEN_WIDTH // 2
    center_y = (config.TOP_Y + config.CARD_HEIGHT + config.BOTTOM_Y) // 2

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


def get_answer_button_rects(config):
    bar_y = config.SCREEN_HEIGHT - 86
    button_width = 150
    button_height = 46
    gap = 28
    total_width = button_width * 2 + gap
    start_x = (config.SCREEN_WIDTH - total_width) // 2
    y = bar_y + 34

    yes_rect = pygame.Rect(start_x, y, button_width, button_height)
    no_rect = pygame.Rect(start_x + button_width + gap, y, button_width, button_height)
    return yes_rect, no_rect


def draw_answer_buttons(surface, config):
    bar_rect = pygame.Rect(0, config.SCREEN_HEIGHT - 86, config.SCREEN_WIDTH, 86)
    pygame.draw.rect(surface, config.BAR_COLOR, bar_rect)

    font = pygame.font.Font(config.FONT_NAME, 28)
    hint_font = pygame.font.Font(config.FONT_NAME, 18)
    yes_rect, no_rect = get_answer_button_rects(config)

    hint_surface = hint_font.render(
        "Clicca SI/NO oppure usa le frecce: sinistra = SI, destra = NO",
        True,
        config.MUTED_TEXT_COLOR,
    )
    hint_rect = hint_surface.get_rect(center=(config.SCREEN_WIDTH // 2, bar_rect.top + 16))
    surface.blit(hint_surface, hint_rect)

    for label, rect in [("SI", yes_rect), ("NO", no_rect)]:
        pygame.draw.rect(surface, config.BUTTON_COLOR, rect)
        pygame.draw.rect(surface, config.BUTTON_BORDER_COLOR, rect, 2)
        text_surface = font.render(label, True, config.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)


def get_answer_from_click(position, config):
    yes_rect, no_rect = get_answer_button_rects(config)
    if yes_rect.collidepoint(position):
        return True
    if no_rect.collidepoint(position):
        return False
    return None


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
