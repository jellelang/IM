# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 10:33:09 2014

Bar charts met mc voor simulatierun 10 (Duripanel, Hydropanel, Weatherdefence)

@author: jelle
"""

import os.path


import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import matplotlib
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import scipy.ndimage
from pylab import meshgrid,cm,imshow,contour,clabel,colorbar,axis,title,show
sys.path.append('C:/PostDoc/Python/IM/PostProcessing')
import mould
from matplotlib import gridspec
import sys
path='C:/Program Files (x86)/MiKTeX 2.9/miktex/bin'
sys.path.append(path)

basefile_name = 'F:/14/INPUT1' 
basefile= 'F:/14/'


max_MC=[]
MC_all=[]
M_max=[]
for i in range(1,90):       
        # open and read output file
        filename = basefile_name + '_%01d' % i
        folder = filename + '.results'        
        output_filename = folder + '/TOP_S.out' 
        if os.path.exists(output_filename)==True:
            data=pd.read_csv(output_filename,skiprows=range(13), header=None,sep='\s+')
            data.columns=['TIJD', 'MC']  
            max_MC.append(data.MC.max())
            MC_all.append(data.MC)      

        print('number %s' %i)
     
max_MC=pd.Series(max_MC)


# DURIPANEL MET ISOLATIE
max_MC=max_MC/1270


tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
for i in range(len(tableau20)):  
    r, g, b = tableau20[i]  
    tableau20[i] = (r / 255., g / 255., b / 255.)  




fig1 = plt.figure(figsize=(8, 6)) 
n_groups = 3
#std_women = (3, 5, 2, 3, 3)
index = np.arange(n_groups)
bar_width = 0.45

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = plt.bar(index, max_MC[0:3], bar_width,
                 alpha=opacity,
                 color='g',
                 #yerr=std_men, kun je gebruiken om onzekerheid op te zetten (stel dat je nog een parameter laat varieren)
                 error_kw=error_config,
                 label='Duripanel 18mm')



text(0.05,0.15, '1.10-9 m^2', fontsize=12)
text(0.05,0.12, '30 kg/m^3', fontsize=12)

             
text(1.05,0.27, '4.10-8 m^2', fontsize=12)
text(1.05,0.24, '40 kg/m^3', fontsize=12)

             
text(2.05,0.16, '3.10-9 m^2', fontsize=12)
text(2.05,0.12, '35 kg/m^3', fontsize=12)
   
   
plt.ylabel('moisture content (kg/kg)')
plt.xticks(index +bar_width/2, ('Glass wool', 'Rockwool', 'Cellulose'))
leg=plt.legend(loc=2)
leg.get_frame().set_linewidth(0.0)
plt.tight_layout()
fig1.savefig('C:/Users/jelle/Desktop/blown-in.png',dpi=400)




























































