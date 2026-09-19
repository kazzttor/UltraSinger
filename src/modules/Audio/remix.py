"""Stem remixing for optional transposed karaoke output."""

import os

import librosa
import numpy as np
import soundfile as sf

from modules.Audio.change_pitch import change_pitch


STEMS = ("vocals", "drums", "bass", "other")


def _mix_stems(paths: list[str], output_file: str) -> str:
    """Mix aligned stems without changing their common duration."""
    loaded = [librosa.load(path, sr=None, mono=False) for path in paths]
    sample_rate = loaded[0][1]
    if any(rate != sample_rate for _, rate in loaded):
        raise ValueError("All Demucs stems must use the same sample rate")
    channels = max(1 if audio.ndim == 1 else audio.shape[0] for audio, _ in loaded)
    length = min(audio.shape[-1] for audio, _ in loaded)
    mix = np.zeros((channels, length), dtype=np.float32)
    for audio, _ in loaded:
        if audio.ndim == 1:
            audio = np.repeat(audio[np.newaxis, :], channels, axis=0)
        elif audio.shape[0] < channels:
            audio = np.repeat(audio, channels, axis=0)
        mix += audio[:, :length]
    mix /= max(len(loaded), 1)
    sf.write(output_file, mix.T, sample_rate)
    return output_file


def create_transposed_instrumental(
    stems_dir: str, output_file: str, semitones: int
) -> str:
    """Keep drums unchanged and transpose bass/other before remixing."""
    if semitones == 0:
        return _mix_stems(
            [os.path.join(stems_dir, name + ".wav") for name in ("drums", "bass", "other")],
            output_file,
        )

    shifted_dir = os.path.join(stems_dir, "transposed")
    os.makedirs(shifted_dir, exist_ok=True)
    bass = change_pitch(
        os.path.join(stems_dir, "bass.wav"),
        semitones,
        os.path.join(shifted_dir, "bass.wav"),
    )
    other = change_pitch(
        os.path.join(stems_dir, "other.wav"),
        semitones,
        os.path.join(shifted_dir, "other.wav"),
    )
    return _mix_stems([os.path.join(stems_dir, "drums.wav"), bass, other], output_file)
