# Use the official Python image.
FROM python:3.12

# Set the working directory in the container.
WORKDIR /usr/src

# Copy only the requirements.txt file initially.
COPY requirements.txt .

# Install system dependencies required by your project.
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

# Setup a virtual environment in the container and activate it.
# This ensures that all Python packages installed with pip are contained within this environment.
RUN python -m venv /usr/src/venv
ENV PATH="/usr/src/venv/bin:$PATH"

# Install Python dependencies in the virtual environment.
RUN pip install --no-cache-dir -r requirements.txt

# After the dependencies have been installed, copy the rest of the application code.
# This line should be placed just before the command to start your application.
# It ensures that changes in your application code do not invalidate the cached layers of installed dependencies.
COPY . .

# Launch the application using the virtual environment's Python interpreter.
CMD ["python", "./consumeStream.py"]
