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

basefile_name = 'F:/13/INPUT1' 
basefile= 'F:/13/'


max_MC=[]
MC_all=[]
M_max=[]
for i in range(0,90):       
        # open and read output file
        filename = basefile_name + '_%02d' % i
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
max_MC=max_MC/270


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
n_groups = 10
#std_women = (3, 5, 2, 3, 3)
index = np.arange(n_groups)
bar_width = 0.15



#allemaal voor grid 5


#9mm    21->20
nine=pd.Series(numpy.zeros(10))
nine[4]=max_MC[20]
#60mm   22->21
max_MC[21]
sixty=pd.Series(numpy.zeros(10))
sixty[4]=max_MC[21]
#80mm   23->22
eighty=pd.Series(numpy.zeros(10))
eighty[4]=max_MC[22]


#60mm   24->23
d60_s=pd.Series(numpy.zeros(10))
d60_s[4]=max_MC[23]
#80mm   25->24
d80_s=pd.Series(numpy.zeros(10))
d80_s[4]=max_MC[24]
#18mm   26->25
d18_s=pd.Series(numpy.zeros(10))
d18_s[4]=max_MC[25]
#36mm   27->26
d36_s=pd.Series(numpy.zeros(10))
d36_s[4]=max_MC[26]
#9mm   28->27
d9_s=pd.Series(numpy.zeros(10))
d9_s[4]=max_MC[27]






opacity = 0.4
error_config = {'ecolor': '0.3'}

rects6 = plt.bar(index+0.05, d18_s, bar_width,
                 alpha=opacity,
                 color=tableau20[3],
                 #yerr=std_men, kun je gebruiken om onzekerheid op te zetten (stel dat je nog een parameter laat varieren)
                 error_kw=error_config,
                 label='18mm (+sd=0.5m)')  

rects7 = plt.bar(index + bar_width+0.05, d36_s, bar_width,
                 alpha=opacity,
                 color=tableau20[1],
                 #yerr=std_women, kun je gebruiken om onzekerheid op te zetten
                 error_kw=error_config,
                 label='36mm (+sd=0.5m)')

rects8 = plt.bar(index + bar_width*2+0.05, d9_s, bar_width,
                 alpha=opacity,
                 color=tableau20[6],
                 #yerr=std_women, kun je gebruiken om onzekerheid op te zetten
                 error_kw=error_config,
                 label='9mm (+sd=0.5m)')


rects9 = plt.bar(index + bar_width*3+0.05, d60_s, bar_width,
                 alpha=opacity,
                 color=tableau20[11],
                 #yerr=std_women, kun je gebruiken om onzekerheid op te zetten
                 error_kw=error_config,
                 label='60mm (+sd=0.5m)')
rects10 = plt.bar(index + bar_width*4+0.05, d80_s, bar_width,
                 alpha=opacity,
                 color=tableau20[9],
                 #yerr=std_women, kun je gebruiken om onzekerheid op te zetten
                 error_kw=error_config,
                 label='80mm (+sd=0.5m)')   




rects1 = plt.bar(index+0.05, max_MC[0:10], bar_width,
                 alpha=opacity,
                 color='g',
                 #yerr=std_men, kun je gebruiken om onzekerheid op te zetten (stel dat je nog een parameter laat varieren)
                 error_kw=error_config,
                 label='18mm')
rects2 = plt.bar(index + bar_width+0.05, max_MC[10:20], bar_width,
                 alpha=opacity,
                 color=tableau20[15],
                 #yerr=std_women, kun je gebruiken om onzekerheid op te zetten
                 error_kw=error_config,
                 label='36mm')
rects3 = plt.bar(index + bar_width*2+0.05, nine, bar_width,
                 alpha=opacity,
                 color=tableau20[17],
                 #yerr=std_women, kun je gebruiken om onzekerheid op te zetten
                 error_kw=error_config,
                 label='9mm')
rects4 = plt.bar(index + bar_width*3+0.05, sixty, bar_width,
                 alpha=opacity,
                 color=tableau20[6],
                 #yerr=std_women, kun je gebruiken om onzekerheid op te zetten
                 error_kw=error_config,
                 label='60mm')
rects5 = plt.bar(index + bar_width*4+0.05, eighty, bar_width,
                 alpha=opacity,
                 color=tableau20[12],
                 #yerr=std_women, kun je gebruiken om onzekerheid op te zetten
                 error_kw=error_config,
                 label='80mm')       
         
       
         
     
     
     
     
     
         
                 
plt.xlabel('leakages')
plt.ylabel('moisture content (kg/kg)')
plt.xticks(index + bar_width, ('1', '2', '3', '4', '5','6','7','8','9','10'))
leg=plt.legend(loc=2)
leg.get_frame().set_linewidth(0.0)
plt.tight_layout()
fig1.savefig('C:/Users/jelle/Desktop/test_MASTERCLIMAc.png',dpi=400)




























































