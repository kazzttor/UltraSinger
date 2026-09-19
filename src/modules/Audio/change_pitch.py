"""Audio pitch shifting helpers."""

import librosa
import soundfile as sf


def change_pitch(audio_file: str, steps: int, output_file: str | None = None) -> str:
    """Write a pitch-shifted copy and return its path.

    The input is never overwritten.  Keeping the source intact is required when
    an original and a transposed karaoke version are generated in one run.
    """
    destination = output_file or audio_file
    samples, sample_rate = librosa.load(audio_file, sr=None, mono=False)
    shifted = librosa.effects.pitch_shift(samples, sr=sample_rate, n_steps=steps)
    sf.write(destination, shifted.T if shifted.ndim > 1 else shifted, sample_rate)
    return destination
