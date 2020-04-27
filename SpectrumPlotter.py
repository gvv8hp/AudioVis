import matplotlib.pyplot as plt
import numpy as np

class Spectrum:
    def __init__(self, s=[], t=0, dt=0):
        self.s = s
        self.t = t
        self.dt = dt
        self.Fs = 1/self.dt

    def showPlot(self, frange=[0,20000]):
        fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(7,7))
        # plot time signal:
        axes[0, 0].set_title("Signal")
        axes[0, 0].plot(self.t, self.s, color='C0')
        axes[0, 0].set_xlabel("Time")
        axes[0, 0].set_ylabel("Amplitude")

        # plot different spectrum types:
        axes[1, 0].set_title("Magnitude Spectrum")
        axes[1, 0].magnitude_spectrum(self.s, Fs=self.Fs, color='C1')
        axes[1, 0].set_xlim(frange[0], frange[1])

        axes[1, 1].set_title("Log. Magnitude Spectrum")
        axes[1, 1].magnitude_spectrum(self.s, Fs=self.Fs, scale='dB', color='C1')


        axes[2, 0].set_title("Phase Spectrum ")
        axes[2, 0].phase_spectrum(self.s, Fs=self.Fs, color='C2')

        axes[2, 1].set_title("Angle Spectrum")
        axes[2, 1].angle_spectrum(self.s, Fs=self.Fs, color='C2')

        axes[0, 1].remove()  # don't display empty ax

        fig.tight_layout()
        plt.show()

def plotFFT(fft):
    fig = plt.figure()
    ax = plt.axes()
    x = np.arange(0, len(fft), 1)
    ax.plot(x, fft)
    ax.set_xlim(0,len(fft))
    plt.show()