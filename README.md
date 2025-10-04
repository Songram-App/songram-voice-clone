# OpenVoice REST API

This project provides a REST API for instant voice cloning using OpenVoice V2 and MeloTTS. The API allows users to send a reference voice clip and lyrics, and returns a synthesized audio file in the cloned voice.

## Project Structure

```
openvoice-rest-api
├── app
│   ├── __init__.py
│   ├── api.py                # Flask REST API endpoints
│   ├── models
│   │   ├── __init__.py
│   │   └── openvoice_model.py # OpenVoice V2 + MeloTTS integration
│   ├── services
│   │   ├── __init__.py
│   │   └── voice_cloning_service.py # Voice cloning and synthesis logic
│   └── utils
│       ├── __init__.py
│       └── file_utils.py     # File utility functions
├── checkpoints                # Model checkpoints (see below)
│   ├── base_speakers/ses/*.pth
│   └── converter/{checkpoint.pth, config.json}
├── Dockerfile                 # Docker build instructions
├── requirements.txt           # Python dependencies
├── config.py                  # Configuration settings
├── MeloTTS/                   # MeloTTS source (as a submodule or folder)
└── README.md                  # Project documentation
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd openvoice-rest-api
   ```

2. **Model Checkpoints**
   - Download the OpenVoice V2 checkpoints as described in the [OpenVoice repo](https://github.com/myshell-ai/OpenVoice).
   - Place them in the `checkpoints` directory as follows:
     - `checkpoints/base_speakers/ses/*.pth` (e.g., `en-us.pth`, `en-newest.pth`, etc.)
     - `checkpoints/converter/checkpoint.pth` and `checkpoints/converter/config.json`

3. **Build and Run with Docker**
   ```bash
   docker build -t openvoice-rest-api .
   docker run -p 6000:6000 \
     -v $(pwd)/checkpoints:/app/checkpoints \
     -v $(pwd)/app/output:/app/app/output \
     openvoice-rest-api
   ```

   The API will be available at `http://localhost:6000`.

## API Usage

### Endpoint

- **POST /clone-voice**

#### Request (multipart/form-data)
- `reference_voice`: (file) The reference voice clip to clone (WAV, MP3, FLAC, OGG).
- `lyrics`: (string) The lyrics/text to be synthesized.
- `language`: (string, optional) Target language (e.g., `en`, `es`, `fr`, `zh`, `jp`, `kr`). Defaults to `en`.
- `speaker`: (string, optional) Base speaker key (e.g., `en-us`, `en-newest`). If not provided, a default is chosen.

#### Example (using curl)
```bash
curl -X POST http://localhost:6000/clone-voice \
  -F "reference_voice=@/path/to/voice.wav" \
  -F "lyrics=Your lyrics here" \
  -F "language=en" \
  -F "speaker=en-us"
```

#### Response
- **200 OK**: JSON with `audio_file_path`, `relative_path`, and metadata.
- **400 Bad Request**: If required fields are missing or invalid.
- **500 Internal Server Error**: On processing errors.

## Features
- Uses OpenVoice V2 for instant, multi-lingual, zero-shot voice cloning.
- Uses MeloTTS for high-quality base TTS in multiple languages.
- Reference audio is denoised and normalized for best results.
- Output audio is normalized to -1 dBFS for consistent loudness.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Maintainers

This project is actively maintained by [@gbudjeakp](https://github.com/gbudjeakp).
