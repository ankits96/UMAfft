#!/usr/bin/env python

# This script records a .wav file, and then runs an fft on it. 
# Code inspired by http://www.raspberrypi.org/forums/viewtopic.php?p=314087
 
import subprocess, signal, scipy
import numpy as np
import matplotlib.pyplot as plt

from threading import Thread
from scikits import audiolab

import lcm
from common import constants
from common import utime
from common.LCM.types.hydro_t import hydro_t

# Set up audio
sample_rate = 44100
no_channels = 1
chunk = 1024 # Use a multiple of 8

def calculate_levels(data, chunk,sample_rate):
   # Apply FFT - real data so rfft used
   fourier=np.fft.rfft(data)
   # Remove last element in array to make it the same size as chunk
   fourier=np.delete(fourier,len(fourier)-1)
   #print fourier
   # Find amplitude
   #print fourier
   dB = np.log(np.abs(fourier))
   #print power
   return dB


def run():

	lc = lcm.LCM()
	msg = hydro_t()

	while(True):

		subprocess.call("arecord -D plughw:0 --duration=5 --channels=1 --rate=44100 output.wav", shell=True)

		# print "Processing....."   
		data, sample_rate, toss1 = audiolab.wavread('output.wav') #data_in.read()
		matrix=calculate_levels(data, chunk,sample_rate)
		y = matrix>0
		matrix *= y
		x = scipy.linspace(0,sample_rate/2, len(matrix))
		# print x.shape
		# print matrix.shape
		matrix[:50000] = 0
		a = .9*np.max(matrix)
		peaks = np.where(matrix>=a)[0]
		# total = sum(matrix[peaks[0]-50:peaks[0]+50]) FOR AVERAGING
		# average = total/(len(matrix[peaks[0]-50:peaks[0]+50])) FOR AVERAGING
		print 'HDYROPHONE:: peaks at',np.where(matrix>=a)[0] *.2,'hZ'
		print 'HYDROPHONE:: amplitude at', peaks[0]*.2, 'hZ is', matrix[peaks[0]]
		msg.utime = utime.utime()
		msg.intensity = matrix[peaks[0]]
		msg.frequency = peaks[0] *.2
		lc.publish(constants.get_SENSOR_HYDROPHONE_CHANNEL(), msg.encode())

		#print matrix
		# plt.plot(x,matrix)
		#plt.xlim(0,20000)
		#plt.ylim(0,10)
		# plt.show()


if (__name__ == '__main__'):
	run()