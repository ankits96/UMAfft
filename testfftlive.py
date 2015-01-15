#!/usr/bin/env python

# This script attempts to do an FFT on sound data in real time. Currently not entirely too accurate
 
import alsaaudio as aa
import time
from struct import unpack
import numpy as np
import matplotlib.pyplot as plt
import scipy


# Set up audio
sample_rate = 96000
no_channels = 2
chunk = 2000 # Use a multiple of 8
data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL, card = 'default')
data_in.setchannels(no_channels)
data_in.setrate(sample_rate)
data_in.setformat(aa.PCM_FORMAT_S16_LE)
data_in.setperiodsize(chunk)

def calculate_levels(data, chunk,sample_rate):
   # Convert raw data to numpy array
   data = unpack("%dh"%(len(data)/2),data)
   data = np.array(data, dtype='h')
   # Apply FFT - real data so rfft used
   fourier=np.fft.rfft(data)
   # Remove last element in array to make it the same size as chunk
   fourier=np.delete(fourier,len(fourier)-1)
   # Find amplitude
   power =(np.abs(fourier))
   return power

print "Processing....."

#most comments are for debugging purposes

matrix2=0
timeout = time.time()+2
iters = 0
while True:
   # Read data from device   
   l,data = data_in.read()
   data_in.pause(1) # Pause capture whilst RPi processes data
   #if l:
      # catch frame error
      #try:
   matrix=calculate_levels(data, chunk,sample_rate)
   #print matrix.shape
   matrix[:200] = 0 #throws out the edges since they dont seem to be necessary
   matrix[1900:]=0
   matrix2+=matrix #to have aggregate data
   xaxis = scipy.linspace(0,sample_rate/2, len(data)/4)
   #plt.plot(xaxis,matrix)
   #plt.xlim(0,20000)
   #plt.show()
   #plt.close()
   #print matrix2.shape
   #print xaxis.shape
   #print matrix
   time.sleep(.1) #wait before capturing
   data_in.pause(0) # Resume capture
   iters += 1
   if time.time()>timeout: #runs for 2 seconds
       break

#total = sum(matrix2[1300:1350])
#matrix2[1300:1350] = 0
#print total/iters
#print iters
#print sum(matrix2)
#matrix2 /= iters
#print sum(matrix2)
plt.plot(xaxis, matrix2)
#plt.xlim(0,20000)
plt.ylim(500)
plt.show()
