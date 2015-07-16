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

basefile_name = 'F:/12/INPUT1' 
basefile_name1 = 'F:/12/ INPUT1' 

basefile= 'F:/12/'


max_MC=[]
MC_all=[]
M_max=[]
for i in range(0,90):       
        # open and read output file
        filename = basefile_name + '_%02d' % i
        folder = filename + '.results'        
        output_filename = folder + '/TOP_S.out' 
        
        filename1 = basefile_name1 + '_%02d' % i
        folder1 =filename1 + '.results'        
        output_filename1 = folder1 + '/TOP_S.out' 

        if os.path.exists(output_filename)==True:
            data=pd.read_csv(output_filename,skiprows=range(13), header=None,sep='\s+')
            data.columns=['TIJD', 'MC']  
            max_MC.append(data.MC.max())
            MC_all.append(data.MC)      
        if os.path.exists(output_filename1)==True:
            data=pd.read_csv(output_filename1,skiprows=range(13), header=None,sep='\s+')
            data.columns=['TIJD', 'MC']  
            max_MC.append(data.MC.max())
            MC_all.append(data.MC)  
        print('number %s' %i)
     
max_MC=pd.Series(max_MC)


# DURIPANEL MET ISOLATIE
max_MC=max_MC/1290




basefile_name = 'F:/10/INPUT1' 
max_MC1=[]
MC_all1=[]
for i in range(1,10):       
        # open and read output file
        filename = basefile_name + '_%02d' % i
        folder = filename + '.results'        
        output_filename = folder + '/TOP_S.out' 
        if os.path.exists(output_filename)==True:
            data1=pd.read_csv(output_filename,skiprows=range(13), header=None,sep='\s+')
            data1.columns=['TIJD', 'MC']  
            max_MC1.append(data1.MC.max())
            MC_all1.append(data1.MC)            
        print('number %s' %i)
    
max_MC1=pd.Series(max_MC1)


# DURIPANEL
max_MC1[0:10]=max_MC1[0:10]/1290






file_result = 'F:/12/INPUT1_04_10.results/TOP_S.out' 
max_MC10=[]
MC_all10=[]
data10=pd.read_csv(file_result,skiprows=range(13), header=None,sep='\s+')
data10.columns=['TIJD', 'MC']  
max_MC10.append(data10.MC.max())

file_result = 'F:/12/INPUT1_40_10.results/TOP_S.out' 
data10=pd.read_csv(file_result,skiprows=range(13), header=None,sep='\s+')
data10.columns=['TIJD', 'MC']  
max_MC10.append(data10.MC.max())

file_result = 'F:/12/INPUT1_76_10.results/TOP_S.out' 
data10=pd.read_csv(file_result,skiprows=range(13), header=None,sep='\s+')
data10.columns=['TIJD', 'MC']  
max_MC10.append(data10.MC.max())

max_MC10=pd.Series(max_MC10)/1290




tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
for i in range(len(tableau20)):  
    r, g, b = tableau20[i]  
    tableau20[i] = (r / 255., g / 255., b / 255.)  



#max_duripanel = max_MC[0:10]
#max_hydropanel = max_MC[10:20]
#max_weatherdefence = max_MC[20:30]
#
#max_duripanelAmax= max_MC[30:40]
#max_duripanelAmax.index=max_duripanel.index
#max_duripanelAmin= max_MC[40:50]
#max_duripanelAmin.index=max_duripanel.index
#max_duripanelmhumax= max_MC[50:60]
#max_duripanelmhumax.index=max_duripanel.index
#max_duripanelmhumin= max_MC[60:70]
#max_duripanelmhumin.index=max_duripanel.index



fig1 = plt.figure(figsize=(8, 6)) 
n_groups = 9
#std_women = (3, 5, 2, 3, 3)
index = np.arange(n_groups)
bar_width = 0.15





opacity = 0.4
error_config = {'ecolor': '0.3'}
rects1 = plt.bar(index+0.05, max_MC[0:9], bar_width,
                 alpha=opacity,
                 color='g',
                 #yerr=std_men, kun je gebruiken om onzekerheid op te zetten (stel dat je nog een parameter laat varieren)
                 error_kw=error_config,
                 label='6cm')
rects2 = plt.bar(index + bar_width+0.05, max_MC[9:18], bar_width,
                 alpha=opacity,
                 color=tableau20[15],
                 #yerr=std_women, kun je gebruiken om onzekerheid op te zetten
                 error_kw=error_config,
                 label='4cm')
rects3 = plt.bar(index + bar_width*2+0.05,max_MC[18:27], bar_width,
                 alpha=opacity,
                 color='b',
                 #yerr=std_women, kun je gebruiken om onzekerheid op te zetten
                 error_kw=error_config,
                 label='2cm')
rects4 = plt.bar(index + bar_width*3+0.05,max_MC1[0:9], bar_width,
                 alpha=opacity,
                 color='R',
                 #yerr=std_women, kun je gebruiken om onzekerheid op te zetten
                 error_kw=error_config,
                 label='0cm')                 
                 
                 
plt.xlabel('leakages')
plt.ylabel('moisture content (kg/kg)')
plt.xticks(index + bar_width, ('1', '2', '3', '4', '5','6','7','8','9'))
leg=plt.legend(loc=2)
leg.get_frame().set_linewidth(0.0)
plt.tight_layout()
fig1.savefig('C:/Users/jelle/Desktop/test1.png',dpi=400)




























































