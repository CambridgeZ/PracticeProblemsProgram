import argparse
import sys
from pathlib import Path
from random import Random

from .bank import load_questions
from .question import Question
from .records import PracticeRecords
from .session import run_session


MENU = """\
请选择功能：
0. 顺序做题
1. 随机抽题（不重复）
2. 错题回顾（按记录顺序）
3. 清空错题库
4. 退出"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="在终端练习 XLS 题库。")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("."),
        metavar="目录",
        help="存放题库.xls 和答题记录的目录（默认：当前目录）",
    )
    args = parser.parse_args(argv)
    try:
        questions = load_questions(args.data_dir / "题库.xls")
        _run_menu(questions, PracticeRecords(args.data_dir))
    except (OSError, ValueError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1
    except EOFError:
        print("\n输入结束，已退出。")
    except KeyboardInterrupt:
        print("\n已中断。", file=sys.stderr)
        return 130
    return 0


def _run_menu(questions: list[Question], records: PracticeRecords) -> None:
    print("欢迎使用刷题程序（原始版本由 XueJingyuan / Platinum 设计）。")
    by_number = {question.number: question for question in questions}
    rng = Random()
    while True:
        print(f"\n{MENU}")
        choice = input("请输入：").strip()
        if choice == "0":
            _run_sequence(questions, records, rng)
        elif choice == "1":
            print("\n随机做题不记录错题，输入一个空格可跳过当前题。")
            shuffled = questions.copy()
            rng.shuffle(shuffled)
            run_session(shuffled, rng, allow_skip=True)
        elif choice == "2":
            _run_review(by_number, records, rng)
        elif choice == "3":
            if input("输入 yes 确认清空错题记录：").strip() == "yes":
                records.clear_wrong()
                print("清除错题成功")
            else:
                print("已取消清除错题")
        elif choice == "4":
            print("感谢使用")
            return
        else:
            print("请输入 0 到 4 之间的菜单编号。")


def _run_sequence(
    questions: list[Question], records: PracticeRecords, rng: Random
) -> None:
    next_number = records.load_progress()
    start: int | None = 0
    if next_number:
        start = next(
            (i for i, question in enumerate(questions) if question.number == next_number),
            None,
        )
        if start is None:
            print(
                f"当前题库没有进度题号 {next_number}。请核对题库，"
                f"或备份后清空 {records.progress_path}。",
                file=sys.stderr,
            )
            return

    paused_at = run_session(questions[start:], rng, on_wrong=records.append_wrong)
    if paused_at is None:
        records.save_progress(0)
        print("顺序进度已重置，下次从第一题开始。")
    else:
        records.save_progress(paused_at)
        print(f"已保存进度，下次从第 {paused_at} 题继续。")


def _run_review(
    by_number: dict[int, Question], records: PracticeRecords, rng: Random
) -> None:
    wrong_numbers = records.load_wrong()
    if not wrong_numbers:
        print("错题记录为空，请先顺序做题。")
        return
    questions = [by_number[number] for number in wrong_numbers if number in by_number]
    missing = len(wrong_numbers) - len(questions)
    if missing:
        print(f"有 {missing} 条错题记录在当前题库中找不到，已略过。", file=sys.stderr)
    if questions:
        run_session(questions, rng)
    else:
        print("没有可回顾的题目。")
