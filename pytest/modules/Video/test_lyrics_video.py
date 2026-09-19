from pathlib import Path

from src.modules.Video.lyrics_video import ultrastar_to_ass


def test_ultrastar_to_ass_uses_real_bpm_and_gap(tmp_path: Path):
    source = tmp_path / "song.txt"
    destination = tmp_path / "song.ass"
    source.write_text(
        "#BPM:30\n#GAP:500\n: 4 8 3 Hello\nE\n",
        encoding="utf-8",
    )

    ultrastar_to_ass(str(source), str(destination))

    dialogue = next(line for line in destination.read_text(encoding="utf-8").splitlines()
                    if line.startswith("Dialogue:"))
    assert ",0:00:02.50,0:00:06.50," in dialogue
