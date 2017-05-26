#!/usr/bin/python
# coding: utf-8

import os
import sys
from math import *

# H_Res   - Horizontal resolution (1600 to 1920)
# V_Res   - (50Hz : 192 to 288) - (60Hz : 192 a 256)
# R_Rate  - (47 a 62)
# H_Pos   - Horizontal position of the screen (-10 to 10)
# H_Zoom  - Horizontal size of the screen (-40 to 10)
# V_Pos   - Vertical position of the screen (-10 to 10) 
# H_FP    - Horizontal Front Porch. Set to 48 if you don't know what you do.
# H_Sync  - Horizontal Sync. Set to 192 if you don't know what you do.
# H_BP    - Horizontal Back Porch. Set to 240 if you don't know what you do.
# V_Sync  - Vertical Sync. (3 to 10 or more...)
# H_Freq  - Horizontal frequency of the screen. (15500 to 16000)

# WARNING, all these values are intrinsically linked. If your screen is desynchronized, quickly reboot the RPI.
# Some values will be limited due to other values.

 
H_Res=int(sys.argv[1])
V_Res=int(sys.argv[2])
R_Rate=float(sys.argv[3])
H_Pos=int(sys.argv[4])
H_Zoom=int(sys.argv[5])
V_Pos=int(sys.argv[6])
H_FP=int(sys.argv[7])
H_Sync=int(sys.argv[8])
H_BP=int(sys.argv[9])
V_Sync=int(sys.argv[10])
H_Freq=int(sys.argv[11])


# Scaling Front and back porch horizontals according to the position and zoom settings
H_FP=H_FP-(H_Zoom*3)-(H_Pos*3)
H_BP=H_BP-(H_Zoom*3)+(H_Pos*3)

# Do not use negative values
if H_FP < 0 :
  H_FP = 0
if H_BP < 0 :
  H_BP = 0

# Total number of horizontal, visible and invisible pixels
H_Total=(H_Res+H_FP+H_Sync+H_BP)

# Calculate the number of lines
V_Total=H_Freq/R_Rate
V_Total=int(ceil(V_Total))

# Calculation of the horizontal frequency
Horizontal=V_Total*R_Rate
Horizontal=int(ceil(Horizontal))

# Calculation of the pixel clock
Pixel_Clock=Horizontal*H_Total

# Calculation of the Vertical Front Porch
V_FP=V_Total-V_Res
V_FP=V_FP-V_Sync
V_FP=V_FP/2
V_FP=int(floor(V_FP))

# Vertical Position can't be bigger than Vertical Front Porch
if V_Pos > V_FP :
  V_Pos = V_FP
  
# Calculate Vertical Front Porch
V_FP=V_FP-V_Pos

# Calculate Vertical Back Porch
V_BP=V_Total-V_Res
V_BP=V_BP-V_Sync
V_BP=int(V_BP-V_FP)


hdmi_timings = "vcgencmd hdmi_timings %s 1 %s %s %s %s 1 %s %s %s 0 0 0 %s 0 %s 1" % (H_Res,H_FP,H_Sync,H_BP,V_Res,V_FP,V_Sync,V_BP,R_Rate,Pixel_Clock)
os.system(hdmi_timings)
os.system("tvservice -e \"DMT 87\"")
os.system("fbset -depth 8 && fbset -depth 16")
