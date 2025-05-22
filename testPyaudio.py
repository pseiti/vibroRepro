import time

import numpy as np
import pyaudio

def playVib(vol,dur,Hz):

    p = pyaudio.PyAudio()
 
    volume = vol  # range [0.0, 1.0]
    fs = 44100  # sampling rate, Hz, must be integer
    duration = dur  # in seconds, may be float
    f = Hz  # sine frequency, Hz, may be float

    # generate samples, note conversion to float32 array
    samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)
    # print(len(samples))

    # per @yahweh comment explicitly convert to bytes sequence
    output_bytes = (volume * samples).tobytes()

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    # play. May repeat with different volume values (if done interactively)
    start_time = time.time()
    stream.write(output_bytes)
    # print("Played sound for {:.2f} seconds".format(time.time() - start_time))

    stream.stop_stream()
    stream.close()

    p.terminate()

playVib(vol=.5,dur=1,Hz=440)