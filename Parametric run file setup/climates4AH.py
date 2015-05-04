# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 11:42:03 2011

@author: Jelle Langmans
"""


from __future__ import division
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from  numpy.random import randn
import  numpy.random as random
from pandas import Series, DataFrame
import math
import sys,os
direct_py='C:/PostDoc/Python' #'C:/JELLE'
direct_sim='C:/PostDoc/SIMULATIES' #'C:/JELLE'
path1=direct_py+ '/IM/Parametric run file setup'
path2=direct_py+ '/IM/BASICS'
path3=direct_py+ '/IM/Boundary_conditions'
path=path1
sys.path.append(path)
from definities import *
# laat toe om alle functie en classes die gedefinieerd zijn in BASICS te gebruiken
import sys,os
path=path2
sys.path.append(path)
path=path3
sys.path.append(path)
#from path import *
from physics import *
from Pvi_HIR import *
import climates
# import the module for calling external programs (creating subprocesses)
import subprocess
from datetime import datetime




Climate_columns=['s','T_ex','Dir','Dif','RH_e','Rav','Wsp','Wdi','CC','T_in','RHi','Ven','HPi','MPi']

DATA=pd.read_csv('C:/Users/jelle/Desktop/An-Heleen/noiseBE01m.cli', sep=',',skiprows=range(2))
name='noise'
DATA.columns=Climate_columns
      
Ta=DATA['T_ex']
c=DATA['CC']
DATA['T_sky']=Ta-(23.8-0.2*Ta)*(1-0.87*c) 
DATA['T_ground']=Ta



DATA['s']=pd.date_range(start='1/1/2001 00:00:00', end='31/12/2001 23:58:00', freq='MIN')
DATA.index=DATA['s']
DATA=DATA.resample('H')

path='C:/Users/jelle/Desktop/An-Heleen'
for type_input in ['T_sky','T_ground','RAD','T_ex','T_in'] :
    if type_input=='T_sky':
        schrijf=open(path+'/'+name+'_T_sky.ccd', 'w')
        schrijf.write('TC	C	 \n')	
        value=DATA['T_sky']
    if type_input=='T_ex':
        schrijf=open(path+'/'+name+'_T_ex.ccd', 'w')
        schrijf.write('TC	C	 \n')	
        value=DATA['T_ex']
    if type_input=='T_ground':
        schrijf=open(path+'/'+name+'_T_ground.ccd', 'w')
        schrijf.write('TC	C	 \n')
        value=DATA['T_ground']
    if type_input=='RAD':
        schrijf=open(path+'/'+name+'_RAD.ccd', 'w')
        schrijf.write('SHWRAD  W/m2\n')	 
        value=DATA['Dir']+DATA['Dif']
    if type_input=='T_in':
        schrijf=open(path+'/'+name+'_T_in.ccd', 'w')
        schrijf.write('TC	C	 \n')	 
        value=DATA['T_in']               
    schrijf.write('\n')
    for d in range(364):
       day=d
       for h in range (24):
         hour=h+1
         pos=day*24+hour
         if pos == len(value):
             break
         pos_shift=pos+5856
         if pos_shift>=8760:
             pos_shift=pos-(8760-5856)
         schrijf.write('%0.0f %2.0f:%0.0f0:0%0.0f %3.4f\n' %(day,hour,0,0,value[pos_shift]))
         if h == len(value): 
              break 
       if pos == len(value):
           break
    schrijf.flush()
    schrijf.close()


figure(figsize=(12, 7))  
plot(DATA['T_sky'])


          



###############################################################################
