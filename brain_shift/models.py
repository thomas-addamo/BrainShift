from dataclasses import dataclass

@dataclass
class Trial:
    position: str #TOP / BOTTOM
    letter: str # lettera maiuscola (A-Z)
    number: int #un numero
    expected_answer: bool
    user_answer: bool | None = None
    is_correct: bool = False