import whisper
import torch

def get_mel_spectogram(audio_file_path: str) -> torch.Tensor:
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio_file_path)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram
    mel = whisper.log_mel_spectrogram(audio)
    return mel