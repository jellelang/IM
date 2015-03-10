# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 17:25:41 2014

@author: jelle
"""
import numpy as np
import pandas as pd
import csv
from physics import vp, dewpoint



def climate_file(type_input,value):
    if type_input=='T_sky':
        schrijf=open('T_sky.ccd', 'w')
        schrijf.write('TC	C	 \n')	
    if type_input=='RH':
        schrijf=open('RH.ccd', 'w')
        schrijf.write('RH	---	 \n')	
        value=value/100
    if type_input=='Ta':
        schrijf=open('Ta.ccd', 'w')
        schrijf.write('TC	C	 \n')	
    if type_input=='RAD_NE':
        schrijf=open('RAD_shrt_NE.ccd', 'w')
        schrijf.write('SHWRAD  W/m2\n')	
    if type_input=='RAD_SW':
        schrijf=open('RAD_shrt_SW.ccd', 'w')
        schrijf.write('SHWRAD  W/m2\n')	
    if type_input=='PV':
        schrijf=open('PV.ccd', 'w')
        schrijf.write('VAPPRESS 	Pa\n')           
    schrijf.write('\n')	
    for d in range(364):
       day=d
       for h in range (24):
         hour=h+1
         pos=day*24+hour
         if pos == len(value):
             break
         schrijf.write('%0.0f %2.0f:%0.0f0:0%0.0f %3.4f\n' %(day,hour,0,0,value[pos]))
         if h == len(value): 
              break 
       if pos == len(value):
           break
    schrijf.flush()
    schrijf.close()
    