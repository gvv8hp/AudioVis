# Input imports
import pyaudio
import numpy as np
import time

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Stream Parameters
RATE = 44100*4
CHUNKSIZE = 4096
TARGET = 40

# seconds = samples / (samples/second)
PERIOD = CHUNKSIZE / RATE

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNKSIZE)

def getLevel():
    while True:
        data = np.fromstring(stream.read(CHUNKSIZE),dtype=np.int16)
        fft = abs(np.fft.fft(data).real)
        fft = fft[:int(len(fft)/2)] # keep only first half
        freq = np.fft.fftfreq(CHUNKSIZE,1.0/RATE)
        freq = freq[:int(len(freq)/2)] # keep only first half
        #assert freq[-1]>TARGET, "ERROR: increase chunk size"
        #val = fft[np.where(freq>TARGET)[0][0]]
        #print("val:"+ str(val) +"\t\t"+"|"*int(float(val)/1000))
        yield fft


# for item in fft:
#     print(item)

print(f"Period: {PERIOD}")

def update(self, fft):
    plt.cla()
    plt.hist(data[num])

fig = plt.figure()
hist = plt.hist(data[0])

animation = animation.FuncAnimation(fig, update_hist, getLevel, fargs=(data, ) )
plt.show()
plt.show()

stream.stop_stream()
stream.close()
p.terminate()

