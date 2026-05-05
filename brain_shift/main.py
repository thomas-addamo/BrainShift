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
from generator import generate_trial
from scoring import apply_answer
from ui import draw_card, draw_timer, draw_results
import config


pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Brain Shift")
clock = pygame.time.Clock()

def reset_game():
    rng = random.Random(42)
    score = 0
    correct_answers = 0
    wrong_answers = 0
    trial = generate_trial(rng)
    start_time = pygame.time.get_ticks()
    state = "PLAYING"

    return rng, score, correct_answers, wrong_answers, trial, start_time, state

rng, score, correct_answers, wrong_answers, trial, start_time, state = reset_game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r and state == "RESULTS":
                rng, score, correct_answers, wrong_answers, trial, start_time, state = reset_game()
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT) and state == "PLAYING":
                user_answer = (event.key == pygame.K_LEFT)
                trial.user_answer = user_answer
                is_correct = (trial.expected_answer == user_answer)
                if is_correct:
                    score = apply_answer(score, True)
                    correct_answers += 1
                else:
                    score = apply_answer(score, False)
                    wrong_answers += 1
                print(f"Score: {score}, Correct: {correct_answers}, Wrong: {wrong_answers}")
                trial = generate_trial(rng)

    elapsed = (pygame.time.get_ticks() - start_time) / 1000
    if state == "PLAYING" and elapsed >= config.COUNTDOWN:
        state = "RESULTS"

    screen.fill((255, 255, 255))

    if state == "PLAYING":
        remaining_time = max(0, int(config.COUNTDOWN - elapsed))
        draw_timer(screen, remaining_time, config)
        draw_card(screen, trial, config)
    elif state == "RESULTS":
        draw_results(screen, score, correct_answers, wrong_answers, config)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
