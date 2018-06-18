#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Script to convert .xyz to .vti

Created on Tue Jun 12 15:23:36 2018

@author: moreira
"""
from numpy import *
import re

# function use to read the input file .xyz
def ReadFile(dfile):
    array = []
    with open(str(dfile), 'r') as myFile:
        for line in myFile:
            lines = re.sub(' +',' ',line)      
            lines = lines[1:]
            array.append(map(float, lines.split(' ')))
    return array

#function that converts .xyz to .vti
def xyz2vti(filename,Lx,Ly,Lz):
 
    phi = zeros((Lx,Ly,Lz))
    
    a = ReadFile(filename)
    
    for i in a:
        phi[int(i[0])+100][int(i[1])+100][int(i[2])+50] = i[3]
        
    
    f = open(filename[:-3]+'vti','w')
    
    f.write('<?xml version="1.0"?> \n')
    f.write('<VTKFile type="ImageData" version="0.1" byte_order="LittleEndian"> \n')
    f.write('  <ImageData WholeExtent="0 '+str(Lx)+' 0 '+str(Ly)+' 0 '+str(Lz)+'"   Origin="0 0 0" Spacing
="1 1 1"> \n')
    f.write('    <Piece Extent="0 '+str(Lx)+' 0 '+str(Ly)+' 0 '+str(Lz)+'"> \n')
    f.write('      <CellData> \n')
    f.write('        <DataArray Name="scalar_data" type="Float64" format="ascii">\n')
    for k in range(0,Lz):
        for j in range(0,Ly):
            for i in range(0,Lx):
                if(phi[i][j][k]<0.001): # for t - 0.001 - for phi 0.1
                    value = '0'
                else:
                    value = str(phi[i][j][k])
                    
                f.write(value+' ')
                
    f.write('        </DataArray>')
    f.write('      </CellData>\n')
    f.write('    </Piece> \n')
    f.write('  </ImageData> \n')
    f.write('</VTKFile> \n')
    
    f.close()
    print "File "+filename[:-3]+"vti done!"
    return






Lx = 200  # change the box length here
Ly = 200
Lz = 100

# Example: converting one file
filename = 'phi60000.xyz'
xyz2vti(filename, Lx, Ly, Lz)


#Example: converting several files
for i in range(2000,10000,2000):
    filename = 't'+str(i)+'.xyz'
    xyz2vti(filename,Lx,Ly,Lz)
