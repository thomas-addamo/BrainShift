import pygame
import random
import time
from dataclasses import dataclass, field

from generator import generate_trial
from scoring import apply_answer_advanced, apply_final_bonus
from ui import (
    draw_answer_buttons,
    draw_card,
    draw_feedback_icon,
    draw_hud,
    draw_intro,
    draw_paused,
    draw_results,
    draw_trial_prompt,
    get_answer_from_click,
)
import config

@dataclass
class GameState:
    rng: object

    score: int = 0
    multiplier: int = 1
    meter: int = 0
    max_multiplier: int = 1
    final_bonus: int = 0

    correct_answers: int = 0
    wrong_answers: int = 0

    trial: object = None
    next_trial: object = None
    position_history: list = field(default_factory=list)

    start_time: float = 0.0
    total_pause_time: float = 0.0  # somma di tutte le pause
    pause_start: float = 0.0       # quando è iniziata la pausa corrente

    state: str = "INTRO"

    feedback_until: float = 0.0        # time.time() fino a cui mostrare feedback
    feedback_is_correct: bool | None = None
    inter_trial_until: float = 0.0     # time.time() fino a cui bloccare input

    correct_count: int = 0   # corrette cumulative (per calcolare opacità)
    wrong_streak: int = 0    # errori consecutivi (per riportare le istruzioni)

    current_streak: int = 0
    best_streak: int = 0

    response_times: list = field(default_factory=list)
    trial_start_time: float = 0.0



def create_new_game() -> GameState:
    """Crea un GameState fresco per una nuova partita (inizia in INTRO)."""
    rng = random.Random()
    gs = GameState(rng=rng)
    first_trial = generate_trial(rng, [])
    gs.trial = first_trial
    gs.position_history = [first_trial.position]
    return gs


def start_playing(gs: GameState):
    """Passa allo stato PLAYING e azzera il timer."""
    gs.start_time = time.time()
    gs.trial_start_time = time.time()
    gs.state = "PLAYING"


def get_elapsed(gs: GameState) -> float:
    """Secondi di gioco effettivi (escluse le pause)."""
    return time.time() - gs.start_time - gs.total_pause_time


def get_instruction_opacity(correct_count: int, wrong_streak: int) -> int:
    """
    Calcola l'opacità (0-255) del testo delle istruzioni.
    Si riduce all'aumentare delle risposte corrette cumulative.
    Se il giocatore sbaglia molte volte di fila, le istruzioni riappaiono parzialmente.
    """

    if correct_count < config.FADE_THRESHOLD_1:
        base = 255
    elif correct_count < config.FADE_THRESHOLD_2:
        base = 178   # 70% di 255
    elif correct_count < config.FADE_THRESHOLD_3:
        base = 102   # 40% di 255
    else:
        base = 0

    if wrong_streak >= 3:
        extra = min(160, wrong_streak * 40)
        base = min(255, base + extra)

    return base


def submit_answer(gs: GameState, user_answer: bool):
    """Registra la risposta dell'utente, aggiorna lo scoring e prepara il prossimo trial."""
    now = time.time()

    gs.trial.response_time = now - gs.trial_start_time
    gs.response_times.append(gs.trial.response_time)

    is_correct = (gs.trial.expected_answer == user_answer)
    gs.trial.user_answer = user_answer
    gs.trial.is_correct = is_correct

    gs.score, gs.multiplier, gs.meter = apply_answer_advanced(
        gs.score, gs.multiplier, gs.meter, is_correct
    )
    gs.max_multiplier = max(gs.max_multiplier, gs.multiplier)

    if is_correct:
        gs.correct_answers += 1
        gs.correct_count += 1
        gs.wrong_streak = 0
        gs.current_streak += 1
        gs.best_streak = max(gs.best_streak, gs.current_streak)
    else:
        gs.wrong_answers += 1
        gs.wrong_streak += 1
        gs.current_streak = 0

    gs.feedback_until = now + config.FEEDBACK_DURATION
    gs.feedback_is_correct = is_correct
    gs.inter_trial_until = gs.feedback_until + config.INTER_TRIAL_DELAY
    gs.next_trial = generate_trial(gs.rng, gs.position_history)


def end_game(gs: GameState):
    """Calcola il bonus finale e passa allo stato RESULTS."""
    gs.final_bonus = 250 * gs.multiplier
    gs.score = apply_final_bonus(gs.score, gs.multiplier)
    gs.state = "RESULTS"


def reset_and_replay(gs: GameState):
    """Resetta tutti i valori per una nuova partita, ripartendo da PLAYING."""
    gs.rng = random.Random()
    gs.score = 0
    gs.multiplier = 1
    gs.meter = 0
    gs.max_multiplier = 1
    gs.final_bonus = 0
    gs.correct_answers = 0
    gs.wrong_answers = 0
    gs.position_history = []
    gs.next_trial = None
    gs.feedback_until = 0.0
    gs.feedback_is_correct = None
    gs.inter_trial_until = 0.0
    gs.correct_count = 0
    gs.wrong_streak = 0
    gs.current_streak = 0
    gs.best_streak = 0
    gs.response_times = []
    gs.total_pause_time = 0.0

    first_trial = generate_trial(gs.rng, [])
    gs.trial = first_trial
    gs.position_history = [first_trial.position]

    start_playing(gs)



pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Brain Shift")
clock = pygame.time.Clock()


gs = create_new_game()


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key in (pygame.K_SPACE, pygame.K_RETURN) and gs.state == "INTRO":
                start_playing(gs)

            elif event.key == pygame.K_p:
                if gs.state == "PLAYING":
                    gs.state = "PAUSED"
                    gs.pause_start = time.time()
                elif gs.state == "PAUSED":
                    gs.total_pause_time += time.time() - gs.pause_start
                    gs.state = "PLAYING"

            elif event.key == pygame.K_r and gs.state == "RESULTS":
                reset_and_replay(gs)

            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT) and gs.state == "PLAYING":
                can_answer = gs.next_trial is None and time.time() >= gs.inter_trial_until
                if can_answer:
                    user_answer = (event.key == pygame.K_LEFT)  # sinistra = SI
                    submit_answer(gs, user_answer)

        elif event.type == pygame.MOUSEBUTTONDOWN and gs.state == "PLAYING":
            can_answer = gs.next_trial is None and time.time() >= gs.inter_trial_until
            if can_answer:
                user_answer = get_answer_from_click(event.pos, config)
                if user_answer is not None:
                    submit_answer(gs, user_answer)

    if gs.state == "PLAYING":
        elapsed = get_elapsed(gs)

        if elapsed >= config.COUNTDOWN:
            end_game(gs)

        elif gs.next_trial is not None and time.time() >= gs.inter_trial_until:
            gs.position_history.append(gs.next_trial.position)
            gs.trial = gs.next_trial
            gs.next_trial = None
            gs.feedback_is_correct = None
            gs.trial_start_time = time.time()

    screen.fill((255, 255, 255))

    if gs.state == "INTRO":
        draw_intro(screen, config)

    elif gs.state == "PLAYING":
        elapsed = get_elapsed(gs)
        remaining = max(0, int(config.COUNTDOWN - elapsed))

        draw_hud(screen, remaining, gs.score, gs.multiplier, gs.meter, config)

        now = time.time()
        if now < gs.feedback_until:
            card_color = config.CORRECT_COLOR if gs.feedback_is_correct else config.WRONG_COLOR
        else:
            card_color = config.CARD_COLOR

        draw_card(screen, gs.trial, config, card_color)

        if now < gs.feedback_until:
            draw_feedback_icon(screen, gs.feedback_is_correct, config)

        opacity = get_instruction_opacity(gs.correct_count, gs.wrong_streak)
        draw_trial_prompt(screen, gs.trial, config, opacity)

        draw_answer_buttons(screen, config)

    elif gs.state == "PAUSED":
        elapsed = get_elapsed(gs)
        remaining = max(0, int(config.COUNTDOWN - elapsed))
        draw_hud(screen, remaining, gs.score, gs.multiplier, gs.meter, config)
        draw_card(screen, gs.trial, config, config.CARD_COLOR)
        draw_answer_buttons(screen, config)
        draw_paused(screen, config)

    elif gs.state == "RESULTS":
        avg_rt = (sum(gs.response_times) / len(gs.response_times)
                  if gs.response_times else None)
        draw_results(
            screen, gs.score, gs.correct_answers, gs.wrong_answers, config,
            max_multiplier=gs.max_multiplier,
            final_multiplier=gs.multiplier,
            avg_response_time=avg_rt,
            best_streak=gs.best_streak,
            final_bonus=gs.final_bonus,
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
