SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CARD_WIDTH = 240
CARD_HEIGHT = 160
TOP_Y = 80
BOTTOM_Y = 360

# Colori carta e feedback
CARD_COLOR = (200, 200, 255)
CORRECT_COLOR = (120, 220, 120)
WRONG_COLOR = (230, 100, 100)

# Colori testo
TEXT_COLOR = (0, 0, 0)
MUTED_TEXT_COLOR = (95, 95, 95)

# Colori HUD e pulsanti
BAR_COLOR = (235, 235, 240)
BUTTON_COLOR = (255, 255, 255)
BUTTON_BORDER_COLOR = (80, 80, 90)

# Colori meter bar
METER_FULL_COLOR = (80, 190, 80)
METER_EMPTY_COLOR = (200, 200, 200)
METER_BORDER_COLOR = (100, 100, 100)

# Font
FONT_NAME = None   # None = font di sistema predefinito di pygame
FONT_SIZE = 72

# Timing
COUNTDOWN = 60            # durata partita in secondi
FEEDBACK_DURATION = 0.35  # durata feedback verde/rosso in secondi
INTER_TRIAL_DELAY = 0.15  # pausa dopo il feedback prima del trial successivo

FADE_THRESHOLD_1 = 4    # 0-3 corrette  → opacità 100%
FADE_THRESHOLD_2 = 8    # 4-7 corrette  → opacità 70%
FADE_THRESHOLD_3 = 12   # 8-11 corrette → opacità 40%
                        # 12+ corrette  → opacità 0% (sparisce)
