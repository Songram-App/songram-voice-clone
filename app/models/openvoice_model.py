import sys
import os
import torch
import soundfile as sf
from openvoice import se_extractor
from openvoice.api import ToneColorConverter
from melo.api import TTS
from pydub import AudioSegment

class OpenVoiceModel:
    def __init__(self, checkpoints_dir, device='cuda'):
        self.device = device
        self.checkpoints_dir = checkpoints_dir
        self.converter_dir = os.path.join(checkpoints_dir, 'converter')
        self.base_speakers_dir = os.path.join(checkpoints_dir, 'base_speakers/ses')
        print(f"Loading tone color converter from {self.converter_dir}/checkpoint.pth")
        self.tone_color_converter = ToneColorConverter(
            os.path.join(self.converter_dir, 'config.json'),
            device=device
        )
        self.tone_color_converter.load_ckpt(os.path.join(self.converter_dir, 'checkpoint.pth'))
        print("OpenVoice V2 model initialized successfully")

    def extract_speaker_embedding(self, reference_audio_path):
        print(f"Extracting speaker embedding from {reference_audio_path}")
        target_se, _ = se_extractor.get_se(reference_audio_path, self.tone_color_converter, vad=True)
        print(f"Speaker embedding extracted successfully, shape: {target_se.shape}")
        return target_se

    def synthesize_audio(self, text, target_se, output_path, language='EN', base_speaker_key='en-newest', speed=1.0):
        print(f"Synthesizing text: '{text}' using MeloTTS and OpenVoice V2 tone color conversion")
        tts = TTS(language=language, device=self.device)
        speaker_ids = tts.hps.data.spk2id
        normalized_key = base_speaker_key.lower().replace('_', '-')
        available_embeddings = [os.path.splitext(f)[0] for f in os.listdir(self.base_speakers_dir) if f.endswith('.pth')]
        if normalized_key not in available_embeddings:
            if language.lower().startswith('en'):
                fallback = 'en-newest'
                if fallback in available_embeddings:
                    normalized_key = fallback
                else:
                    normalized_key = available_embeddings[0]
            else:
                normalized_key = available_embeddings[0]
        if normalized_key in speaker_ids:
            speaker_id = speaker_ids[normalized_key]
        else:
            speaker_id = list(speaker_ids.values())[0]
        base_audio_path = output_path + '.base.wav'
        tts.tts_to_file(text, speaker_id, base_audio_path, speed=speed)
        source_se_path = os.path.join(self.base_speakers_dir, f'{normalized_key}.pth')
        if not os.path.exists(source_se_path):
            raise FileNotFoundError(f"Base speaker embedding not found: {source_se_path}")
        source_se = torch.load(source_se_path, map_location=self.device)
        self.tone_color_converter.convert(
            audio_src_path=base_audio_path,
            src_se=source_se,
            tgt_se=target_se,
            output_path=output_path,
            message="@MyShell"
        )
        try:
            audio = AudioSegment.from_wav(output_path)
            change_in_dBFS = -1.0 - audio.max_dBFS
            normalized_audio = audio.apply_gain(change_in_dBFS)
            normalized_audio.export(output_path, format="wav")
            print(f"Audio normalized to -1 dBFS: {output_path}")
        except Exception as e:
            print(f"Warning: Could not normalize audio volume: {e}")
        print(f"Audio saved to {output_path}")
        return output_path