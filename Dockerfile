FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install git for installing MeloTTS
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install unidic and download the dictionary
RUN pip install unidic && python -m unidic download

# Clone and install OpenVoice V2
RUN git clone https://github.com/myshell-ai/OpenVoice.git /tmp/OpenVoice && \
    pip install /tmp/OpenVoice && \
    rm -rf /tmp/OpenVoice

# Copy the application code
COPY app ./app
COPY checkpoints ./checkpoints
COPY config.py .

# Copy the MeloTTS directory into the Docker image
COPY MeloTTS /app/MeloTTS

# Install MeloTTS locally
RUN pip install -e /app/MeloTTS

# Expose the port the app runs on
EXPOSE 6000

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]