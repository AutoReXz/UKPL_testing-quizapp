# Quiz App Testing Project

This Software Quality Testing coursework uses a Streamlit quiz app for white-box and black-box testing. The app reads questions from JSON, scores submitted answers, and displays results.

## Run the Quiz

From the repository root, create and activate a Python virtual environment and then run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run streamlit_quiz_app.py
```

Open the local URL printed by Streamlit. The bundled [questions.json](questions.json) supplies the sample quiz questions.

## Run the Tests

Install pytest into the same environment and run the tests from the repository root:

```bash
python -m pip install pytest
python -m pytest blackbox whitebox
```

| Test area | What it covers |
| --- | --- |
| [Black-box tests](blackbox/) | Quiz scoring and empty question-bank checks through the Streamlit interface. |
| [White-box tests](whitebox/) | Control-flow and independent-path exercises for selected quiz functions. |

See the [black-box notes](blackbox/blackbox_documentation.md) for the current scenarios and planned checks. The [white-box notes](whitebox/whitebox_documentation.md) describe the scenarios. The flow graphs cover [loading questions](whitebox/flowgraph_load_questions.png) and [presenting the quiz](whitebox/flowgraph_show_quiz_question.png).
