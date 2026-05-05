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
from ui import draw_card
import config


pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Brain Shift")
clock = pygame.time.Clock()

rng = random.Random(42)
score = 0
correct_answers = 0
wrong_answers = 0
trial = generate_trial(rng)
start_time = pygame.time.get_ticks()
state = 'PLAYING'

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT) and state == 'PLAYING':
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
    elapsed = pygame.time.get_ticks() - start_time
    if elapsed > 60000:  # 1 minuto
        state = 'RESULT'

    screen.fill((255, 255, 255))
    draw_card(screen, trial, config)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
