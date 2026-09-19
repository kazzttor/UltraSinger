"""UltraSinger uses AI to automatically create UltraStar song files"""

import copy
import getopt
import argparse
import os
import sys
import Levenshtein

from packaging import version

from modules import os_helper
from modules.Audio.denoise import denoise_vocal_audio
from modules.Audio.separation import separate_vocal_from_audio
from modules.Audio.change_pitch import change_pitch
from modules.Audio.vocal_chunks import (
    create_audio_chunks_from_transcribed_data,
    create_audio_chunks_from_ultrastar_data,
)
from modules.Audio.silence_processing import remove_silence_from_transcription_data, mute_no_singing_parts

from modules.Audio.convert_audio import convert_audio_to_mono_wav, convert_wav_to_mp3
from modules.Audio.youtube import (
    download_from_youtube,
)
from modules.Audio.change_pitch import change_pitch
from modules.console_colors import (
    ULTRASINGER_HEAD,
    blue_highlighted,
    gold_highlighted,
    red_highlighted,
    green_highlighted,
)
from modules.Midi.midi_creator import (
    create_midi_segments_from_transcribed_data,
    create_repitched_midi_segments_from_ultrastar_txt,
    create_midi_file,
)

from modules.Pitcher.pitcher import (
    get_pitch_with_crepe_file,
)
from modules.Pitcher.pitched_data import PitchedData
from modules.Speech_Recognition.TranscriptionResult import TranscriptionResult
from modules.Speech_Recognition.hyphenation import (
    hyphenate_each_word,
)
from modules.Speech_Recognition.Whisper import transcribe_with_whisper
from modules.Ultrastar import (
    ultrastar_writer,
)
from modules.Speech_Recognition.TranscribedData import TranscribedData
from modules.Ultrastar.ultrastar_score_calculator import Score, calculate_score_points
from modules.Ultrastar.ultrastar_txt import FILE_ENCODING, FormatVersion
from modules.Ultrastar.coverter.ultrastar_txt_converter import from_ultrastar_txt, \
    create_ultrastar_txt_from_midi_segments, create_ultrastar_txt_from_automation
from modules.Ultrastar.ultrastar_parser import parse_ultrastar_txt
from modules.common_print import print_support, print_help, print_version
from modules.os_helper import check_file_exists, get_unused_song_output_dir
from modules.plot import create_plots
from modules.musicbrainz_client import get_music_infos
from modules.sheet import create_sheet
from modules.ProcessData import ProcessData, ProcessDataPaths, MediaInfo
from modules.DeviceDetection.device_detection import check_gpu_support
from modules.Audio.bpm import get_bpm_from_file
from modules.Ultrastar.transposition import transpose_ultrastar_file
from modules.Video.lyrics_video import generate_lyrics_video

from Settings import Settings

settings = Settings()


def add_hyphen_to_data(
        transcribed_data: list[TranscribedData], hyphen_words: list[list[str]]
):
    """Add hyphen to transcribed data return new data list"""
    new_data = []

    for i, data in enumerate(transcribed_data):
        if not hyphen_words[i]:
            new_data.append(data)
        else:
            chunk_duration = data.end - data.start
            chunk_duration = chunk_duration / (len(hyphen_words[i]))

            next_start = data.start
            for j in enumerate(hyphen_words[i]):
                hyphenated_word_index = j[0]
                dup = copy.copy(data)
                dup.start = next_start
                next_start = data.end - chunk_duration * (
                        len(hyphen_words[i]) - 1 - hyphenated_word_index
                )
                dup.end = next_start
                dup.word = hyphen_words[i][hyphenated_word_index]
                dup.is_hyphen = True
                if hyphenated_word_index == len(hyphen_words[i]) - 1:
                    dup.is_word_end = True
                else:
                    dup.is_word_end = False
                new_data.append(dup)

    return new_data


def correct_words(recognized_words, word_list_file):
    """Docstring"""
    with open(word_list_file, "r", encoding="utf-8") as file:
        text = file.read()
    word_list = text.split()

    for i, rec_word in enumerate(recognized_words):
        if rec_word.word in word_list:
            continue

        closest_word = min(
            word_list, key=lambda x: Levenshtein.distance(rec_word.word, x)
        )
        print(recognized_words[i].word + " - " + closest_word)
        recognized_words[i].word = closest_word
    return recognized_words


def remove_unecessary_punctuations(transcribed_data: list[TranscribedData]) -> None:
    """Remove unecessary punctuations from transcribed data"""
    punctuation = ".,"
    for i, data in enumerate(transcribed_data):
        data.word = data.word.translate({ord(i): None for i in punctuation})


def run() -> tuple[str, Score, Score]:
    """The processing function of this program"""

    process_data = InitProcessData()

    process_data.process_data_paths.cache_folder_path = (
        os.path.join(settings.output_folder_path, "cache")
        if settings.cache_override_path is None
        else settings.cache_override_path
    )

    # Create process audio
    process_data.process_data_paths.processing_audio_path = CreateProcessAudio(process_data)

    # Audio transcription
    process_data.media_info.language = settings.language
    if not settings.ignore_audio:
        TranscribeAudio(process_data)

    # Create audio chunks
    if settings.create_audio_chunks:
        create_audio_chunks(process_data)

    # Pitch audio
    process_data.pitched_data = pitch_audio(process_data.process_data_paths)

    # Create Midi_Segments
    if not settings.ignore_audio:
        process_data.midi_segments = create_midi_segments_from_transcribed_data(process_data.transcribed_data,
                                                                                process_data.pitched_data)
    else:
        process_data.midi_segments = create_repitched_midi_segments_from_ultrastar_txt(process_data.pitched_data,
                                                                                       process_data.parsed_file)

    # Create plot
    if settings.create_plot:
        create_plots(process_data, settings.output_folder_path)

    # Create Ultrastar txt
    accurate_score, simple_score, ultrastar_file_output = CreateUltraStarTxt(process_data)

    # Create Midi
    if settings.create_midi:
        create_midi_file(process_data.media_info.bpm, settings.output_folder_path, process_data.midi_segments,
                         process_data.basename)

    # Sheet music
    create_sheet(process_data.midi_segments, settings.output_folder_path,
                 process_data.process_data_paths.cache_folder_path, settings.musescore_path, process_data.basename,
                 process_data.media_info)

    # Cleanup
    if not settings.keep_cache:
        remove_cache_folder(process_data.process_data_paths.cache_folder_path)

    # Print Support
    print_support()
    return ultrastar_file_output, simple_score, accurate_score


def create_audio_chunks(process_data):
    if not settings.ignore_audio:
        create_audio_chunks_from_transcribed_data(
            process_data.process_data_paths,
            process_data.transcribed_data)
    else:
        create_audio_chunks_from_ultrastar_data(
            process_data.process_data_paths,
            process_data.parsed_file
        )


def InitProcessData():
    settings.input_file_is_ultrastar_txt = settings.input_file_path.endswith(".txt")
    if settings.input_file_is_ultrastar_txt:
        # Parse Ultrastar txt
        (
            basename,
            settings.output_folder_path,
            audio_file_path,
            ultrastar_class,
        ) = parse_ultrastar_txt(settings.input_file_path, settings.output_folder_path)
        process_data = from_ultrastar_txt(ultrastar_class)
        process_data.basename = basename
        process_data.process_data_paths.audio_output_file_path = audio_file_path
        # todo: ignore transcribe
        settings.ignore_audio = True

    elif settings.input_file_path.startswith("https:"):
        # Youtube
        print(f"{ULTRASINGER_HEAD} {gold_highlighted('full automatic mode')}")
        process_data = ProcessData()
        (
            process_data.basename,
            settings.output_folder_path,
            process_data.process_data_paths.audio_output_file_path,
            process_data.media_info,
        ) = download_from_youtube(settings.input_file_path, settings.output_folder_path)
    else:
        # Audio File
        print(f"{ULTRASINGER_HEAD} {gold_highlighted('full automatic mode')}")
        process_data = ProcessData()
        (
            process_data.basename,
            settings.output_folder_path,
            process_data.process_data_paths.audio_output_file_path,
            process_data.media_info,
        ) = infos_from_audio_input_file()
    return process_data


def TranscribeAudio(process_data):
    transcription_result = transcribe_audio(process_data.process_data_paths.cache_folder_path,
                                            process_data.process_data_paths.processing_audio_path)

    if process_data.media_info.language is None:
        process_data.media_info.language = transcription_result.detected_language

    process_data.transcribed_data = transcription_result.transcribed_data

    # Hyphen
    remove_unecessary_punctuations(process_data.transcribed_data)
    if settings.hyphenation:
        hyphen_words = hyphenate_each_word(process_data.media_info.language, process_data.transcribed_data)

        if hyphen_words is not None:
            process_data.transcribed_data = add_hyphen_to_data(process_data.transcribed_data, hyphen_words)

    process_data.transcribed_data = remove_silence_from_transcription_data(
        process_data.process_data_paths.processing_audio_path, process_data.transcribed_data
    )


def CreateUltraStarTxt(process_data: ProcessData):
    song_folder = os_helper.create_folder(
        os.path.join(settings.output_folder_path, process_data.basename)
    )
    if settings.create_karaoke:
        karaoke_output_path = os.path.join(song_folder, f'{process_data.basename}.mp3')
        convert_wav_to_mp3(process_data.process_data_paths.instrumental_audio_file_path, karaoke_output_path)
        settings.audio_output_file_path = karaoke_output_path

    ultrastar_file_output = create_ultrastar_txt_from_automation(
        process_data.basename,
        song_folder,
        process_data.midi_segments,
        process_data.media_info,
        settings.format_version,
        settings.create_karaoke,
        settings.APP_VERSION,
    )
    if settings.changetone:
        transposed_wav = os.path.join(
            process_data.process_data_paths.cache_folder_path,
            "remixes",
            f"{process_data.basename}_{settings.changetone}.wav",
        )
        if not os.path.exists(transposed_wav):
            raise FileNotFoundError(f"Transposed remix was not created: {transposed_wav}")
        transposed_basename = f"{process_data.basename} [{settings.changetone:+d} semitones]"
        transposed_audio = os.path.join(song_folder, transposed_basename + ".mp3")
        convert_wav_to_mp3(transposed_wav, transposed_audio)
        transpose_ultrastar_file(
            ultrastar_file_output,
            os.path.join(song_folder, transposed_basename + ".txt"),
            settings.changetone,
            audio_suffix=f" [{settings.changetone:+d} semitones]",
        )
    accurate_score, simple_score = calculate_score_points(process_data.pitched_data, process_data.transcribed_data)

    return accurate_score, simple_score, ultrastar_file_output


def CreateProcessAudio(process_data) -> str:
    # Set processing audio to cache file
    process_data.process_data_paths.processing_audio_path = os.path.join(
        process_data.process_data_paths.cache_folder_path, process_data.basename + ".wav"
    )
    os_helper.create_folder(process_data.process_data_paths.cache_folder_path)

    # Separate vocal from audio
    audio_separation_folder_path = separate_vocal_from_audio(
        process_data.process_data_paths.cache_folder_path,
        process_data.process_data_paths.audio_output_file_path,
        settings.use_separated_vocal,
        settings.create_karaoke,
        settings.pytorch_device,
        settings.demucs_model,
        settings.skip_cache_vocal_separation,
        settings.changetone or 0,
    )
    process_data.process_data_paths.vocals_audio_file_path = os.path.join(audio_separation_folder_path, "vocals.wav")
    process_data.process_data_paths.instrumental_audio_file_path = os.path.join(audio_separation_folder_path, "no_vocals.wav")
    if settings.changetone:
        remix_name = os.path.splitext(os.path.basename(
            process_data.process_data_paths.audio_output_file_path
        ))[0]
        process_data.process_data_paths.instrumental_audio_file_path = os.path.join(
            process_data.process_data_paths.cache_folder_path,
            "remixes",
            f"{remix_name}_original.wav",
        )

    if settings.use_separated_vocal:
        input_path = process_data.process_data_paths.vocals_audio_file_path
    else:
        input_path = process_data.process_data_paths.audio_output_file_path

    # Denoise vocal audio
    denoised_output_path = os.path.join(
        process_data.process_data_paths.cache_folder_path, process_data.basename + "_denoised.wav"
    )
    denoise_vocal_audio(input_path, denoised_output_path, settings.skip_cache_denoise_vocal_audio)

    # Convert to mono audio
    mono_output_path = os.path.join(
        process_data.process_data_paths.cache_folder_path, process_data.basename + "_mono.wav"
    )
    convert_audio_to_mono_wav(denoised_output_path, mono_output_path)

    # Mute silence sections
    mute_output_path = os.path.join(
        process_data.process_data_paths.cache_folder_path, process_data.basename + "_mute.wav"
    )
    mute_no_singing_parts(mono_output_path, mute_output_path)

    # Define the audio file to process
    return mute_output_path


def parse_args():
    """Parse options specific to the DarkKaraoke extensions."""
    parser = argparse.ArgumentParser(description="UltraSinger - Geração Automática de Arquivos UltraStar")

    # Adicionar outros parâmetros já existentes

    # Novo parâmetro --changetone
    parser.add_argument(
        "--changetone",
        type=int,
        help="Muda a tonalidade dos áudios separados (exceto drums) em n semitons",
        required=False,
    )
    parser.add_argument(
        "--create-lyrics-video",
        action="store_true",
        help="gera vídeos MP4 com letras sincronizadas a partir do arquivo UltraStar",
    )
    parser.add_argument(
        "--video-background",
        help="imagem ou vídeo opcional usado como plano de fundo",
    )

    args = parser.parse_args()
    return args


def main():
    """Função principal para rodar o UltraSinger"""
    args = parse_args()
    
    # Aplicar as configurações com base nos argumentos recebidos
    settings.changetone = args.changetone
    settings.create_lyrics_video = args.create_lyrics_video
    settings.video_background = args.video_background
    if settings.changetone and not settings.create_karaoke:
        print(f"{ULTRASINGER_HEAD} Transposition requires a playback file; enabling karaoke output.")
        settings.create_karaoke = True
    
    # Executar o processo principal
    ultrastar_file_output, simple_score, accurate_score = run()

    if settings.create_lyrics_video:
        basename = process_data_basename(ultrastar_file_output)
        generate_lyrics_video(
            ultrastar_file_output,
            os.path.join(os.path.dirname(ultrastar_file_output), f"{basename}.mp3"),
            os.path.join(os.path.dirname(ultrastar_file_output), f"{basename}.mp4"),
            settings.video_background,
        )
        if settings.changetone:
            transposed_basename = f"{basename} [{settings.changetone:+d} semitones]"
            generate_lyrics_video(
                os.path.join(os.path.dirname(ultrastar_file_output), transposed_basename + ".txt"),
                os.path.join(os.path.dirname(ultrastar_file_output), transposed_basename + ".mp3"),
                os.path.join(os.path.dirname(ultrastar_file_output), transposed_basename + ".mp4"),
                settings.video_background,
            )
    print(f"Processamento completo. Arquivo UltraStar salvo em: {ultrastar_file_output}")


def process_data_basename(ultrastar_file_output: str) -> str:
    """Return the song basename without the UltraStar extension."""
    return os.path.splitext(os.path.basename(ultrastar_file_output))[0]


if __name__ == "__main__":
    main()
