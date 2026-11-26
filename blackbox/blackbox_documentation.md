# Black-Box Test Scenarios

The tests open the quiz through Streamlit's app testing API and inspect the displayed result. Each test uses a temporary question file.

- **Mixed answers** — Start a two-question quiz, submit one correct and one incorrect answer, and verify the displayed score is `1/2` and the percentage is `50.0%`.
- **Empty question bank** — Open the quiz with an empty question file and verify that the app displays help and hides the start button.

Run these checks with `python -m pytest blackbox` from the repository root. The unit, load, and stress files are placeholders for future scenarios.
