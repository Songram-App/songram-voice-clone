from flask import current_app
import os
from melo.api import TTS
from openvoice.api import ToneColorConverter

class VoiceCloningService:
    def __init__(self):
        # Initialize MeloTTS for base speaker synthesis
        self.base_tts = TTS(
            os.path.join(current_app.config['CHECKPOINTS_DIR'], 'base_speakers'),
            device=current_app.config['DEVICE']
        )

        # Initialize ToneColorConverter for voice cloning
        self.tone_color_converter = ToneColorConverter(
            os.path.join(current_app.config['CHECKPOINTS_DIR'], 'converter/config.json'),
            device=current_app.config['DEVICE']
        )
        self.tone_color_converter.load_ckpt(
            os.path.join(current_app.config['CHECKPOINTS_DIR'], 'converter/checkpoint.pth')
        )

    def clone_voice_and_synthesize(self, reference_audio_path, lyrics, target_language):
        # Extract speaker embedding from reference audio
        speaker_embedding = self.tone_color_converter.extract_speaker_embedding(reference_audio_path)

        # Generate audio using MeloTTS with the cloned voice
        output_audio_path = os.path.join(current_app.config['OUTPUT_DIR'], 'output.wav')
        self.base_tts.tts(
            text=lyrics,
            output_path=output_audio_path,
            speaker_embedding=speaker_embedding,
            language=target_language
        )

        return output_audio_path