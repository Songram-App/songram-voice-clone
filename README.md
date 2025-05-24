# OpenVoice REST API

This project provides a REST API for voice cloning using the OpenVoice V2 functionality. The API allows users to send a reference voice clip and a string of lyrics, which will be synthesized into an audio file using the cloned voice.

## Project Structure

```
openvoice-rest-api
├── app
│   ├── __init__.py
│   ├── api.py                # Defines the Flask REST API endpoints
│   ├── models
│   │   ├── __init__.py
│   │   └── openvoice_model.py # Implementation of the OpenVoice model
│   ├── services
│   │   ├── __init__.py
│   │   └── voice_cloning_service.py # Logic for voice cloning and audio synthesis
│   └── utils
│       ├── __init__.py
│       └── file_utils.py     # Utility functions for file operations
├── checkpoints                # Directory for model checkpoints
├── Dockerfile                 # Instructions to build the Docker image
├── requirements.txt           # Python dependencies
├── config.py                  # Configuration settings
└── README.md                  # Project documentation
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd openvoice-rest-api
   ```

2. **Install Dependencies**
   It is recommended to use a virtual environment. You can create one using `venv` or `conda`.

   ```bash
   pip install -r requirements.txt
   ```

3. **Model Checkpoints**
   Place the necessary model checkpoints in the `checkpoints` directory.

4. **Run the API**
   You can run the API using Flask. Make sure to set the `FLASK_APP` environment variable to `app.api`.

   ```bash
   export FLASK_APP=app.api
   flask run
   ```

## API Usage

### Endpoint

- **POST /synthesize**

#### Request

- **Body**: 
  - `reference_audio`: (file) The reference voice clip to clone.
  - `lyrics`: (string) The lyrics to be read by the cloned voice.

#### Response

- **200 OK**: Returns the path to the synthesized audio file.
- **400 Bad Request**: If the request is malformed or missing required fields.

## Docker Instructions

To build and run the Docker container:

1. **Build the Docker Image**
   ```bash
   docker build -t openvoice-rest-api .
   ```

2. **Run the Docker Container**
   ```bash
   docker run -p 5000:5000 openvoice-rest-api
   ```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.