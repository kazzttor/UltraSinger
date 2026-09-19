"""Generate karaoke videos from an UltraStar TXT and an audio track."""

import re
import shutil
import subprocess
from pathlib import Path


def _ass_time(seconds: float) -> str:
    seconds = max(0.0, seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, remainder = divmod(remainder, 60)
    whole = int(remainder)
    centiseconds = int(round((remainder - whole) * 100))
    if centiseconds == 100:
        whole += 1
        centiseconds = 0
    return f"{int(hours)}:{int(minutes):02d}:{whole:02d}.{centiseconds:02d}"


def ultrastar_to_ass(ultrastar_file: str, ass_file: str) -> str:
    """Convert note lines to timed ASS events using UltraStar's real timing."""
    tags = {}
    notes = []
    with open(ultrastar_file, encoding="utf-8") as source:
        for line in source:
            line = line.rstrip()
            if line.startswith("#") and ":" in line:
                key, value = line[1:].split(":", 1)
                tags[key.upper()] = value.strip()
            elif line.startswith((": ", "* ", "F ")) or line.startswith((":", "*", "F")):
                parts = line.split(maxsplit=4)
                if len(parts) >= 4:
                    try:
                        notes.append((int(parts[1]), int(parts[2]), parts[4] if len(parts) > 4 else ""))
                    except (ValueError, IndexError):
                        continue
    try:
        ultrastar_bpm = float(tags["BPM"].replace(",", "."))
    except (KeyError, ValueError) as error:
        raise ValueError("UltraStar file must contain a numeric #BPM") from error
    if ultrastar_bpm <= 0:
        raise ValueError("#BPM must be greater than zero")
    gap = float(tags.get("GAP", "0").replace(",", ".")) / 1000
    seconds_per_beat = 60 / (ultrastar_bpm * 4)
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Karaoke,Arial,64,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,1,0,1,2,1,2,80,80,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(ass_file, "w", encoding="utf-8") as destination:
        destination.write(header)
        for start, duration, text in notes:
            start_time = gap + start * seconds_per_beat
            end_time = gap + (start + duration) * seconds_per_beat
            text = re.sub(r"\{[^}]*\}", "", text).replace("\\", r"\\")
            destination.write(
                f"Dialogue: 0,{_ass_time(start_time)},{_ass_time(end_time)},Karaoke,,0,0,0,,{text}\n"
            )
    return ass_file


def generate_lyrics_video(
    ultrastar_file: str,
    audio_file: str,
    output_file: str,
    background: str | None = None,
    ffmpeg: str = "ffmpeg",
) -> str:
    """Render a lyrics video with FFmpeg and the generated ASS subtitles."""
    if shutil.which(ffmpeg) is None:
        raise RuntimeError("FFmpeg is required to generate a lyrics video")
    ass_file = str(Path(output_file).with_suffix(".ass"))
    ultrastar_to_ass(ultrastar_file, ass_file)
    source = background or "color=c=0x101018:s=1920x1080:r=30"
    input_args = ["-f", "lavfi", "-i", source] if not background else ["-stream_loop", "-1", "-i", background]
    subtitle_filter = ass_file.replace("\\", "/").replace(":", r"\:")
    command = [
        ffmpeg, "-y", *input_args, "-i", audio_file,
        "-vf", f"ass={subtitle_filter}",
        "-map", "0:v:0", "-map", "1:a:0", "-shortest",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", output_file,
    ]
    subprocess.run(command, check=True)
    return output_file
