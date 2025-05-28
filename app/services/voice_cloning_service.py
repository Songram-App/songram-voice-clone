import os
import uuid
from app.models.openvoice_model import OpenVoiceModel

class VoiceCloningService:
    def __init__(self, checkpoints_dir, device, output_dir):
        """Initialize the voice cloning service with OpenVoice model."""
        self.checkpoints_dir = checkpoints_dir
        self.device = device
        self.output_dir = output_dir
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize the OpenVoice model
        self.openvoice_model = OpenVoiceModel(checkpoints_dir, device)
        print(f"Voice Cloning Service initialized with OpenVoice on device: {device}")

    def clone_voice_and_synthesize(self, reference_audio_path, lyrics, target_language='en', speaker=None):
        """
        Clone voice from reference audio and synthesize speech using OpenVoice V2 and MeloTTS.
        
        Args:
            reference_audio_path: Path to the reference audio file
            lyrics: Text to be synthesized
            target_language: Target language for synthesis (default: 'en')
            speaker: Optional speaker ID (not used with OpenVoice)
            
        Returns:
            Path to the synthesized audio file
        """
        # Generate a unique file name for the output
        unique_filename = f"{uuid.uuid4()}.wav"
        output_audio_path = os.path.join(self.output_dir, unique_filename)
        
        try:
            print(f"Processing reference audio: {reference_audio_path}")
            
            # Extract speaker embedding from reference audio
            speaker_embedding = self.openvoice_model.extract_speaker_embedding(reference_audio_path)
            
            # Use 'en-newest' as default base speaker for English, or match language
            base_speaker_key = 'en-newest' if target_language.lower().startswith('en') else target_language.lower()
            
            # Synthesize and convert
            self.openvoice_model.synthesize_audio(
                lyrics,
                speaker_embedding,
                output_audio_path,
                language=target_language.upper(),
                base_speaker_key=base_speaker_key
            )
            
            print(f"Voice cloning and synthesis completed successfully")
            print(f"Audio file saved to: {output_audio_path}")
            
            return output_audio_path
            
        except Exception as e:
            print(f"Error in voice cloning and synthesis: {e}")
            raise