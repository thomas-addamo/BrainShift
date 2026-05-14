import random
import pytest

try:
    from brain_shift.generator import generate_trial, MAX_POSITION_STREAK
    from brain_shift.rules import compute_expected_answer
except ImportError:
    generate_trial = None
    MAX_POSITION_STREAK = 3
    compute_expected_answer = None


def test_structure_check():
    assert generate_trial is not None, "Non trovo 'generate_trial' in generator.py"


def test_same_seed_produces_same_sequence():
    """Due generatori con lo stesso seed devono produrre gli stessi trial."""
    rng1 = random.Random(42)
    rng2 = random.Random(42)

    trials1 = [generate_trial(rng1, []) for _ in range(20)]
    trials2 = [generate_trial(rng2, []) for _ in range(20)]

    for t1, t2 in zip(trials1, trials2):
        assert t1.position == t2.position
        assert t1.letter == t2.letter
        assert t1.number == t2.number
        assert t1.expected_answer == t2.expected_answer


def test_different_seeds_produce_different_sequences():
    """Seed diversi devono (nella pratica) produrre sequenze diverse."""
    rng1 = random.Random(1)
    rng2 = random.Random(999)

    trials1 = [generate_trial(rng1, []) for _ in range(20)]
    trials2 = [generate_trial(rng2, []) for _ in range(20)]

    # Almeno un trial deve essere diverso
    any_diff = any(
        t1.position != t2.position or t1.letter != t2.letter or t1.number != t2.number
        for t1, t2 in zip(trials1, trials2)
    )
    assert any_diff


def test_no_streak_exceeds_maximum():
    """
    Generando 100 trial con lo stesso rng, non ci devono mai essere più di
    MAX_POSITION_STREAK posizioni uguali di fila.
    """
    rng = random.Random(7)
    history = []

    for _ in range(100):
        trial = generate_trial(rng, history)
        history.append(trial.position)

        # Controlla che gli ultimi MAX_POSITION_STREAK+1 non siano tutti uguali
        if len(history) > MAX_POSITION_STREAK:
            last = history[-(MAX_POSITION_STREAK + 1):]
            assert not (len(set(last)) == 1), (
                f"Streak troppo lunga trovata: {last}"
            )


def test_forces_opposite_position_after_streak():
    """
    Se gli ultimi MAX_POSITION_STREAK trial sono tutti TOP,
    il prossimo deve essere BOTTOM (e viceversa).
    """
    rng = random.Random(0)
    history = ["TOP"] * MAX_POSITION_STREAK

    trial = generate_trial(rng, history)
    assert trial.position == "BOTTOM", (
        f"Dopo {MAX_POSITION_STREAK} TOP di fila, ci si aspettava BOTTOM"
    )

    history2 = ["BOTTOM"] * MAX_POSITION_STREAK
    trial2 = generate_trial(rng, history2)
    assert trial2.position == "TOP", (
        f"Dopo {MAX_POSITION_STREAK} BOTTOM di fila, ci si aspettava TOP"
    )


def test_position_is_valid():
    """La posizione deve essere 'TOP' o 'BOTTOM'."""
    rng = random.Random(10)
    for _ in range(50):
        trial = generate_trial(rng, [])
        assert trial.position in ("TOP", "BOTTOM")


def test_number_is_in_range():
    """Il numero deve essere tra 1 e 9 inclusi."""
    rng = random.Random(10)
    for _ in range(50):
        trial = generate_trial(rng, [])
        assert 1 <= trial.number <= 9


def test_letter_is_uppercase():
    """La lettera deve essere una maiuscola A-Z."""
    rng = random.Random(10)
    for _ in range(50):
        trial = generate_trial(rng, [])
        assert trial.letter.isupper()
        assert len(trial.letter) == 1
        assert trial.letter.isalpha()


def test_expected_answer_is_correct():
    """expected_answer deve corrispondere a quanto calcola compute_expected_answer."""
    rng = random.Random(10)
    for _ in range(50):
        trial = generate_trial(rng, [])
        expected = compute_expected_answer(trial.position, trial.letter, trial.number)
        assert trial.expected_answer == expected, (
            f"Trial {trial}: expected_answer sbagliata"
        )
