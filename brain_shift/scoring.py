
def apply_answer(score: int, is_correct: bool) -> int:
    if is_correct:
        return score + 10
    elif score - 5 < 0:
        score = 0
        return score
    else:
        return score - 5