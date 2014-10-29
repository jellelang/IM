# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 17:25:41 2014

@author: jelle
"""
import numpy as np
import pandas as pd
import csv
from physics import vp, dewpoint



def Delphin_intput(type_input,value):
    schrijf=open('T_sky.ccd', 'w')
    if type_input=='T_sky':
        schrijf=open('T_sky.ccd', 'w')
        schrijf.write('TC	C	 \n')	
    schrijf.write('\n')	
    for d in range(364):
       day=d
       for h in range (24):
         hour=h+1
         pos=day*24+hour
         if pos == len(Tsky):
             break
         schrijf.write('%0.0f %2.0f:%0.0f0:0%0.0f %3.4f\n' %(day,hour,0,0,value[pos]))
         if h == len(value): 
              break 
       if pos == len(value):
           break
    schrijf.flush()
    schrijf.close()