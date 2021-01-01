import os
import random
from madmom.features.beats import RNNBeatProcessor, DBNBeatTrackingProcessor
from pydub import AudioSegment
from typing import List, Optional
from clap import get_random_clap, ClapParams

"""
Parameters
"""
# file in ./data
FILE = "YOUR_FILE.mp3"
# mode
MODE = "claps"  # 'beats' | 'claps'
# whether to overlay or produce a new track with only claps
OVERLAY = True
# claps parameters
CLAPS_PITCH_SHIFT_MIN_OCTAVE = -0.5  # random pitch shift lower bound in octaves
CLAPS_PITCH_SHIFT_MAX_OCTAVE = 0.5  # random pitch shift upper bound in octaves
CLAPS_TIME_SHIFT_MAX_MS = 5  # max random time shift for overlaying each clap
CLAPS_VOLUME_LOOKBEHIND_BEATS = (
    4
)  # how many beats to look behind to determine the appropriate volume of the clap. If 0, always full volume.
CLAPS_GAIN = (
    20
)  # adjust as required: extra gain (in dB) for claps

"""
Constants
"""
REPO_ROOT = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(REPO_ROOT, "data")

BEAT_SOUND_PATH = os.path.join(REPO_ROOT, "sounds", "tone880.mp3")
CLAPS_PATH = os.path.join(REPO_ROOT, "sounds", "claps")
CLAPS_FILES = ["01.mp3", "02.mp3", "03.mp3", "04.mp3"]
FILE_PATH = os.path.join(DATA_PATH, FILE)
OUTPUT_PATH = os.path.join(REPO_ROOT, "output")
EXPORT_PATH = os.path.join(OUTPUT_PATH, FILE)

CLAP_PARAMS = ClapParams(
    CLAPS_PITCH_SHIFT_MIN_OCTAVE,
    CLAPS_PITCH_SHIFT_MAX_OCTAVE,
    CLAPS_TIME_SHIFT_MAX_MS,
    CLAPS_VOLUME_LOOKBEHIND_BEATS,
    CLAPS_GAIN,
)


def get_beats(file_path: str) -> List[float]:
    """
    Given the path to an audio file get a list of detected beat timings (in seconds)
    """
    print(f"Getting beats for {file_path}")
    proc = DBNBeatTrackingProcessor(fps=100)
    act = RNNBeatProcessor()(file_path)
    res: List[float] = proc(act)
    print(f"Got {len(res)} beats")
    print(res)
    return res


def apply_beat_sounds(
    file_path: str, beat_sound_path: str, beats: List[float], overlay: bool
) -> AudioSegment:
    print(f"Loading {file_path}")
    audio_file = AudioSegment.from_file(file_path)
    print(f"Loading {beat_sound_path}")
    beat_sound = AudioSegment.from_file(beat_sound_path)
    if not overlay:
        audio_file = AudioSegment.silent(duration=len(audio_file), frame_rate=audio_file.frame_rate)
        print("Making a new beat track")
    else:
        print("Overlaying beats")
    for b in beats:
        audio_file = audio_file.overlay(beat_sound, position=int(b * 1000))
    print(f"Finished overlaying beats")

    return audio_file


def apply_clap_sounds(
    file_path: str,
    claps: List[AudioSegment],
    beats: List[float],
    clap_params: ClapParams,
    overlay: bool,
) -> AudioSegment:
    print(f"Loading {file_path}")
    audio_file = AudioSegment.from_file(file_path)
    resultant_audio = audio_file
    if not overlay:
        resultant_audio = AudioSegment.silent(duration=len(audio_file), frame_rate=audio_file.frame_rate)
        print("Making a new clap track")
    else:
        print("Overlaying claps")
    for i in range(len(beats)):
        b = beats[i]
        clap = get_random_clap(audio_file, beats, i, claps, clap_params)
        if clap is not None:
            resultant_audio = resultant_audio.overlay(clap, position=int(b * 1000))
    print(f"Finished overlaying claps")
    return resultant_audio



if __name__ == "__main__":
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    print(f"Processing {FILE_PATH}")
    beats = get_beats(FILE_PATH)
    processed_audio: Optional[AudioSegment] = None

    if MODE == "claps":
        print(f"Mode: claps")
        claps: List[AudioSegment] = []
        for c in CLAPS_FILES:
            p = os.path.join(CLAPS_PATH, c)
            claps.append(AudioSegment.from_file(p))
        processed_audio = apply_clap_sounds(FILE_PATH, claps, beats, CLAP_PARAMS, OVERLAY)
         
    else:
        print(f"Mode: beats")
        processed_audio = apply_beat_sounds(FILE_PATH, BEAT_SOUND_PATH, beats, OVERLAY)

    print(f"Exporting to {EXPORT_PATH}")
    if processed_audio is not None:
        processed_audio.export(EXPORT_PATH)
    else:
        raise ValueError(f"Processed audio is None")
