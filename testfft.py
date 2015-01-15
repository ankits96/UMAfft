#!/usr/bin/env python

#This script runs an fft on an existing .wav file
 
import alsaaudio as aa
import smbus
from time import sleep
from struct import unpack
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scikits import audiolab

# Set up audio
sample_rate = 96000
no_channels = 2
chunk = 512 # Use a multiple of 8

def calculate_levels(data, chunk,sample_rate):
   # Apply FFT - real data so rfft used
   fourier=np.fft.rfft(data)
   # Remove last element in array to make it the same size as chunk
   fourier=np.delete(fourier,len(fourier)-1)
   #print fourier
   # Find amplitude
   dB = np.abs(fourier)
   #print power
   return dB
print "Processing....."   
data, sample_rate, toss1 = audiolab.wavread('25ksin.wav') #data_in.read()
#l = len(data)
#print data
#data = np.array_str(data)
#print type(data)
#l = len(data)
#print data
#print l
matrix=calculate_levels(data, chunk,sample_rate)
y = matrix>0
matrix *= y
x = scipy.linspace(0,sample_rate/2, len(data)/2)
#print x.shape
#print matrix.shape
a = .9*np.max(matrix)
print np.max(matrix)
print a
start = 30000
end = 150000
total = sum(matrix[start:end])
#print total
average = total/(len(matrix[start:end]))
print 'average amplitude is', average
#print sum(matrix>(a))
print 'peaks at',np.where(matrix>a)[0] *.1 ,'hZ'
   #print matrix
plt.plot(x,matrix)
#plt.xlim(0,20000)
         #plt.ylim(0,10)
plt.show()
