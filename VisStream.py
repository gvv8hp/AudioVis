from OpenGL.GL import *
from OpenGL.GLU import *

import random
import math
import queue

# Input imports
import pyaudio
import numpy as np
import time

import SpectrumPlotter

class VisStream:
    def __init__(self, rate=48000*4, chunkSize=4096*1):
        self.rate = rate
        self.chunkSize = chunkSize
        self.period = 1/self.rate
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=self.rate,
                    input=True
        )
        self.fft = []
        #self.ffts = queue.Queue(queueSize)
        self.upperLim = 0
        self.runCount = 0
        self.minS =[9999999999, 9999999999, 9999999999, 9999999999, 9999999999, 9999999999]
        self.maxS =[0, 0, 0, 0, 0, 0]
        self.minFFT = 99999999
        self.maxFFT = 00000000

    def periodicReset(self):
        if self.runCount > 20:
            self.minS = [9999999999, 9999999999, 9999999999, 9999999999, 9999999999, 9999999999]
            self.maxS = [0, 0, 0, 0, 0, 0]

            self.minFFT = 99999999
            self.maxFFT = 00000000
            self.runCount = 0
        else:
            self.runCount+=1

    def reset(self): 
        
        self.minS = [9999999999, 9999999999, 9999999999, 9999999999, 9999999999, 9999999999]
        self.maxS = [0, 0, 0, 0, 0, 0]

        self.minFFT = 99999999
        self.maxFFT = 00000000

    def endStream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def is_active(self):
        return self.stream.is_active()

    def setFFT(self):
        data = np.fromstring(self.stream.read(self.chunkSize),dtype=np.int16)
        fft = abs(np.fft.fft(data).real)
        fft = fft[:int(len(fft)/2)] # keep only first half
        fft = fft[0:int(20000 * self.chunkSize / self.rate)] # keep only audible frequencies
        # self.periodicReset()
        # if (self.ffts.full()):
        #     self.ffts.get()
        #     self.ffts.put(fft)
        # else:
        #     self.ffts.put(fft)
        # fftsList = list(self.ffts.queue)
        # avgFFT = []
        
        # for i in range(len(fftsList[0])):
        #     product = 1
        #     for j in range(len(fftsList)):
        #         product = product * fftsList[j][i]
        #     avgFFT.append(product/len(fftsList))

        # self.fft = avgFFT

        self.fft = fft

    def plotStream(self):
        data = np.fromstring(self.stream.read(self.chunkSize),dtype=np.int16)
        t = np.arange(0, self.chunkSize)
        plot = SpectrumPlotter.Spectrum(data, t, self.period)
        plot.showPlot(frange=[0,1000])
    
    def plotFFT(self):
        SpectrumPlotter.plotFFT(self.fft)

    def getSideColors(self):
        minS = self.minS
        maxS = self.maxS

        self.setFFT()
        fft = self.fft
        # upperLim = int(20000 * self.chunkSize / self.rate)
        # self.upperLim = upperLim
        # fft = fft[0:upperLim]
        upperLim = len(fft)
        freq = np.fft.fftfreq(4096,1.0/44100*4)
        freq = freq[:int(len(freq)/2)] # keep only first half

        ffts = (
            fft[0:int(.05*upperLim)],
            fft[int(.05*upperLim):int(.1*upperLim)],
            fft[int(.1*upperLim):int(.2*upperLim)],
            fft[int(.2*upperLim):int(.35*upperLim)],
            fft[int(.35*upperLim):int(.5*upperLim)],
            fft[int(.5*upperLim):int(upperLim)]
        )

        # fft1 = fft[0:fftChunk]
        # fft2 = fft[fftChunk:fftChunk*2]
        # fft3 = fft[fftChunk*2:fftChunk*3]
        # fft4 = fft[fftChunk*3:fftChunk*4]
        # fft5 = fft[fftChunk*4:fftChunk*5]
        # fft6 = fft[fftChunk*5:fftChunk*6]

        sides = []

        i = 0
        for fft in ffts:
            sides.append(np.mean(fft))
            if (sides[i] < minS[i]):
                minS[i] = sides[i]
            if (sides[i] > maxS[i]):
                maxS[i] = sides[i]
            # print(f"minS ({i}): {minS[i]}")
            # print(f"maxS ({i}): {maxS[i]}")
            i+=1 

        i = 0
        upper = 1
        lower = .01
        for i in range(len(sides)):
            sides[i] = (sides[i] - minS[i])/(maxS[i] - minS[i]) * (upper-lower) + lower
            # print(f"side{i}: {sides[i]}")
            i+=1

        # s1 = np.mean(fft1)/scaleFactor
        # s2 = np.mean(fft2)/scaleFactor
        # s3 = np.mean(fft3)/scaleFactor
        # s4 = np.mean(fft4)/scaleFactor
        # s5 = np.mean(fft5)/scaleFactor
        # s6 = np.mean(fft6)/scaleFactor
        # s2 = 0
        # s3 = 0
        # s4 = 0
        # s5 = 0
        # s6 = 0


        sideColors = (
            (sides[0],0,0),
            (0,sides[1],0),
            (0,0,sides[2]),
            (sides[3],sides[3],0),
            (0,sides[4],sides[4]),
            (sides[5],0,sides[5]),
        )
        return sideColors

    def getDynamicRotation(self, lower, upper, maxFreq):
        fft = self.fft
        fft = fft[0:int(maxFreq * self.chunkSize / self.rate)]
        fftAvg = np.mean(fft)
        if fftAvg > self.maxFFT:
            self.maxFFT = fftAvg
        if fftAvg < self.minFFT:
            self.minFFT = fftAvg
        fftAvgScale = (fftAvg - self.minFFT)/(self.maxFFT - self.minFFT) * (upper-lower) + lower
        if (math.isnan(fftAvgScale)):
            return 1
        return fftAvgScale
