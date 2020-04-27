# Input imports
import pyaudio
import numpy as np
import time

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Stream Parameters
RATE = 44100*4
CHUNKSIZE = 16384
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
        print(len(fft))
        fft = fft[:int(len(fft)/2)] # keep only first half
        # freq = np.fft.fftfreq(CHUNKSIZE,1.0/RATE)
        # freq = freq[:int(len(freq)/2)] # keep only first half
        #assert freq[-1]>TARGET, "ERROR: increase chunk size"
        #val = fft[np.where(freq>TARGET)[0][0]]
        #print("val:"+ str(val) +"\t\t"+"|"*int(float(val)/1000))
        yield fft


# for item in fft:
#     print(item)

print(f"Period: {PERIOD}")

class Scope:
    def __init__(self, ax, maxt=500, miny=1000, maxy=1000000, dt=0.02):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [1]
        self.ydata = [1]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(miny, maxy)
        self.ax.set_xlim(0, self.maxt)
        # self.ax.set_xscale("log")
        # self.ax.set_xscale("log", basex=1.000001)
        self.ax.set_yscale("log", basey=10)
        self.maxAmp = 0

    def update(self, fft):
        # lastt = self.tdata[-1]
        # if lastt > self.tdata[0] + self.maxt:  # reset the arrays
        #     self.tdata = [self.tdata[-1]]
        #     self.ydata = [self.ydata[-1]]
        #     self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
        #     self.ax.figure.canvas.draw()

        # if (y > self.maxAmp):
        #     self.maxAmp = y
        #     self.ax.set_ylim(-.1, self.maxAmp)

        # t = self.tdata[-1] + self.dt
        # self.tdata.append(t)
        # self.ydata.append(y)
        # self.line.set_data(self.tdata, self.ydata)

        freq = np.fft.fftfreq(CHUNKSIZE,1.0/RATE)
        freq = freq[:int(len(freq)/2)] # keep only first half

        self.tdata = freq
        self.ydata = fft
        self.line.set_data(self.tdata, self.ydata)
        self.ax.figure.canvas.draw()

        return self.line,
        
# Fixing random state for reproducibility



fig, ax = plt.subplots()
scope = Scope(ax)

# pass a generator in "emitter" to produce data for the update func
ani = animation.FuncAnimation(fig, scope.update, getLevel, interval=10,
                              blit=True)

plt.show()

stream.stop_stream()
stream.close()
p.terminate()

