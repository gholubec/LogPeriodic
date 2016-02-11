#!/usr/bin/python

"""
nonPlanarLpda.py

Non-Planar LPDA Wire Generator

EZ-NEC ASCII File Format Description

Wire definitions consist of end 1 coordinates, end 2 coordinates, and diameter. 
If desired, the number of segments can be added as an eighth field. 
If the segment field isn't included, the wire will be automatically segmented 
using the "conservative" criterion.
The file is case-insensitive. 

Blank lines, and any text on a line following a semicolon will be ignored. 
Blanks, tabs, or any combination can be used as delimiters (separators between 
fields or individual specifications). 
Commas can be used as delimiters only if your decimal separator is not a comma. 
Number format must correspond to your Windows regional setting. 
That is, if you normally write one-and-one-half  1,5 then it must be written 
that way in this file.

"""

import sys
import os
from math import *


#{START: Define and Set LPDA Design Parameters
#LPDA Design Parameters Default Values

#Angular Design Parameters in Degrees
Alpha = 45.0
AlphaRadians = pi*Alpha/180.0

Tsi = 30.0
TsiRadians = pi*Tsi/180.0

#Element Filling Parameter
#As T approaches 1 the number of elements increases
T = 0.6

#Lowest Frequency (mhz)
fl=144.0

#Upper Frequency
fu=1400.0

#Element Diameter in Inches
Dia_Base = 0.375

#Scale Wire Diameter Option
Scale_Wire_Dia = True


#Num Segments for Each Wire
NumSegments_Base = 21

#EZ-NEC File Format
EZ_NEC = True


#}DONE: Define and Set LPDA Design Parameters

#{START: Initialize Lists and Other Containers
#LSD Triple Container, 
#For Each Element Pair (Length, Separation, Distance to Vertex)
LSD=[]
LSD.append(("Length","Separation","Distance_to_Vertex","Element_Diameter"))

#}DONE: Initialize Lists and Other Containers


#{START: Determine Over All Dimensions of the LPDA

#Length of First Element Pair in Feet
#L=492(ft/mhz)/Frequency(mhz)
L=492.0/fl

#Distance of First Element Pair to Vertex
D=L/tan(AlphaRadians/2.0)

#Separation of First Element Pair
S=2*D*tan(TsiRadians/2.0)

#Element Diameters of the First Diameter Pair in Feet
Dia = Dia_Base/12.0 #Base Diameter given in Inches

#Generate the First LSD Triple and Place in the Triple List Container
LSD.append((L,S,D,Dia))

#Generate Boom Length of Element Supporter
BoomLength = sqrt((S/2.0)**2 + D**2)


#Calulate the Number of Element Pairs Required
NumElementPairs = int(ceil(2*(log((fl/fu)*3.0/4.0)/log(T))+1))

for entry in LSD : print entry
print "BoomLength(ft):",BoomLength
print L,S,D,Dia
print "Num Element Pairs:",NumElementPairs
print "Lower Frequency (mhz):",fl
print "Upper Frequency (mhz):",fu

#}DONE: Determine Over All Dimensions of the LPDA


#{START: Generate the Element Pairs
Num = 2
while Num <= NumElementPairs :

    #Calculate New Length
    L *= sqrt(T)
    
    #Calculate New Separation
    S *= sqrt(T)
    
    #Calculate New Distance to Vertex
    D *= sqrt(T)
    
    #Calculate New Wire Diameter
    if (Scale_Wire_Dia) : Dia *= sqrt(T)
    else : Dia = Dia_Base
    
    #Append LSD Array and go to Next Value
    LSD.append((L,S,D,Dia))
    Num +=1

#}DONE: Generate the Element Pairs

print
print "LSD Array"
for entry in LSD : print entry


#{START: Create LSD Array in Inches
LSD_inch = []
for entry in enumerate(LSD) :
    #Append Header
    if entry[0] == 0 : LSD_inch.append(entry[1])
    
    #Generate LSD_Inch Entries
    if entry[0] != 0 :
        L_inch = 12.0*entry[1][0]
        S_inch = 12.0*entry[1][1]
        D_inch = 12.0*entry[1][2]
        Dia_inch = 12.0*entry[1][3]
        LSD_inch.append((L_inch,S_inch,D_inch,Dia_inch))

print       
for entry in LSD_inch : print entry
#}DONE: LSD Array in Inches

def selectWireInch(dia_Inch,available_InchDiameterS=[1.0,0.75,0.5,0.375,0.25,0.125]) :
    minDifference = abs(10000.0 - dia_Inch)
    diameterSelected = 10000
    for diameter in available_InchDiameterS :
        difference = abs(dia_Inch-diameter)
        if difference < minDifference :
            minDifference = difference
            diameterSelected = diameter
    return diameterSelected
            



#{START: Generate Wire Array
#This array will be used to create the ASCII Files For Either NEC Programs or EZ-NEC

WireS = []
WireS.append(("X1","Y1","Z1","X2","Y2","Z2","Dia","Num_SegmentS"))

#START: Create the Transverse Wires
for entry in enumerate(LSD_inch) :
    if entry[0] != 0 : 
        L = entry[1][0]
        S = entry[1][1]
        D = entry[1][2]
        Dia = entry[1][3]
        
        #{START: Create and Store Upper Element of Element Pair
        #Create Upper Left Hand Side
        X1 = D
        Y1 = L/2.0
        Z1 = S/2.0
        X2 = D
        Y2 =  0
        Z2 = S/2.0
        DiaClosest = selectWireInch(Dia)
        NumSegments = NumSegments_Base
        WireS.append((X1,Y1,Z1,X2,Y2,Z2,DiaClosest,NumSegments))
        #Create Upper Right Hand Side
        X1 = D
        Y1 = 0
        Z1 = S/2.0
        X2 = D
        Y2 = -L/2.0
        Z2 = S/2.0
        DiaClosest = selectWireInch(Dia)
        NumSegments = NumSegments_Base
        WireS.append((X1,Y1,Z1,X2,Y2,Z2,DiaClosest,NumSegments))        
        #}DONE: Create and Store Upper Element of Element Pair

        #{START: Create and Store Lower Element of Element Pair
        #Create Lower Left Hand Side
        X1 = D
        Y1 = L/2.0
        Z1 = -S/2.0
        X2 = D
        Y2 = 0
        Z2 = -S/2.0
        DiaClosest = selectWireInch(Dia)
        NumSegments = NumSegments_Base
        WireS.append((X1,Y1,Z1,X2,Y2,Z2,DiaClosest,NumSegments)) 
        #Create Lower Right Hand Side
        X1 = D
        Y1 = 0
        Z1 = -S/2.0
        X2 = D
        Y2 = -L/2.0
        Z2 = -S/2.0
        DiaClosest = selectWireInch(Dia)
        NumSegments = NumSegments_Base
        WireS.append((X1,Y1,Z1,X2,Y2,Z2,DiaClosest,NumSegments))        
        #}DONE: Create and Store Lower Element of Element Pair
        
        
#Create the Connecting Wires
#Top Side (z > 0) Odd to Even Connect on the Right Side, y > 0

#Bottom Wires (z < 0 ) Odd to Event Connect on the Left Side, y < 0

#Connect Wires Down the Middle
        
print
print "Wires"
for entry in WireS : print entry
#}DONE: Generate Wire Array


#{START: Publish Wire Array


fileObj=open("LPDA.txt","w")
iter = 0
for entry in WireS :
    if EZ_NEC and iter == 0 : 
        fileObj.write("in\r\n")
        iter += 1
        continue 
    outputString = ""
    for _entry in entry :
        outputString += str(_entry)+" "
        iter += 1
    fileObj.write(outputString+"\r\n")
    
fileObj.close()
#}DONE: Publish Wire Array