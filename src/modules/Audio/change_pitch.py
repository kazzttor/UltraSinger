import librosa

def change_pitch(audio_file, steps): # Added the missing change_pitch function
  """
  Changes the pitch of an audio file.

  Args:
    audio_file: Path to the audio file.
    steps: Number of steps to shift the pitch.
  """
  y, sr = librosa.load(audio_file)
  y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=steps)
  sf.write(audio_file, y_shifted, sr)
  print(f"Tom do arquivo {audio_file} alterado em {steps} semitons.")
