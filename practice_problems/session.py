from collections.abc import Callable, Sequence
from random import Random
from time import monotonic

from .question import OPTION_LABELS, Question


def run_session(
    questions: Sequence[Question],
    rng: Random,
    *,
    on_wrong: Callable[[int], None] | None = None,
    allow_skip: bool = False,
) -> int | None:
    """Run one round; return the unanswered question number if paused."""
    answered = earned = possible = 0
    started = monotonic()
    paused_at = None

    for position, question in enumerate(questions, start=1):
        presented = question.shuffled(rng)
        _show_question(presented, position, len(questions))
        question_started = monotonic()
        answer = _read_answer(len(presented.answer), allow_skip=allow_skip)
        if answer is None:
            paused_at = question.number
            break
        if answer == " ":
            continue

        answered += 1
        points = len(presented.answer)
        possible += points
        if presented.is_correct(answer):
            earned += points
            print("答案正确")
        else:
            if on_wrong is not None:
                on_wrong(question.number)
            print("答案错误，本题答案是", presented.answer)
        print(f"当前正确率{earned / possible:.2%}")
        print(f"本题用时{monotonic() - question_started:.3f}s")

    if answered:
        elapsed = monotonic() - started
        print(
            f"\n本次做了{answered}题，正确率为{earned / possible:.2%}，"
            f"共用时{elapsed:.1f}s，题均用时{elapsed / answered:.1f}s"
        )
    if paused_at is None:
        print("\n本轮题目已结束。")
    return paused_at


def _show_question(question: Question, position: int, total: int) -> None:
    print(f"\n当前进度{position}/{total}")
    print(f"目录:{question.catalog} 题号:{question.number}")
    print(f"\n{question.kind}——{question.prompt}")
    for label, option in zip(OPTION_LABELS, question.options):
        print(f"{label}:{option}")


def _read_answer(answer_size: int, *, allow_skip: bool) -> str | None:
    prompt = "请输入答案："
    can_retry = True
    while True:
        response = input(prompt)
        if response == "":
            if input("你真的要退出吗，输入1退出：").strip() == "1":
                return None
            prompt = "请输入答案："
            continue
        if response == "?":
            print(f"提示：本题有 {answer_size} 个正确选项。")
            prompt = "请再次输入答案："
            continue
        if allow_skip and response == " ":
            return response

        answer = response.strip().upper()
        if can_retry and (len(answer) == 1) != (answer_size == 1):
            kind = "单选题" if answer_size == 1 else "多选题"
            prompt = f"本题是{kind}！请再次输入答案："
            can_retry = False
            continue
        return answer
