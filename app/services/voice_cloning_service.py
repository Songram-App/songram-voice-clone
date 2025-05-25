import os
from MeloTTS.melo.api import TTS

class VoiceCloningService:
    def __init__(self, checkpoints_dir, device, output_dir):
        self.checkpoints_dir = checkpoints_dir
        self.device = device
        self.output_dir = output_dir

    def clone_voice_and_synthesize(self, reference_audio_path, lyrics, target_language, speaker):
        # Initialize MeloTTS for the specified language and device
        tts = TTS(language=target_language, device=self.device)

        # Extract speaker ID
        speaker_ids = tts.hps.data.spk2id
        if speaker not in speaker_ids:
            raise ValueError(f"Speaker '{speaker}' not found for language '{target_language}'.")

        # Generate audio using MeloTTS
        output_audio_path = os.path.join(self.output_dir, 'output.wav')
        tts.tts_to_file(lyrics, speaker_ids[speaker], output_audio_path)

        return output_audio_path