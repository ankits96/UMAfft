#!/usr/bin/env python

# 8 bar Audio equaliser using MCP2307
 
import alsaaudio as aa
import smbus
from time import sleep
from struct import unpack
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scikits import audiolab

#bus=smbus.SMBus(0)     #Use '1' for newer Pi boards;

#ADDR   = 0x20         #The I2C address of MCP23017
#DIRA   = 0x00         #PortA I/O direction, by pin. 0=output, 1=input
#DIRB   = 0x01         #PortB I/O direction, by pin. 0=output, 1=input
#BANKA  = 0x12         #Register address for Bank A
#BANKB  = 0x13         #Register address for Bank B

#Set up the 23017 for 16 output pins
#bus.write_byte_data(ADDR, DIRA, 0);  #all zeros = all outputs on Bank A
#bus.write_byte_data(ADDR, DIRB, 0);  #all zeros = all outputs on Bank B

#def TurnOffLEDS ():
#  bus.write_byte_data(ADDR, BANKA, 0xFF)  #set all columns high
#   bus.write_byte_data(ADDR, BANKB, 0x00)  #set all rows low

#def Set_Column(row, col):
#   TurnOffLEDS()
#   bus.write_byte_data(ADDR, BANKA, col)
#   bus.write_byte_data(ADDR, BANKB, row)
         
# Initialise matrix
#TurnOffLEDS()

# Set up audio
sample_rate = 96000
no_channels = 2
chunk = 512 # Use a multiple of 8
data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL)
data_in.setchannels(no_channels)
data_in.setrate(sample_rate)
data_in.setformat(aa.PCM_FORMAT_S16_LE)
data_in.setperiodsize(chunk)

def calculate_levels(data, chunk,sample_rate):
   # Convert raw data to numpy array
   #data = np.delete(data,len(data)-1)
   #data = unpack("%dh"%(len(data)/2),data)
   #data = np.array(data, dtype='h')
   # Apply FFT - real data so rfft used
   fourier=np.fft.rfft(data)
   # Remove last element in array to make it the same size as chunk
   fourier=np.delete(fourier,len(fourier)-1)
   #print fourier
   # Find amplitude
   dB = np.abs(fourier)
   #print power
   # Araange array into 8 rows for the 8 bars on LED matrix
   #power = np.reshape(power,(8,chunk/8))
   #matrix= np.int_(np.average(power,axis=1)/4)
   return dB
print "Processing....."
#while True:
   #TurnOffLEDS()
   # Read data from device   
data, sample_rate, toss1 = audiolab.wavread('25ksin.wav') #data_in.read()
#l = len(data)
#print data
#data = np.array_str(data)
#print type(data)
#l = len(data)
#print data
#print l
   #data_in.pause(1) # Pause capture whilst RPi processes data
      # catch frame error
   #try:
matrix=calculate_levels(data, chunk,sample_rate)
y = matrix>0
      #y.astype(int)
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
         #plt.ioff()
         #plt.close()

   #except audioop.error, e:
    #  if e.message !="not a whole number of frames":
     #    raise e
#sleep(0.001)
   #data_in.pause(0) # Resume capture
