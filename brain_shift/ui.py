import pygame
from models import Trial



def get_card_rect(trial: Trial, config):
    x = (config.SCREEN_WIDTH - config.CARD_WIDTH) // 2
    y = config.TOP_Y if trial.position == "TOP" else config.BOTTOM_Y
    return pygame.Rect(x, y, config.CARD_WIDTH, config.CARD_HEIGHT)


def draw_card(surface, trial: Trial, config, card_color=None):
    card_rect = get_card_rect(trial, config)
    color = card_color or config.CARD_COLOR

    pygame.draw.rect(surface, color, card_rect, border_radius=12)
    pygame.draw.rect(surface, (150, 150, 180), card_rect, 2, border_radius=12)

    font = pygame.font.Font(config.FONT_NAME, config.FONT_SIZE)
    text = f"{trial.letter}{trial.number}"
    text_surface = font.render(text, True, config.TEXT_COLOR)
    text_rect = text_surface.get_rect(center=card_rect.center)
    surface.blit(text_surface, text_rect)



def _draw_arrow_on(surface, start, end, color):
    pygame.draw.line(surface, color, start, end, 3)
    if end[0] > start[0]:
        tip = end
        points = [tip, (tip[0] - 12, tip[1] - 7), (tip[0] - 12, tip[1] + 7)]
    else:
        tip = end
        points = [tip, (tip[0] + 12, tip[1] - 7), (tip[0] + 12, tip[1] + 7)]
    pygame.draw.polygon(surface, color, points)



def draw_trial_prompt(surface, trial: Trial, config, opacity: int = 255):
    """
    Disegna il testo della regola e la freccia accanto alla carta.
    opacity va da 0 (invisibile) a 255 (completamente visibile).
    """
    if opacity <= 0:
        return

    card_rect = get_card_rect(trial, config)
    r, g, b = config.MUTED_TEXT_COLOR

    temp = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
    color_rgba = (r, g, b, opacity)

    font = pygame.font.Font(config.FONT_NAME, 24)

    if trial.position == "TOP":
        start = (card_rect.right + 18, card_rect.centery)
        end = (card_rect.right + 68, card_rect.centery)
        _draw_arrow_on(temp, start, end, color_rgba)

        text_surface = font.render("Il numero è pari?", True, (r, g, b))
        text_surface.set_alpha(opacity)
        text_rect = text_surface.get_rect(midleft=(card_rect.right + 82, card_rect.centery))
        temp.blit(text_surface, text_rect)
    else:
        start = (card_rect.left - 18, card_rect.centery)
        end = (card_rect.left - 68, card_rect.centery)
        _draw_arrow_on(temp, start, end, color_rgba)

        text_surface = font.render("La lettera è vocale?", True, (r, g, b))
        text_surface.set_alpha(opacity)
        text_rect = text_surface.get_rect(midright=(card_rect.left - 82, card_rect.centery))
        temp.blit(text_surface, text_rect)

    surface.blit(temp, (0, 0))



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
        pygame.draw.line(surface, color,
                         (center_x - 22, center_y - 22),
                         (center_x + 22, center_y + 22), 8)
        pygame.draw.line(surface, color,
                         (center_x + 22, center_y - 22),
                         (center_x - 22, center_y + 22), 8)



def draw_hud(surface, remaining_time, score, multiplier, meter, config):
    """Disegna tutta la barra HUD in alto: timer, punteggio, moltiplicatore e meter."""
    font = pygame.font.Font(config.FONT_NAME, 30)
    small_font = pygame.font.Font(config.FONT_NAME, 18)

    timer_surf = font.render(f"Tempo: {remaining_time}s", True, config.TEXT_COLOR)
    surface.blit(timer_surf, timer_surf.get_rect(center=(config.SCREEN_WIDTH // 2, 28)))

    score_surf = font.render(f"Punti: {score}", True, config.TEXT_COLOR)
    surface.blit(score_surf, score_surf.get_rect(midright=(config.SCREEN_WIDTH - 12, 28)))

    mult_surf = font.render(f"x{multiplier}", True, config.TEXT_COLOR)
    surface.blit(mult_surf, mult_surf.get_rect(midleft=(12, 18)))

    for i in range(4):
        rect = pygame.Rect(12 + i * 22, 40, 18, 14)
        color = config.METER_FULL_COLOR if i < meter else config.METER_EMPTY_COLOR
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, config.METER_BORDER_COLOR, rect, 1)

    label_surf = small_font.render("meter", True, config.MUTED_TEXT_COLOR)
    surface.blit(label_surf, label_surf.get_rect(midleft=(12, 58)))


def draw_timer(surface, remaining_time, config):
    font = pygame.font.Font(config.FONT_NAME, 36)
    text_surface = font.render(f"Tempo: {remaining_time}", True, config.TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, 35))
    surface.blit(text_surface, text_rect)



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
    hint_font = pygame.font.Font(config.FONT_NAME, 17)
    yes_rect, no_rect = get_answer_button_rects(config)

    hint_surface = hint_font.render(
        "Clicca SI/NO oppure usa le frecce: sinistra = SI, destra = NO",
        True, config.MUTED_TEXT_COLOR,
    )
    hint_rect = hint_surface.get_rect(center=(config.SCREEN_WIDTH // 2, bar_rect.top + 14))
    surface.blit(hint_surface, hint_rect)

    for label, rect in [("SI", yes_rect), ("NO", no_rect)]:
        pygame.draw.rect(surface, config.BUTTON_COLOR, rect, border_radius=8)
        pygame.draw.rect(surface, config.BUTTON_BORDER_COLOR, rect, 2, border_radius=8)
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



def draw_intro(surface, config):
    font_title = pygame.font.Font(config.FONT_NAME, 56)
    font_section = pygame.font.Font(config.FONT_NAME, 26)
    font_body = pygame.font.Font(config.FONT_NAME, 22)
    font_start = pygame.font.Font(config.FONT_NAME, 28)

    title_surf = font_title.render("Brain Shift", True, config.TEXT_COLOR)
    surface.blit(title_surf, title_surf.get_rect(center=(config.SCREEN_WIDTH // 2, 70)))

    sections = [
        ("Regole del gioco", font_section, config.TEXT_COLOR),
        ("Carta in ALTO  →  il numero è PARI?", font_body, config.MUTED_TEXT_COLOR),
        ("Carta in BASSO  →  la lettera è VOCALE?", font_body, config.MUTED_TEXT_COLOR),
        ("", None, None),
        ("Controlli", font_section, config.TEXT_COLOR),
        ("Freccia SINISTRA  =  SI", font_body, config.MUTED_TEXT_COLOR),
        ("Freccia DESTRA  =  NO", font_body, config.MUTED_TEXT_COLOR),
        ("P  =  Pausa / Riprendi", font_body, config.MUTED_TEXT_COLOR),
        ("", None, None),
        ("Premi SPAZIO o INVIO per iniziare", font_start, config.TEXT_COLOR),
    ]

    y = 145
    for text, font, color in sections:
        if font is None:
            y += 14
            continue
        surf = font.render(text, True, color)
        surface.blit(surf, surf.get_rect(center=(config.SCREEN_WIDTH // 2, y)))
        y += 40



def draw_paused(surface, config):
    overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    surface.blit(overlay, (0, 0))

    font_big = pygame.font.Font(config.FONT_NAME, 60)
    font = pygame.font.Font(config.FONT_NAME, 28)

    pausa_surf = font_big.render("PAUSA", True, (255, 255, 255))
    surface.blit(pausa_surf, pausa_surf.get_rect(center=(config.SCREEN_WIDTH // 2,
                                                          config.SCREEN_HEIGHT // 2 - 40)))

    resume_surf = font.render("Premi P per riprendere", True, (210, 210, 210))
    surface.blit(resume_surf, resume_surf.get_rect(center=(config.SCREEN_WIDTH // 2,
                                                            config.SCREEN_HEIGHT // 2 + 30)))



def draw_results(surface, score, correct_answers, wrong_answers, config,
                 max_multiplier=1, final_multiplier=1,
                 avg_response_time=None, best_streak=0, final_bonus=0):
    font_big = pygame.font.Font(config.FONT_NAME, 46)
    font = pygame.font.Font(config.FONT_NAME, 26)

    total = correct_answers + wrong_answers
    accuracy = (correct_answers / total * 100) if total > 0 else 0.0

    lines = [
        ("Risultati", font_big),
        (f"Punteggio finale: {score}", font),
        (f"  di cui bonus finale: +{final_bonus}", font),
        (f"Corrette: {correct_answers}   Sbagliate: {wrong_answers}", font),
        (f"Accuratezza: {accuracy:.1f}%", font),
        (f"Streak migliore: {best_streak}", font),
        (f"Moltiplicatore  max: x{max_multiplier}   finale: x{final_multiplier}", font),
    ]

    if avg_response_time is not None:
        lines.append((f"Tempo medio risposta: {avg_response_time:.2f}s", font))

    lines.append(("", None))
    lines.append(("Premi R per rigiocare", font))

    y = 70
    for text, current_font in lines:
        if current_font is None:
            y += 16
            continue
        text_surface = current_font.render(text, True, config.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, y))
        surface.blit(text_surface, text_rect)
        y += 50
