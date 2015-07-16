# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 10:33:09 2014

Bar charts met condensation voor simulatierun 10 (Duripanel, Hydropanel, Weatherdefence)

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

basefile_name = 'F:/10/INPUT1' 
basefile= 'F:/10/'


max_condens=[]
max_MC=[]
MC_all=[]
results_cond=[]
M_max=[]

for i in range(1,71):       
        # open and read output file
        filename = basefile_name + '_%02d' % i
        folder = filename + '.results'        
        output_filename_cav = folder + '/cavity.out' 
        output_filename_mw1 = folder + '/MW1.out' 
        output_filename_mw2 = folder + '/MW2.out' 
        output_filename_mw3 = folder + '/MW3.out' 


        if True==True:
            
            if i==1 or i==11 or i==21 or i==31 or i==41 or i==51 or i==61 :
                data1=pd.read_csv(output_filename_mw1,skiprows=range(13), header=None,sep='\s+')
                data=data1*0.0027

            if i==2 or i==12 or i==22 or i==32 or i==42 or i==52 or i==62 :
                data1=pd.read_csv(output_filename_mw1,skiprows=range(8650), header=None,sep='\s+')
                data2=pd.read_csv(output_filename_mw2,skiprows=range(8650), header=None,sep='\s+')
                data3=pd.read_csv(output_filename_mw3,skiprows=range(8650), header=None,sep='\s+')
                data1=data1.drop(data1.columns[[0]], axis=1)
                data2=data1.drop(data1.columns[[0]], axis=1)
                data3=data1.drop(data1.columns[[0]], axis=1)
                data=data1*0.00526+data2*0.00526+data3*0.00526
                
            if i==3 or i==13 or i==23 or i==33 or i==43 or i==53 or i==63 :
                data1=pd.read_csv(output_filename_cav,skiprows=range(8883), header=None,sep='\s+')
                data2=pd.read_csv(output_filename_mw1,skiprows=range(8883), header=None,sep='\s+')
                data3=pd.read_csv(output_filename_mw2,skiprows=range(8883), header=None,sep='\s+')
                data4=pd.read_csv(output_filename_mw3,skiprows=range(8883), header=None,sep='\s+')
                data1=data1.drop(data1.columns[[0]], axis=1)
                data2=data1.drop(data1.columns[[0]], axis=1)
                data3=data1.drop(data1.columns[[0]], axis=1)
                data=data1*0.001+data2*0.00526+data3*0.00526+data4*0.00526
           
            if i==4 or i==14 or i==24 or i==34 or i==44 or i==54 or i==64 :
                data1=pd.read_csv(output_filename_cav,skiprows=range(8883), header=None,sep='\s+')
                data2=pd.read_csv(output_filename_mw1,skiprows=range(8883), header=None,sep='\s+')
                data3=pd.read_csv(output_filename_mw2,skiprows=range(8883), header=None,sep='\s+')
                data4=pd.read_csv(output_filename_mw3,skiprows=range(8883), header=None,sep='\s+')
                data1=data1.drop(data1.columns[[0]], axis=1)
                data2=data1.drop(data1.columns[[0]], axis=1)
                data3=data1.drop(data1.columns[[0]], axis=1)
                data=data1*0.003+data2*0.00526+data3*0.00526+data4*0.00526

            if i==5 or i==15 or i==25 or i==35 or i==45 or i==55 or i==65 :
                data1=pd.read_csv(output_filename_cav,skiprows=range(8883), header=None,sep='\s+')
                data2=pd.read_csv(output_filename_mw1,skiprows=range(8883), header=None,sep='\s+')
                data3=pd.read_csv(output_filename_mw2,skiprows=range(8883), header=None,sep='\s+')
                data4=pd.read_csv(output_filename_mw3,skiprows=range(8883), header=None,sep='\s+')
                data1=data1.drop(data1.columns[[0]], axis=1)
                data2=data1.drop(data1.columns[[0]], axis=1)
                data3=data1.drop(data1.columns[[0]], axis=1)
                data4=data1.drop(data1.columns[[0]], axis=1)
                data=data1*0.005+data2*0.00526+data3*0.00526+data4*0.00526

            if i==6 or i==16 or i==26 or i==36 or i==46 or i==56 or i==66 :
                data1=pd.read_csv(output_filename_cav,skiprows=range(8767), header=None,sep='\s+')
                data2=pd.read_csv(output_filename_mw1,skiprows=range(8767), header=None,sep='\s+')
                data3=pd.read_csv(output_filename_mw2,skiprows=range(8767), header=None,sep='\s+')
                data4=pd.read_csv(output_filename_mw3,skiprows=range(8767), header=None,sep='\s+')
                data1=data1.drop(data1.columns[[0]], axis=1)
                data2=data1.drop(data1.columns[[0]], axis=1)
                data3=data1.drop(data1.columns[[0]], axis=1)
                data4=data1.drop(data1.columns[[0]], axis=1)
                data=data1*0.005+data2*0.00526+data3*0.00526+data4*0.00526
            if i==7 or i==17 or i==27 or i==37 or i==47 or i==57 or i==67 :
                data1=pd.read_csv(output_filename_cav,skiprows=range(8770), header=None,sep='\s+')
                data2=pd.read_csv(output_filename_mw1,skiprows=range(8770), header=None,sep='\s+')
                data3=pd.read_csv(output_filename_mw2,skiprows=range(8770), header=None,sep='\s+')
                data4=pd.read_csv(output_filename_mw3,skiprows=range(8770), header=None,sep='\s+')
                data1=data1.drop(data1.columns[[0]], axis=1)
                data2=data1.drop(data1.columns[[0]], axis=1)
                data3=data1.drop(data1.columns[[0]], axis=1)
                data4=data1.drop(data1.columns[[0]], axis=1)
                data=data1*0.005+data2*0.00526+data3*0.00526+data4*0.00526

            if i==8 or i==18 or i==28 or i==38 or i==48 or i==58 or i==68 :
                data1=pd.read_csv(output_filename_cav,skiprows=range(8770), header=None,sep='\s+')
                data2=pd.read_csv(output_filename_mw1,skiprows=range(8770), header=None,sep='\s+')
                data3=pd.read_csv(output_filename_mw2,skiprows=range(8770), header=None,sep='\s+')
                data4=pd.read_csv(output_filename_mw3,skiprows=range(8770), header=None,sep='\s+')
                data1=data1.drop(data1.columns[[0]], axis=1)
                data2=data1.drop(data1.columns[[0]], axis=1)
                data3=data1.drop(data1.columns[[0]], axis=1)
                data4=data1.drop(data1.columns[[0]], axis=1)
                data=data1*0.005+data2*0.00526+data3*0.00526+data4*0.00526

            if i==9 or i==19 or i==29 or i==39 or i==49 or i==59 or i==69 :
                data1=pd.read_csv(output_filename_cav,skiprows=range(8884), header=None,sep='\s+')
                data2=pd.read_csv(output_filename_mw1,skiprows=range(8884), header=None,sep='\s+')
                data3=pd.read_csv(output_filename_mw2,skiprows=range(8884), header=None,sep='\s+')
                data4=pd.read_csv(output_filename_mw3,skiprows=range(8884), header=None,sep='\s+')
                data1=data1.drop(data1.columns[[0]], axis=1)
                data2=data1.drop(data1.columns[[0]], axis=1)
                data3=data1.drop(data1.columns[[0]], axis=1)
                data4=data1.drop(data1.columns[[0]], axis=1)
                data=data1*0.005+data2*0.00526+data3*0.00526+data4*0.00526
   
            if i==10 or i==20 or i==30 or i==40 or i==50 or i==60 or i==70 :
                data1=pd.read_csv(output_filename_cav,skiprows=range(8884), header=None,sep='\s+')
                data2=pd.read_csv(output_filename_mw1,skiprows=range(8884), header=None,sep='\s+')
                data3=pd.read_csv(output_filename_mw2,skiprows=range(8884), header=None,sep='\s+')
                data4=pd.read_csv(output_filename_mw3,skiprows=range(8884), header=None,sep='\s+')
                data1=data1.drop(data1.columns[[0]], axis=1)
                data2=data1.drop(data1.columns[[0]], axis=1)
                data3=data1.drop(data1.columns[[0]], axis=1)
                data4=data1.drop(data1.columns[[0]], axis=1)
                data=data1*0.005+data2*0.00526+data3*0.00526+data4*0.00526

            if i==1 or i==11 or i==21 or i==31 or i==41 or i==51 or i==61 :
                data.columns=['TIJD', 'condens']  
                max_condens.append(data.condens.max())
                del data
            else: 
                data = data.max(axis=1)
                maxx=data.max()
                max_condens.append(maxx)
                del data                 
               
               
               
               
        print('number %s' %i)

                     
max_condens=pd.Series(max_condens)






tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
for i in range(len(tableau20)):  
    r, g, b = tableau20[i]  
    tableau20[i] = (r / 255., g / 255., b / 255.)  





max_duripanel = max_condens[0:10]
max_hydropanel = max_condens[10:20]
max_weatherdefence = max_condens[20:30]

max_duripanelAmax=max_condens[30:40]
max_duripanelAmax.index=max_duripanel.index
max_duripanelAmin=max_condens[40:50]
max_duripanelAmin.index=max_duripanel.index
max_duripanelmhumax=max_condens[50:60]
max_duripanelmhumax.index=max_duripanel.index
max_duripanelmhumin=max_condens[60:70]
max_duripanelmhumin.index=max_duripanel.index






fig1 = plt.figure(figsize=(8, 6)) 

n_groups = 10




#std_women = (3, 5, 2, 3, 3)

index = np.arange(n_groups)
bar_width = 0.25

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = plt.bar(index+0.05, max_duripanel, bar_width,
                 alpha=opacity,
                 color='g',
                 error_kw=error_config,
                 label='Duripanel')

rects2 = plt.bar(index + bar_width+0.05, max_hydropanel, bar_width,
                 alpha=opacity,
                 color=tableau20[15],
                 error_kw=error_config,
                 label='Hydropanel')

rects3 = plt.bar(index + bar_width*2+0.05, max_weatherdefence, bar_width,
                 alpha=opacity,
                 color='b',
                 error_kw=error_config,
                 label='Weatherdefence')

plt.xlabel('leakages')
plt.ylabel('max. accumulated condensation (kg/m2)')
plt.xticks(index + bar_width, ('1', '2', '3', '4', '5','6','7','8','9','10'))
leg=plt.legend(loc=2)
leg.get_frame().set_linewidth(0.0)
plt.tight_layout()

ylim(0, 3)  


fig1.savefig('C:/Users/jelle/Desktop/condensation.png',dpi=400)










minmax_A=[max_duripanel-max_duripanelAmax, max_duripanelAmin-max_duripanel]
minmax_mhu=[max_duripanel-max_duripanelmhumax, max_duripanelmhumin-max_duripanel]


fig2 = plt.figure(figsize=(8, 6)) 
n_groups = 10
#std_women = (3, 5, 2, 3, 3)
index = np.arange(n_groups)
bar_width = 0.25

opacity = 0.4
error_config = {'ecolor': '0.3'}
rects1 = plt.bar(index+0.05, max_duripanel, bar_width,
                 alpha=opacity,
                 color='g',
                 yerr=minmax_mhu,
                 error_kw=error_config,
                 label='Duripanel')
rects2 = plt.bar(index + bar_width+0.05, max_hydropanel, bar_width,
                 alpha=opacity,
                 color=tableau20[15],
                 #yerr=std_women, kun je gebruiken om onzekerheid op te zetten
                 error_kw=error_config,
                 label='Hydropanel')
rects3 = plt.bar(index + bar_width*2+0.05, max_weatherdefence, bar_width,
                 alpha=opacity,
                 color='b',
                 #yerr=std_women, kun je gebruiken om onzekerheid op te zetten
                 error_kw=error_config,
                 label='Weatherdefence')
plt.xlabel('leakages')
plt.ylabel('max. accumulated condensation (kg/m2)')
plt.xticks(index + bar_width, ('1', '2', '3', '4', '5','6','7','8','9','10'))
leg=plt.legend(loc=2)
leg.get_frame().set_linewidth(0.0)
plt.tight_layout()
ylim(0, 3)  

fig2.savefig('C:/Users/jelle/Desktop/test1_mhu.png',dpi=400)



















































