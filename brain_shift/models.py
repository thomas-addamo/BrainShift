from dataclasses import dataclass

@dataclass
class Trial:
    position: str          # "TOP" o "BOTTOM"
    letter: str            # lettera maiuscola A-Z
    number: int            # numero 1-9
    expected_answer: bool
    user_answer: bool | None = None
    is_correct: bool = False
    response_time: float | None = None  # secondi impiegati a rispondere