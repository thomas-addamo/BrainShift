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
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Brain Shift")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Bianco
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
