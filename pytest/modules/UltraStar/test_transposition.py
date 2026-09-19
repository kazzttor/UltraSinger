from pathlib import Path

from src.modules.Ultrastar.transposition import transpose_ultrastar_file


def test_transpose_ultrastar_notes_and_media(tmp_path: Path):
    source = tmp_path / "song.txt"
    destination = tmp_path / "song-transposed.txt"
    source.write_text(
        "#MP3:song.mp3\n"
        "#AUDIO:song.mp3\n"
        ": 10 4 3 Hello world\n"
        "* 20 2 -1 Gold\n"
        "R 30 2 4 Spoken\n"
        "E\n",
        encoding="utf-8",
    )

    transpose_ultrastar_file(source, destination, 2, " [+2 semitones]")

    assert destination.read_text(encoding="utf-8") == (
        "#MP3:song [+2 semitones].mp3\n"
        "#AUDIO:song [+2 semitones].mp3\n"
        ": 10 4 5 Hello world\n"
        "* 20 2 1 Gold\n"
        "R 30 2 4 Spoken\n"
        "E\n"
    )
