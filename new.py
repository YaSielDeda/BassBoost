from pydub import AudioSegment
from pydub import effects
import numpy as np
import math
import os

bass = 20
speedup = 0

def bass_line_freq(track):
    sample_track = list(track)

    # c-value
    est_mean = np.mean(sample_track)

    # a-value
    est_std = 3 * np.std(sample_track) / (math.sqrt(2))

    bass_factor = int(round((est_std - est_mean) * 0.005))

    return bass_factor

def speed(track, speed):
    sound_with_altered_frame_rate = track._spawn(track.raw_data, overrides={
        "frame_rate": int(track.frame_rate * speed)
    })
    return sound_with_altered_frame_rate.set_frame_rate(track.frame_rate)

def Boost(name, bass, speedup):
    #dst = "test.mp3"
    track = AudioSegment.from_file(name)

    if(track.duration_seconds > 300):
        print("Многа, давай что бы было меньше 5 минут, не охота полдня твоё говно бустить")
        return 0

    freq = bass_line_freq(track.get_array_of_samples())

    if (freq < 50):
        filtered_low = track.low_pass_filter(freq)
        filtered_high = track.high_pass_filter(freq)
        boosted = filtered_high.overlay(filtered_low + bass)
        if (0.5 < speedup < 2):
            boosted = speed(boosted, speedup)
    else:
        filtered_low = track.low_pass_filter(freq)
        filtered_low = filtered_low + bass
        filtered_high = track.high_pass_filter(freq)
        for i in range(0, 2):
            filtered_low = filtered_low.low_pass_filter(freq)
            if not (i > 1):
                filtered_high = filtered_high.high_pass_filter(freq)

        boosted = filtered_high.overlay(filtered_low)
        if (0.5 < speedup < 2):
            boosted = speed(boosted, speedup)
    return boosted.export("final.mp3", format="mp3")

def name():
    files = os.listdir()
    file = filter(lambda x: x.endswith('.mp3'), files)
    return list(file)[0]

def clean():
    files = os.listdir()
    file = filter(lambda x: x.endswith('.mp3'), files)
    for i in list(file):
        os.remove(i)

#Boost(name(), bass, speedup)
#clean()