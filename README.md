# installation

Make sure you have python (from 3.8 to 3.12) installed. I recommend virtual environments to manage dependencies.

To create a virtual environment, run the following command:

```bash
python3 -m venv venv
```

To activate the virtual environment, run the following command:

```bash
source env/bin/activate
```

To install the dependencies, run the following command:

```bash
pip install -r requirements.txt
```

Most of those deps are from the streamlit package.

When you want to return to a normal shell, run the following command:

```bash
deactivate
```

# running the app

To run the app, run the following command:

```bash
source venv/bin/activate # if using venv, and you haven't already activated the virtual environment
streamlit run app.py
```

