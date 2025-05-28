from flask import Flask, request, jsonify
from app.services.voice_cloning_service import VoiceCloningService
import os
import torch

app = Flask(__name__)

# Configure the output directory for saving reference audio files
app.config['OUTPUT_DIR'] = 'app/output'

# Configure the checkpoints directory
app.config['CHECKPOINTS_DIR'] = 'checkpoints'

# Configure the device (CPU or GPU)
app.config['DEVICE'] = 'cuda' if torch.cuda.is_available() else 'cpu'

# Initialize the VoiceCloningService with configuration
voice_cloning_service = VoiceCloningService(
    checkpoints_dir=app.config['CHECKPOINTS_DIR'],
    device=app.config['DEVICE'],
    output_dir=app.config['OUTPUT_DIR']
)

@app.route('/clone-voice', methods=['POST'])
def clone_voice():
    if 'reference_voice' not in request.files or 'lyrics' not in request.form:
        return jsonify({'error': 'Reference voice file and lyrics are required.'}), 400

    reference_voice = request.files['reference_voice']
    lyrics = request.form['lyrics']
    
    # Language is optional, defaults to English
    target_language = request.form.get('language', 'en')
    
    # Speaker parameter is retained for backwards compatibility but not used
    speaker = request.form.get('speaker', None)

    # Validate reference audio
    if not reference_voice.filename.lower().endswith(('.wav', '.mp3', '.flac', '.ogg')):
        return jsonify({'error': 'Reference voice file must be a valid audio format (.wav, .mp3, .flac, .ogg)'}), 400
    
    # Create output directory if it doesn't exist
    os.makedirs(app.config['OUTPUT_DIR'], exist_ok=True)
    
    # Save the uploaded reference voice to a temporary file
    reference_audio_path = os.path.join(app.config['OUTPUT_DIR'], 'reference_input.wav')
    reference_voice.save(reference_audio_path)
    
    # Check if the file is empty or corrupted
    try:
        import soundfile as sf
        data, samplerate = sf.read(reference_audio_path)
        duration = len(data) / samplerate
        if duration < 0.5:
            return jsonify({'error': f'Reference audio is too short ({duration:.2f}s). Please provide at least 1-2 seconds of clear speech.'}), 400
    except Exception as e:
        return jsonify({'error': f'Error validating reference audio: {str(e)}'}), 400

    try:
        print(f"Processing request: Language={target_language}, Speaker={speaker}, Audio file size={os.path.getsize(reference_audio_path)} bytes")
        audio_file_path = voice_cloning_service.clone_voice_and_synthesize(
            reference_audio_path, lyrics, target_language, speaker
        )
        
        # Get relative path for response
        relative_path = os.path.relpath(audio_file_path, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        return jsonify({
            'audio_file_path': audio_file_path,
            'relative_path': relative_path,
            'message': 'Voice cloning completed successfully',
            'reference_audio_duration': f'{duration:.2f} seconds',
            'language': target_language
        }), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)