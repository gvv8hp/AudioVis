# Input imports
import pyaudio
import numpy as np

# Plotting imports
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# import tmp102

# import only system from os 
from os import system, name 
  
# import sleep to show output for some time period 
from time import sleep 


# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    # Read temperature (Celsius) from TMP102
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    fft = abs(np.fft.fft(data).real)
    fft = fft[:int(len(fft)/2)] # keep only first half
    freq = np.fft.fftfreq(CHUNK,1.0/RATE)
    freq = freq[:int(len(freq)/2)] # keep only first half
    assert freq[-1]>TARGET, "ERROR: increase chunk size"
    val = fft[np.where(freq>TARGET)[0][0]]
    print("val:"+ str(val) +"\t\t"+"|"*int(float(val)/1000))

    # Add x and y to lists
    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(val)

    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Frequency Level over Time')
    plt.ylabel('Amplitude')



np.set_printoptions(suppress=True) # don't use scientific notation

CHUNK = 2048 # number of data points to read at a time
#RATE = 44100*2 # time resolution of the recording device (Hz)
RATE = 44100*2 # time resolution of the recording device (Hz)

TARGET = 70 # show only this one frequency

p=pyaudio.PyAudio() # start the PyAudio class
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK) #uses default input device

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=.0001)
plt.show()

# create a numpy array holding a single read of audio data
#for i in range(1000000000000): #to it a few times just to see


# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()

