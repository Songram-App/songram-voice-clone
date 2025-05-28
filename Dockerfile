FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install git and build tools for dependencies
RUN apt-get update && apt-get install -y git gcc g++ build-essential && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install unidic and download the dictionary
RUN pip install unidic && python -m unidic download

# Clone and install OpenVoice V2
RUN git clone https://github.com/myshell-ai/OpenVoice.git /tmp/OpenVoice && \
    cd /tmp/OpenVoice && \
    pip install -e . && \
    cd / && \
    # Install additional dependencies needed for OpenVoice
    pip install librosa torchaudio pyworld && \
    # Keep the source code for reference
    mkdir -p /app/OpenVoice && \
    cp -r /tmp/OpenVoice/* /app/OpenVoice/ && \
    rm -rf /tmp/OpenVoice

# Add OpenVoice to the Python path
ENV PYTHONPATH="/app/OpenVoice:$PYTHONPATH"

# Copy the application code
COPY app ./app
COPY checkpoints ./checkpoints
COPY config.py .

# Copy the MeloTTS directory into the Docker image
COPY MeloTTS /app/MeloTTS

# Install MeloTTS locally
RUN pip install -e /app/MeloTTS

# Download the required NLTK resource
RUN python -m nltk.downloader averaged_perceptron_tagger_eng

# Install Resemblyzer for speaker embedding extraction
RUN pip install resemblyzer

# Install ffmpeg for audio processing (required by whisper and OpenVoice)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Install noisereduce and pydub for audio denoising and normalization
RUN pip install noisereduce pydub

# Create the output directory
RUN mkdir -p /app/app/output && chmod 777 /app/app/output

# Expose the port the app runs on
EXPOSE 6000

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=6000"]