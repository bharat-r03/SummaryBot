from kokoro import KPipeline
import torch


def text_to_audio(script_text: str, speaker_voice: str, lang_code: str = "a") -> torch.Tensor:
    pipeline = KPipeline(lang_code=lang_code)
    generator = pipeline(script_text, voice=speaker_voice)
    full_audio = torch.tensor([])

    for _, _, audio in generator:
        full_audio = torch.cat((full_audio, audio))

    return full_audio