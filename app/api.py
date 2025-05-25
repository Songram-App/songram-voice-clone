from flask import Flask, request, jsonify
from app.services.voice_cloning_service import VoiceCloningService
import os

app = Flask(__name__)

# Configure the output directory for saving reference audio files
app.config['OUTPUT_DIR'] = 'app/output'

# Initialize the VoiceCloningService with configuration
voice_cloning_service = VoiceCloningService(
    checkpoints_dir=app.config['CHECKPOINTS_DIR'],
    device=app.config['DEVICE'],
    output_dir=app.config['OUTPUT_DIR']
)

@app.route('/clone-voice', methods=['POST'])
def clone_voice():
    if 'reference_voice' not in request.files or 'lyrics' not in request.form or 'language' not in request.form:
        return jsonify({'error': 'Reference voice file, lyrics, and target language are required.'}), 400

    reference_voice = request.files['reference_voice']
    lyrics = request.form['lyrics']
    target_language = request.form['language']

    # Save the uploaded reference voice to a temporary file
    reference_audio_path = os.path.join(app.config['OUTPUT_DIR'], 'reference.wav')
    os.makedirs(app.config['OUTPUT_DIR'], exist_ok=True)
    reference_voice.save(reference_audio_path)

    try:
        audio_file_path = voice_cloning_service.clone_voice_and_synthesize(
            reference_audio_path, lyrics, target_language
        )
        return jsonify({'audio_file_path': audio_file_path}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)