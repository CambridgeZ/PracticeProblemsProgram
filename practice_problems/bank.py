from pathlib import Path

import xlrd

from .question import OPTION_LABELS, Question


COLUMN_COUNT = 10


def load_questions(path: Path) -> list[Question]:
    questions = []
    numbers = set()
    try:
        with xlrd.open_workbook(path, on_demand=True) as workbook:
            if not workbook.nsheets:
                raise ValueError(f"{path} 没有工作表。")
            sheet = workbook.sheet_by_index(0)
            if sheet.nrows == 0 or sheet.ncols < COLUMN_COUNT:
                raise ValueError(f"{path} 的第一个工作表需要一行表头，且至少有十列。")

            for index in range(1, sheet.nrows):
                row = sheet.row_values(index, 0, COLUMN_COUNT)
                if all(cell == "" for cell in row):
                    continue
                location = f"{path} 第 {index + 1} 行"
                question = _parse_question(row, location)
                if question.number in numbers:
                    raise ValueError(f"{location}：题号 {question.number} 重复。")
                numbers.add(question.number)
                questions.append(question)
    except xlrd.XLRDError as exc:
        raise ValueError(f"无法读取题库 {path}：{exc}") from exc

    if not questions:
        raise ValueError(f"{path} 不包含可练习的题目。")
    return questions


def _parse_question(row: list[str | float | int], location: str) -> Question:
    catalog, raw_number, chapter, prompt, a, b, c, d, raw_answer, kind = map(
        _cell_text, row
    )
    try:
        number = int(raw_number)
    except ValueError as exc:
        raise ValueError(f"{location}：题号必须是正整数。") from exc
    if number <= 0:
        raise ValueError(f"{location}：题号必须是正整数。")
    if not prompt:
        raise ValueError(f"{location}：题干不能为空。")

    options = (a, b, c, d)
    available = {label for label, option in zip(OPTION_LABELS, options) if option}
    answer = raw_answer.upper()
    if not answer or len(set(answer)) != len(answer) or not set(answer) <= available:
        raise ValueError(f"{location}：答案须为不重复的非空选项字母（A–D）。")

    return Question(catalog, number, chapter, prompt, options, answer, kind)


def _cell_text(value: str | float | int) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()
