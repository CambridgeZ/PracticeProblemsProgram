from os import SEEK_END
from pathlib import Path


class PracticeRecords:
    def __init__(self, directory: Path) -> None:
        self.progress_path = directory / "lastFinish.txt"
        self.wrong_path = directory / "错题记录.txt"

    def load_progress(self) -> int:
        numbers = _read_numbers(self.progress_path, minimum=0)
        if len(numbers) > 1:
            raise ValueError(f"{self.progress_path} 只能包含一个题号。")
        return numbers[0] if numbers else 0

    def save_progress(self, next_number: int) -> None:
        self.progress_path.write_text(f"{next_number}\n", encoding="utf-8")

    def load_wrong(self) -> list[int]:
        return _read_numbers(self.wrong_path)

    def append_wrong(self, number: int) -> None:
        with self.wrong_path.open("ab+") as file:
            file.seek(0, SEEK_END)
            separator = b""
            if file.tell():
                file.seek(-1, SEEK_END)
                if file.read(1) != b"\n":
                    separator = b"\n"
            file.write(separator + f"{number}\n".encode("ascii"))

    def clear_wrong(self) -> None:
        self.wrong_path.write_text("", encoding="utf-8")


def _read_numbers(path: Path, *, minimum: int = 1) -> list[int]:
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except FileNotFoundError:
        return []
    except UnicodeError as exc:
        raise ValueError(f"{path} 必须是 UTF-8 文本。") from exc

    numbers = []
    for line_number, line in enumerate(lines, start=1):
        if not (text := line.strip()):
            continue
        message = f"{path} 第 {line_number} 行：需要一个不小于 {minimum} 的整数。"
        try:
            number = int(text)
        except ValueError as exc:
            raise ValueError(message) from exc
        if number < minimum:
            raise ValueError(message)
        numbers.append(number)
    return numbers
