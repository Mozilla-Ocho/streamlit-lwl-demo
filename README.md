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
# the api key used for chat completion inference calls at openai.
# if not present, the UI will ask for it each time.
openai_api_key=''

# set true in local dev, set true for deployed app
bypass_google_auth=false

# whether to show prompts and inference response details in a debug area
show_debug_area=true

# in the deployed app, this is a json-format string of the google oauth client secret
google_client_json_secret_raw='''...'''

# in deployed app, a secret value for the auth cookie. 
cookie_key='...'

# redirect_uri is not a secret, but i'm not sure where else to set environment config
redirect_uri='https://learn-with-llms-demo.streamlit.app/'
```

Finally, to run the app:

```bash
streamlit run app.py
```

