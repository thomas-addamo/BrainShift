#brain_shift/
#├── main.py          ← bootstrap, main loop, macchina a stati
#├── config.py        ← costanti: colori, font, timing, punteggi
#├── models.py        ← dataclass: Trial (e altri dati strutturati)
#├── rules.py         ← is_even, is_vowel, compute_expected_answer
#├── scoring.py       ← funzione che aggiorna il punteggio
#├── generator.py     ← genera trial casuali con seed
#├── ui.py            ← rendering HUD, carta, pulsanti
#├── assets/          ← immagini, font, suoni (se usati)
#└── tests/           ← test pytest forniti (li ricevete già pronti)

import pygame
import random
import time
from generator import generate_trial
from scoring import apply_answer
from ui import (
    draw_answer_buttons,
    draw_card,
    draw_feedback_icon,
    draw_results,
    draw_timer,
    draw_trial_prompt,
    get_answer_from_click,
)
import config


pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Brain Shift")
clock = pygame.time.Clock()

def reset_game():
    rng = random.Random()
    score = 0
    correct_answers = 0
    wrong_answers = 0
    trial = generate_trial(rng)
    start_time = pygame.time.get_ticks()
    state = "PLAYING"
    feedback_until = 0
    feedback_is_correct = None
    next_trial = None

    return (
        rng,
        score,
        correct_answers,
        wrong_answers,
        trial,
        start_time,
        state,
        feedback_until,
        feedback_is_correct,
        next_trial,
    )

rng, score, correct_answers, wrong_answers, trial, start_time, state, feedback_until, feedback_is_correct, next_trial = reset_game()


def submit_answer(user_answer, trial, score, correct_answers, wrong_answers, rng):
    trial.user_answer = user_answer
    is_correct = trial.expected_answer == user_answer

    if is_correct:
        score = apply_answer(score, True)
        correct_answers += 1
    else:
        score = apply_answer(score, False)
        wrong_answers += 1

    print(f"Score: {score}, Correct: {correct_answers}, Wrong: {wrong_answers}")
    feedback_until = time.time() + config.FEEDBACK_DURATION
    next_trial = generate_trial(rng)

    return score, correct_answers, wrong_answers, feedback_until, is_correct, next_trial


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r and state == "RESULTS":
                rng, score, correct_answers, wrong_answers, trial, start_time, state, feedback_until, feedback_is_correct, next_trial = reset_game()
            elif (
                event.key in (pygame.K_LEFT, pygame.K_RIGHT)
                and state == "PLAYING"
                and time.time() >= feedback_until
            ):
                user_answer = (event.key == pygame.K_LEFT)
                score, correct_answers, wrong_answers, feedback_until, feedback_is_correct, next_trial = submit_answer(
                    user_answer,
                    trial,
                    score,
                    correct_answers,
                    wrong_answers,
                    rng,
                )
        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and state == "PLAYING"
            and time.time() >= feedback_until
        ):
            user_answer = get_answer_from_click(event.pos, config)
            if user_answer is not None:
                score, correct_answers, wrong_answers, feedback_until, feedback_is_correct, next_trial = submit_answer(
                    user_answer,
                    trial,
                    score,
                    correct_answers,
                    wrong_answers,
                    rng,
                )

    elapsed = (pygame.time.get_ticks() - start_time) / 1000
    if state == "PLAYING" and elapsed >= config.COUNTDOWN:
        state = "RESULTS"

    if state == "PLAYING" and next_trial is not None and time.time() >= feedback_until:
        trial = next_trial
        next_trial = None
        feedback_is_correct = None

    screen.fill((255, 255, 255))

    if state == "PLAYING":
        remaining_time = max(0, int(config.COUNTDOWN - elapsed))
        draw_timer(screen, remaining_time, config)
        draw_trial_prompt(screen, trial, config)
        if time.time() < feedback_until:
            if feedback_is_correct:
                card_color = config.CORRECT_COLOR
            else:
                card_color = config.WRONG_COLOR
        else:
            card_color = config.CARD_COLOR

        draw_card(screen, trial, config, card_color)
        if time.time() < feedback_until:
            draw_feedback_icon(screen, feedback_is_correct, config)
        draw_answer_buttons(screen, config)
    elif state == "RESULTS":
        draw_results(screen, score, correct_answers, wrong_answers, config)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
