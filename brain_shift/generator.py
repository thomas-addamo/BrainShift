import random
from models import Trial
from rules import compute_expected_answer, is_even


VOWELS = ["A", "E", "I", "O", "U"]
CONSONANTS = ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M",
              "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"]

MAX_POSITION_STREAK = 3


def generate_trial(rng, position_history=None) -> Trial:
    """
    Genera un trial casuale.

    - rng: oggetto random.Random con seed configurabile
    - position_history: lista delle posizioni dei trial precedenti.
      Se gli ultimi MAX_POSITION_STREAK trial hanno la stessa posizione,
      il generatore forza l'altra per evitare streak troppo lunghe.
    """
    if position_history is None:
        position_history = []

    recent = position_history[-MAX_POSITION_STREAK:]
    if len(recent) == MAX_POSITION_STREAK and len(set(recent)) == 1:
        position = "BOTTOM" if recent[-1] == "TOP" else "TOP"
    else:
        position = rng.choice(["TOP", "BOTTOM"])

    if rng.random() < 0.5:
        letter = rng.choice(VOWELS)
    else:
        letter = rng.choice(CONSONANTS)

    number = rng.randint(1, 9)

    expected_answer = compute_expected_answer(position, letter, number)
    return Trial(position=position, letter=letter, number=number,
                 expected_answer=expected_answer)
