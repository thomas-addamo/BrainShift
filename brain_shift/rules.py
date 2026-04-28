def is_even(number: int) -> bool:
    if number % 2 == 0:
        return True

def is_vowel(letter: str) -> bool:
    if letter.upper() in 'AEIOU':
        return True

def compute_expected_answer(position: str, letter: str, number: int) -> bool:
    if position == "TOP":
        return is_even(number)
    if position == "BOTTOM":
        return not is_vowel(letter)