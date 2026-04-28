from models import Trial
from rules import compute_expected_answer, is_even, is_vowel


def generate_trial(rng) -> Trial:
    position = rng.choice(["TOP", "BOTTOM"])
    if is_even(rng.randint(1, 2)):
        letter = rng.choice(["A","E","I","O","U"])
    else:
        letter = rng.choice(["B","C","D","F","G","H","J","K","L","M","N","P","Q","R","S","T","V","W","X","Y","Z"])
    number = rng.randint(1, 9)

    expected_answer = compute_expected_answer(position, letter, number)
    return Trial(position=position, letter=letter, number=number, expected_answer=expected_answer)
