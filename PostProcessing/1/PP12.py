# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 10:33:09 2014

PLOT IN TIJD VAN DE RV ACHTER DE DURIPANEL

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
sys.path.append('C:/PostDoc/Python/IM/PostProcessing')
import mould
from matplotlib import gridspec
import sys
path='C:/Program Files (x86)/MiKTeX 2.9/miktex/bin'
sys.path.append(path)


basefile_name = 'F:/10/INPUT1' 
basefile= 'F:/10/'




RH_1D=[]
RH_2D=[]


for i in range(1,35):       
        # open and read output file
        filename = basefile_name + '_%02d' % i
        folder = filename + '.results'        
          
        if i==21 :
            output_filename_rh = folder + '/RV_B.out'                       
            RH_1D=pd.read_csv(output_filename_rh,skiprows=range(13), header=None,sep='\s+')
            RH_1D.columns=['TIJD', 'RH']  
            RH_1D=RH_1D['RH']

        if i==22 :
            output_filename_rh = folder + '/RV_sarket_interior.out'            
            RH_2D=pd.read_csv(output_filename_rh,skiprows=range(8650), header=None,sep='\s+')
            RH_2D=RH_2D.drop(RH_2D.columns[[0]], axis=1)
            RH_2D_boven=RH_2D[RH_2D.columns[1]]
            RH_2D_onder=RH_2D[RH_2D.columns[38]]


tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
for i in range(len(tableau20)):  
    r, g, b = tableau20[i]  
    tableau20[i] = (r / 255., g / 255., b / 255.)  

 
  
  
# vb van individuele plot ifv tijd (grijs met dikker plot erop)
fig1=figure(figsize=(12, 9))  
  
# Remove the plot frame lines. They are unnecessary chartjunk.  
ax = subplot(111)  
ax.spines["top"].set_visible(False)  
ax.spines["bottom"].set_visible(False)  
ax.spines["right"].set_visible(False)  
ax.spines["left"].set_visible(False)    
  
# Ensure that the axis ticks only show up on the bottom and left of the plot.  
# Ticks on the right and top of the plot are generally unnecessary chartjunk.  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  

# Avoid unnecessary whitespace.  
#ylim(50, 500)  
xlim(0, 8760)  
ylim(55, 100)  


# Verander de X-AS  
#yticks([0.1,0.2,0.3,0.4], [0.1,0.2,0.3,0.4], fontsize=14)  
xticks(range(0, 8760, 735), [x for x in ['S','O','N','D','J','F','M','A','M','J','J','A']], fontsize=14) 



plot(RH_2D[RH_2D.columns[3]], lw=0.5, color=tableau20[1], label='2D_boven')
plot(RH_2D[RH_2D.columns[20]], lw=0.5, color=tableau20[5], label='2D_midden')
plot(RH_2D[RH_2D.columns[35]], lw=0.5, color=tableau20[10], label='2D_onder')

plot(RH_1D, lw=0.5, color='r', label='1D')


plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                labelbottom="on", left="off", right="off", labelleft="on")   


#text(2000,20, "MOISTURE CONTENT (KG/KG) @ SURFACE ", fontsize=17, ha="left") 



leg=plt.legend(loc=2)
leg.get_frame().set_linewidth(0.0)
plt.tight_layout()


fig1.savefig('C:/Users/jelle/Desktop/rh_1D.png',dpi=400)



#and design_grid['MRC_WIND_BARRIER'][i]==0
























