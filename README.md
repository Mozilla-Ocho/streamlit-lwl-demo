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

Create a file `.streamlit/secrets.toml` with the following content:

```toml
# the api key used for chat completion inference calls at openai, e.g. 'sk-...'
# if left empty the UI will ask for it each time in the form. if populated, the query_auth_secret is present, it will be used automatically w/o a user input.
openai_api_key=''

# query string param 'a' must match this which activates usage of the api key above if present.
query_auth_secret='...'

# whether to show prompts and inference response details in a debug area
show_debug_area=true

```

Finally, to run the app:

```bash
streamlit run app.py
```

