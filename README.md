# Learning with LLMs concept explorer Streamlit app

This small application is a space to explore use cases for creating personalized learning materials based on arbitrary source material from, for example, PDFs and web pages.

The app is built using the Streamlit framework, which is a Python library for creating web applications with minimal effort.

# Live demo

Deployed on Streamlit community cloud at: https://learn-with-llms-demo.streamlit.app/

# Local installation

Make sure you have python (from 3.8 to 3.12) installed. I recommend virtual environments to manage dependencies.

To create a new virtual environment, run the following command in the repo root:

```bash
python3 -m venv venv
```

To activate the virtual environment, run the following command:

```bash
source env/bin/activate
```

(Whenever you want to return to a normal shell, run `deactivate`.)

To install the dependencies, run the following command:

```bash
pip install -r requirements.txt
```

Most of those deps are from the streamlit package.

Finally, to run the app:

```bash
streamlit run app.py
```

