import pytest

try:
    from brain_shift.scoring import apply_answer_advanced, apply_final_bonus
except ImportError:
    apply_answer_advanced = None
    apply_final_bonus = None


def test_structure_check():
    assert apply_answer_advanced is not None, (
        "Non trovo 'apply_answer_advanced' in scoring.py"
    )
    assert apply_final_bonus is not None, (
        "Non trovo 'apply_final_bonus' in scoring.py"
    )


def test_correct_answer_adds_50_with_multiplier_1():
    score, multiplier, meter = apply_answer_advanced(0, 1, 0, True)
    assert score == 50


def test_correct_answer_adds_100_with_multiplier_2():
    score, multiplier, meter = apply_answer_advanced(0, 2, 0, True)
    assert score == 100


def test_correct_answer_increments_meter():
    score, multiplier, meter = apply_answer_advanced(0, 1, 0, True)
    assert meter == 1


def test_four_correct_answers_increase_multiplier():
    score, multiplier, meter = 0, 1, 0
    for _ in range(4):
        score, multiplier, meter = apply_answer_advanced(score, multiplier, meter, True)
    assert multiplier == 2
    assert meter == 0  # il meter si azzera al level-up


def test_multiplier_does_not_exceed_10():
    score, multiplier, meter = 0, 10, 0
    # Con multiplier già a 10, altre 4 corrette non devono alzarlo oltre
    for _ in range(4):
        score, multiplier, meter = apply_answer_advanced(score, multiplier, meter, True)
    assert multiplier == 10


def test_multiplier_saturates_at_10():
    """Da multiplier 9: una serie di 4 corrette deve portare a 10, non a 11."""
    score, multiplier, meter = 0, 9, 0
    for _ in range(4):
        score, multiplier, meter = apply_answer_advanced(score, multiplier, meter, True)
    assert multiplier == 10


def test_wrong_answer_resets_meter_when_meter_is_positive():
    score, multiplier, meter = apply_answer_advanced(0, 1, 2, False)
    assert meter == 0
    assert multiplier == 1   # il moltiplicatore non cambia se meter era > 0


def test_wrong_answer_decreases_multiplier_when_meter_is_zero():
    score, multiplier, meter = apply_answer_advanced(0, 3, 0, False)
    assert multiplier == 2
    assert meter == 0


def test_multiplier_does_not_go_below_1():
    score, multiplier, meter = apply_answer_advanced(0, 1, 0, False)
    assert multiplier == 1   # non può andare sotto 1


def test_multiplier_decreases_when_meter_is_empty():
    """
    Con meter = 0 e multiplier = 5, una risposta errata deve portare
    multiplier a 4.
    """
    score, multiplier, meter = apply_answer_advanced(0, 5, 0, False)
    assert multiplier == 4


def test_sequence_from_specification():
    """
    Riproduce l'esempio della specifica:
    partendo da score=0, multiplier=1, meter=0 con 6 trial:
    1 corretta, 2 corretta, 3 corretta, 4 corretta (level-up!),
    5 corretta, 6 errata
    """
    score, multiplier, meter = 0, 1, 0

    score, multiplier, meter = apply_answer_advanced(score, multiplier, meter, True)
    assert score == 50 and multiplier == 1 and meter == 1

    score, multiplier, meter = apply_answer_advanced(score, multiplier, meter, True)
    assert score == 100 and multiplier == 1 and meter == 2

    score, multiplier, meter = apply_answer_advanced(score, multiplier, meter, True)
    assert score == 150 and multiplier == 1 and meter == 3

    score, multiplier, meter = apply_answer_advanced(score, multiplier, meter, True)
    assert score == 200 and multiplier == 2 and meter == 0   # level-up!

    score, multiplier, meter = apply_answer_advanced(score, multiplier, meter, True)
    assert score == 300 and multiplier == 2 and meter == 1   # +100 perché mult=2

    score, multiplier, meter = apply_answer_advanced(score, multiplier, meter, False)
    assert score == 295 and multiplier == 2 and meter == 0   # -5 punti, meter azzera, mult resta


def test_final_bonus_with_multiplier_1():
    assert apply_final_bonus(0, 1) == 250


def test_final_bonus_with_multiplier_3():
    assert apply_final_bonus(100, 3) == 850   # 100 + 250*3


def test_final_bonus_application():
    """Il bonus finale aggiunge 250 × moltiplicatore al punteggio corrente."""
    score = 1000
    multiplier = 5
    result = apply_final_bonus(score, multiplier)
    assert result == score + 250 * multiplier
