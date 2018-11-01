#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 11:05:04 2018

@author: angoosh
"""

def glob():
    mode = "ABS"            #default mode for positioning 
    travel = 10.0             #default mode for travel in mm
    negtravel = -10.0         #default mode for negative travel in mm
    motorsteps = 200        #steps per rotation of used motor
    microstepping = 256     #supplied microstepping
    screwpitch = 4          #screw pitch in mm
    
    return mode, travel, negtravel, motorsteps, microstepping, screwpitch