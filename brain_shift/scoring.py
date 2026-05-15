def apply_answer(score: int, is_correct: bool) -> int:
    if is_correct:
        return score + 10
    elif score - 5 < 0:
        return 0
    else:
        return score - 5


def apply_answer_advanced(score: int, multiplier: int, meter: int, is_correct: bool):
    """Restituisce (score, multiplier, meter) aggiornati."""
    if is_correct:
        score += 50 * multiplier
        meter += 1
        if meter == 4:
            multiplier = min(multiplier + 1, 10)
            meter = 0
    else:
        score = max(0, score - 5)
        if meter > 0:
            meter = 0
        else:
            multiplier = max(multiplier - 1, 1)
    return score, multiplier, meter


def apply_final_bonus(score: int, multiplier: int) -> int:
    """Bonus di fine partita: 250 × moltiplicatore finale."""
    return score + 250 * multiplier
