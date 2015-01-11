#!/usr/bin/env python

# 8 bar Audio equaliser using MCP2307
 
import alsaaudio as aa
import smbus
import time
from struct import unpack
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scikits import audiolab
from matplotlib import animation


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
  # bus.write_byte_data(ADDR, BANKB, 0x00)  #set all rows low

#def Set_Column(row, col):
 #  TurnOffLEDS()
  # bus.write_byte_data(ADDR, BANKA, col)
   #bus.write_byte_data(ADDR, BANKB, row)
         
# Initialise matrix
#TurnOffLEDS()

# Set up audio
sample_rate = 96000
no_channels = 2
chunk = 2000 # Use a multiple of 8
data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL, card = 'default')
data_in.setchannels(no_channels)
data_in.setrate(sample_rate)
data_in.setformat(aa.PCM_FORMAT_S16_LE)
data_in.setperiodsize(chunk)

#Set up animation
#def init()

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
   # Araange array into 8 rows for the 8 bars on LED matrix
   #power = np.reshape(power,(8,chunk/8))
   #matrix= np.int_(np.average(power,axis=1)/4)
   return power

print "Processing....."

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
   print matrix.shape
   matrix[:200] = 0
   #matrix[1900:]=0
   matrix2+=matrix
   xaxis = scipy.linspace(0,sample_rate/2, len(data)/4)
   #plt.plot(xaxis,matrix)
   #plt.xlim(0,20000)
   #plt.show()
         #plt.close()
         #print matrix2.shape
         #print xaxis.shape
         #print matrix
         #for i in range (0,8):
         #   Set_Column((1<<matrix[i])-1,0xFF^(1<<i))
      #except audioop.error, e:
      #   if e.message !="not a whole number of frames":
      #      raise e
   time.sleep(.1)
   data_in.pause(0) # Resume capture
   iters += 1
   if time.time()>timeout:
       break

#total = sum(matrix2[1300:1350])
#matrix2[1300:1350] = 0
#print total/iters
plt.plot(xaxis, matrix2)
#plt.xlim(0,20000)
plt.ylim(500)
plt.show()
