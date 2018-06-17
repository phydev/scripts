#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 22:44:19 2018

@author: moreira

Description: This script apply the Savitisky-Golay filter to a 3D trajectory, calculate the mean velocity, 
the Mean Squared Deviation (MSD) and the Standard Error of the Mean (SEM). The output is given in micrometers/min. 

"""
from matplotlib import pyplot
from scipy import signal
from math import *

def ReadFile(dfile):
    array = []
    with open(str(dfile), 'r') as myFile:
        for line in myFile:
            array.append(map(float, line.split(' ')))
    myFile.close()
    return array

def msd(x,y,z,t):
    dt = 5
    length = 0.0
    number_of_lines = len(t)
    number_of_blocks = int(round(number_of_lines/dt))+1
    msdt = [0.0]*number_of_blocks
       
    block = 0
    nstep = 0
    tau = 1
    msdt[block] = 0.0
    i = tau
    tm = [0.0]*number_of_blocks
   
    while(i<number_of_lines-tau-1):
        
        msdt[block] = msdt[block] + (x[i] - x[0])**2 + (y[i] - y[0])**2 + (z[i] - z[0])**2
        nstep = nstep + tau;
    
        if(nstep==dt):
    
            nstep = 0  
            msdt[block] = (msdt[block]*5.0)/((number_of_lines-tau)*1.0)
            #print t[i],' ', msdt[block] 
            tm[block] = t[i]
            block+=1
        
            msdt[block] = msdt[block-1]
        
        i+=tau
    
    
    print len(tm), len(msdt)    
    return tm, msdt

  

density = 68  # escolhe para qual densidade vais calcular a trajetoria aqui
seed = 0 # a primeira seed a ser calculada
fseed = 5  # a ultima seed a ser calculada. .. 
folder = '0.'+str(density)+'/0'
v = []
L = []

average = 0.0
nsample = 0.0

while (seed<=fseed): 
    dir_name = folder+str(density)+str(seed)
   
    a = ReadFile(dir_name+'/v.out')
    
    
    t = []
    x = []
    y = []
    z = []
    dx = []
    dy = []
    dz = []
    
    
    for i in a:
        t.append(i[0])
        x.append(i[1])
        y.append(i[2])
        z.append(i[3])
    msdt = []
    tm = []      
    tm, msdt = msd(x,y,z,t)
    
    # Savitzky-Golay Smoothing filter
    x = signal.savgol_filter(x, 3, 1, mode='nearest')
    y = signal.savgol_filter(y, 3, 1, mode='nearest')
    z = signal.savgol_filter(z, 3, 1, mode='nearest')
    length = 0.
        
    for i in range(0,len(x)-1):
          #tf=150
          #if(t[i]>tf):
           #   break
          dx.append(round(round(x[i+1],2)-round(x[i],2),2))
          dy.append(round(round(y[i+1],2)-round(y[i],2),2))
          dz.append(round(round(z[i+1],2)-round(z[i],2),2))
          
          length = length + sqrt(pow(dx[i],2) + pow(dy[i],2) + pow(dz[i],2))
          
    v.append((length/(t[len(t)-1]))*1.5)
    L.append(length)
    if(length>10):
        nsample = nsample + 1.0
        average = average + v[seed]
        del tm[-1]
        del msdt[-1]
        pyplot.plot(tm,msdt)
    
    print dir_name, length, v[seed] #, tf
    seed+=1

    
average = average/nsample
stdev = 0.0
for i in range(0,len(v)-1):
    if(L[i]>10):
        stdev = stdev + (v[i] - average)**2

stdev = sqrt(stdev/(nsample*(nsample-1.0))) # n(n-1) ? or (n-1)
    
print "Number of Samples", nsample 
print "Average velocity - stdev (micrometers/min):", average, stdev

