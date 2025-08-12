from kokoro import KPipeline
import torch
import torchaudio
import soundfile as sf
import io


def text_to_audio(script_text: str, speaker_voice: str, lang_code: str = "a") -> torch.Tensor:
    pipeline = KPipeline(lang_code=lang_code)
    generator = pipeline(script_text, voice=speaker_voice)
    full_audio = torch.tensor([])

    for _, _, audio in generator:
        full_audio = torch.cat((full_audio, audio))

    audio_buffer = io.BytesIO()
    audio_buffer.name = "test.wav"

    sf.write(audio_buffer, full_audio, samplerate=24000)
    audio_buffer.seek(0)

    return audio_buffer.read()