import json
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = Path(__file__).resolve().parents[1] / "streamlit_quiz_app.py"


def test_quiz_scores_correct_and_incorrect_answers(tmp_path, monkeypatch):
    questions = [
        {
            "id": 1,
            "question": "Which planet is closest to the Sun?",
            "options": {"A": "Mercury", "B": "Venus", "C": "Earth", "D": "Mars"},
            "correct_answer": "A",
        },
        {
            "id": 2,
            "question": "What is two plus two?",
            "options": {"A": "Three", "B": "Four", "C": "Five", "D": "Six"},
            "correct_answer": "B",
        },
    ]
    (tmp_path / "questions.json").write_text(json.dumps(questions), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    app = AppTest.from_file(APP_PATH).run()
    app.sidebar.radio[0].set_value("📚 Mulai Quiz").run()
    next(button for button in app.button if button.label == "🚀 Mulai Quiz Sekarang").click().run()

    assert any(questions[0]["question"] in entry.value for entry in app.markdown)
    app.radio(key="question_0").set_value("A").run()
    next(button for button in app.button if button.label == "Next →").click().run()

    assert any(questions[1]["question"] in entry.value for entry in app.markdown)
    app.radio(key="question_1").set_value("A").run()
    next(button for button in app.button if button.label == "🏁 Finish Quiz").click().run()

    assert not app.exception
    metrics = {entry.label: entry.value for entry in app.metric}
    assert metrics["📊 Skor Anda"] == "1/2"
    assert metrics["📈 Persentase"] == "50.0%"


def test_empty_question_bank_shows_help_without_start_button(tmp_path, monkeypatch):
    (tmp_path / "questions.json").write_text("[]", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    app = AppTest.from_file(APP_PATH).run()
    app.sidebar.radio[0].set_value("📚 Mulai Quiz").run()

    assert not app.exception
    assert any("Tidak ada soal tersedia" in entry.value for entry in app.error)
    assert all(button.label != "🚀 Mulai Quiz Sekarang" for button in app.button)
