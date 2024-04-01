FROM python:3.12
WORKDIR /usr/src

# Init venv and install all required dependencies
COPY requirements.txt .
RUN python -m venv /usr/src/.venv
RUN . /usr/src/.venv/bin/activate && pip install --no-cache-dir -r requirements.txt

COPY . .

# Launch the application
CMD ["/usr/src/.venv/bin/python", "app.py"]