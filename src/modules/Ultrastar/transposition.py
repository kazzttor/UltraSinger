"""UltraStar text transposition."""

import os

from modules.Ultrastar.ultrastar_txt import FILE_ENCODING, UltrastarTxtNoteTypeTag


NOTE_TYPES = tuple(note.value for note in UltrastarTxtNoteTypeTag)
MEDIA_TAGS = ("#MP3:", "#AUDIO:")


def _transposed_media_name(value: str, suffix: str) -> str:
    root, extension = os.path.splitext(value.strip())
    return f"{root}{suffix}{extension or '.mp3'}"


def transpose_ultrastar_file(
    input_file: str, output_file: str, semitones: int, audio_suffix: str | None = None
) -> str:
    """Copy an UltraStar file, shifting note pitches and optional media names."""
    if not isinstance(semitones, int):
        raise TypeError("semitones must be an integer")

    with open(input_file, "r", encoding=FILE_ENCODING) as source:
        lines = source.readlines()
    suffix = audio_suffix or f" [{semitones:+d} semitones]"
    result = []
    for line in lines:
        stripped = line.rstrip("\r\n")
        if audio_suffix and stripped.startswith(MEDIA_TAGS):
            tag, value = stripped.split(":", 1)
            result.append(f"{tag}:{_transposed_media_name(value, suffix)}\n")
            continue
        if stripped.startswith(NOTE_TYPES) and stripped[:1] in NOTE_TYPES:
            parts = stripped.split(maxsplit=4)
            if len(parts) >= 4 and parts[0] != "R" and parts[0] != "G":
                try:
                    parts[3] = str(int(parts[3]) + semitones)
                except ValueError:
                    pass
                stripped = " ".join(parts)
            result.append(stripped + "\n")
        else:
            result.append(line)
    with open(output_file, "w", encoding=FILE_ENCODING) as destination:
        destination.writelines(result)
    return output_file
