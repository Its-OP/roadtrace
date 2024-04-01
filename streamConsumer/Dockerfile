FROM python:3.12
WORKDIR /usr/src
COPY . .

# Install all required dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Launch the application
CMD ["python", "./consumeStream.py"]
