from pydub import AudioSegment
from typing import List, Optional
import random


class ClapParams:
    def __init__(
        self,
        pitch_shift_min_octave,
        pitch_shift_max_octave,
        time_shift_max_ms,
        volume_lookbehind_beats,
        gain,
    ):
        self.pitch_shift_min_octave = pitch_shift_min_octave
        self.pitch_shift_max_octave = pitch_shift_max_octave
        self.time_shift_max_ms = time_shift_max_ms
        self.volume_lookbehind_beats = volume_lookbehind_beats
        self.gain = gain


def pitch_shift(audio: AudioSegment, shift_octaves: float) -> AudioSegment:
    sample_rate = audio.frame_rate
    new_sample_rate = int(audio.frame_rate * (2.0 ** shift_octaves))

    shifted_sound = audio._spawn(
        audio.raw_data, overrides={"frame_rate": new_sample_rate}
    )
    shifted_sound = shifted_sound.set_frame_rate(sample_rate)

    return shifted_sound


def get_clap_volume_reduction_adjustment(
    audio: AudioSegment,
    beats: List[float],
    curr_beat_index: int,
    clap_params: ClapParams,
) -> Optional[int]:
    """
    get the amount (in dB) to reduce the clap volume. Returns None if should not overlay at all
    """
    if clap_params.volume_lookbehind_beats == 0:
        return clap_params.gain

    start_beat_index = (
        0
        if curr_beat_index < clap_params.volume_lookbehind_beats
        else curr_beat_index - clap_params.volume_lookbehind_beats
    )

    start_time_ms = int(1000 * beats[start_beat_index])
    end_time_ms = int(1000 * beats[curr_beat_index])
    audio_segment = audio[start_time_ms:end_time_ms]

    amp = audio_segment.dBFS

    return amp + clap_params.gain


def get_random_clap(
    audio: AudioSegment,
    beats: List[float],
    curr_beat_index: int,
    claps: List[AudioSegment],
    clap_params: ClapParams,
) -> Optional[AudioSegment]:
    """
    Get a randomised clap sound from the given claps, based on the parameters.
    """

    resultant_audio: Optional[AudioSegment] = None

    # volume reduction adjustment
    db_to_reduce = get_clap_volume_reduction_adjustment(
        audio, beats, curr_beat_index, clap_params
    )

    if db_to_reduce is None:
        return None

    claps_indices = list(range(len(claps)))
    random.shuffle(claps_indices)

    for i in claps_indices:
        clap = claps[i]
        # pitch shift
        shift_amt = random.uniform(
            clap_params.pitch_shift_min_octave, clap_params.pitch_shift_max_octave
        )
        c = pitch_shift(clap, shift_amt)

        if resultant_audio is None:
            resultant_audio = c
        else:
            # time shift in ms
            timeshift_amt_ms = random.uniform(0, clap_params.time_shift_max_ms)
            resultant_audio = resultant_audio.overlay(c, position=int(timeshift_amt_ms))

    if resultant_audio is not None:
        resultant_audio += db_to_reduce
        return resultant_audio

    return None
