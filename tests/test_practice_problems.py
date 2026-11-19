import re
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from random import Random
from unittest.mock import patch

from practice_problems.bank import load_questions
from practice_problems.cli import main
from practice_problems.question import Question
from practice_problems.records import PracticeRecords


class QuestionTests(unittest.TestCase):
    def test_shuffle_tracks_option_positions_even_when_text_is_identical(self):
        question = Question("", 1, "", "题干", ("相同", "", "相同", "不同"), "AD", "多选题")
        rng = Random()
        with patch.object(rng, "shuffle", side_effect=lambda values: values.reverse()):
            presented = question.shuffled(rng)

        self.assertEqual(presented.options, ("不同", "相同", "相同"))
        self.assertEqual(presented.answer, "AC")
        self.assertTrue(presented.is_correct("ca"))
        self.assertFalse(presented.is_correct("aa"))


class BankTests(unittest.TestCase):
    def test_loads_bundled_xls_with_blank_option_cells(self):
        bank = Path(__file__).resolve().parents[1] / "题库.xls"
        questions = load_questions(bank)

        self.assertEqual(len(questions), 995)
        self.assertTrue(any("" in question.options for question in questions))

    def test_invalid_workbook_error_names_the_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.xls"
            path.write_bytes(b"not an Excel workbook")
            with self.assertRaisesRegex(ValueError, r"无法读取题库.*invalid\.xls"):
                load_questions(path)


class RecordTests(unittest.TestCase):
    def test_appending_preserves_existing_ids_without_a_final_newline(self):
        with tempfile.TemporaryDirectory() as directory:
            records = PracticeRecords(Path(directory))
            records.wrong_path.write_text("17\n3", encoding="utf-8-sig")

            records.append_wrong(17)

            self.assertEqual(records.load_wrong(), [17, 3, 17])

    def test_invalid_record_reports_the_line_instead_of_resetting_it(self):
        with tempfile.TemporaryDirectory() as directory:
            records = PracticeRecords(Path(directory))
            records.wrong_path.write_text("17\ninvalid\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, r"错题记录\.txt 第 2 行"):
                records.load_wrong()


class MenuTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.data_dir = Path(directory.name)
        self.records = PracticeRecords(self.data_dir)
        self.questions = [
            Question("", number, "", "题干", ("甲", "乙", "丙", "丁"), "A", "单选题")
            for number in (17, 3)
        ]

    def run_menu(self, *commands):
        output, errors = StringIO(), StringIO()
        with (
            patch("practice_problems.cli.load_questions", return_value=self.questions),
            patch.object(Random, "shuffle", return_value=None),
            patch("builtins.input", side_effect=commands),
            redirect_stdout(output),
            redirect_stderr(errors),
        ):
            result = main(["--data-dir", str(self.data_dir)])
        self.assertEqual(result, 0, errors.getvalue())
        ids = [int(number) for number in re.findall(r"题号:(\d+)\n", output.getvalue())]
        return ids, output.getvalue(), errors.getvalue()

    def test_sequence_pauses_at_the_unanswered_question_and_resumes(self):
        ids, _, _ = self.run_menu("0", "B", "", "1", "4")
        self.assertEqual(ids, [17, 3])
        self.assertEqual(self.records.load_progress(), 3)
        self.assertEqual(self.records.load_wrong(), [17])

        ids, output, _ = self.run_menu("0", "a", "4")
        self.assertEqual(ids, [3])
        self.assertIn("本次做了1题，正确率为100.00%", output)
        self.assertEqual(self.records.load_progress(), 0)
        self.assertEqual(self.records.load_wrong(), [17])

    def test_stale_progress_is_reported_without_overwriting_it(self):
        self.records.save_progress(99)

        ids, _, errors = self.run_menu("0", "4")

        self.assertEqual(ids, [])
        self.assertIn("当前题库没有进度题号 99", errors)
        self.assertEqual(self.records.load_progress(), 99)

    def test_random_round_uses_each_question_without_writing_records(self):
        self.records.save_progress(3)
        self.records.append_wrong(3)

        ids, output, _ = self.run_menu("1", " ", "B", "4")

        self.assertEqual(ids, [17, 3])
        self.assertIn("本次做了1题，正确率为0.00%", output)
        self.assertEqual(self.records.load_progress(), 3)
        self.assertEqual(self.records.load_wrong(), [3])

    def test_review_uses_record_order_and_does_not_change_records_on_pause(self):
        self.records.save_progress(17)
        for number in (3, 99, 17, 3):
            self.records.append_wrong(number)

        ids, output, errors = self.run_menu("2", "?", "A", "B", "A", "4")
        self.assertEqual(ids, [3, 17, 3])
        self.assertIn("本题有 1 个正确选项", output)
        self.assertIn("1 条错题记录在当前题库中找不到", errors)

        self.run_menu("2", "", "1", "4")
        self.assertEqual(self.records.load_progress(), 17)
        self.assertEqual(self.records.load_wrong(), [3, 99, 17, 3])

    def test_clearing_wrong_answers_requires_confirmation(self):
        self.records.save_progress(3)
        self.records.append_wrong(17)

        self.run_menu("3", "no", "4")
        self.assertEqual(self.records.load_wrong(), [17])

        ids, output, _ = self.run_menu("3", "yes", "2", "4")
        self.assertEqual(ids, [])
        self.assertIn("错题记录为空", output)
        self.assertEqual(self.records.load_progress(), 3)
