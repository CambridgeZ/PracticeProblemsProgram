from dataclasses import dataclass, replace
from random import Random


OPTION_LABELS = "ABCD"


@dataclass(frozen=True)
class Question:
    catalog: str
    number: int
    chapter: str
    prompt: str
    options: tuple[str, ...]
    answer: str
    kind: str

    def shuffled(self, rng: Random) -> "Question":
        # Track the original positions so identical option text stays unambiguous.
        positions = [index for index, option in enumerate(self.options) if option]
        rng.shuffle(positions)
        return replace(
            self,
            options=tuple(self.options[index] for index in positions),
            answer="".join(
                label
                for label, index in zip(OPTION_LABELS, positions)
                if OPTION_LABELS[index] in self.answer
            ),
        )

    def is_correct(self, response: str) -> bool:
        return sorted(response.upper()) == sorted(self.answer)
