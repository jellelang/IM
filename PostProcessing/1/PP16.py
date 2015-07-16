# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 10:33:09 2014

Plot in de tijd, selectie van bepaalde zaken

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


basefile_name = 'F:/13/INPUT1' 
basefile= 'F:/13/'




N = len(design_grid)

N=287
# open file for result

# retrieve all the maximum moisture content levels at the middle height at the 
# interface between exterior panel and insulation 

max_MC=[]
MC_all=[]
results_cond=[]
M_max=[]
for i in range(len(design_grid)):       
        # open and read output file
        filename = basefile_name + '_%02d' % i
        folder = filename + '.results'        
        output_filename = folder + '/RV_B.out' 

        if os.path.exists(output_filename)==True:

            data=pd.read_csv(output_filename,skiprows=range(13), header=None,sep='\s+')
            # hier kan je dan bv zoeken hoever in de file het eigelijk begint        
            # s+ omdat er meerdere separtors zijn 
            data.columns=['TIJD', 'MC']  
            max_MC.append(data.MC.max())
            MC_all.append(data.MC)            
             
            #output_filename_max = folder + '/MC_WB.out' 
            #condens=pd.read_csv(output_filename_max,skiprows=range(13), header=None,sep='\s+')
            #results_cond.append(condens[1].max()) #[4]  range(8890)
            
            #output_filename_RH = folder + '/MC_WB.out' 
            #RH=pd.read_csv(output_filename_RH,skiprows=range(13), header=None,sep='\s+')
            #output_filename_T = folder + '/MC_WB.out' 
            #T=pd.read_csv(output_filename_T,skiprows=range(13), header=None,sep='\s+')
            
            #T=np.array(T[1])
            #RH=np.array(RH[1])
            #M=mould.mould(T,RH)
            #M_max.append(M.max())
        
[float(u) for u in range(8761)]

max_MC=pd.Series(max_MC)
MC_all=pd.Series(MC_all)
CONDENS=pd.Series(results_cond)


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
figure(figsize=(12, 9))  
  
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

# Verander de X-AS  
#yticks([0.1,0.2,0.3,0.4], [0.1,0.2,0.3,0.4], fontsize=14)  
xticks(range(0, 8760, 735), [x for x in ['S','O','N','D','J','F','M','A','M','J','J','A']], fontsize=14) 

grid_n=3

MC_allkgkg=MC_all

for i in range(len(MC_all)):
    plot(MC_allkgkg[i], lw=0.5, color=tableau20[1])

plot(MC_allkgkg[27], lw=2, color=tableau20[4], label='9mm 0.5m')   # groen  9
plot(MC_allkgkg[25], lw=2, color=tableau20[2], label='18mm 0.5m')    # orange   18
plot(MC_allkgkg[26], lw=2, color=tableau20[3], label='36mm 0.5m')   # light orange  36
plot(MC_allkgkg[23], lw=2, color=tableau20[5], label='60mm 0.5m')   # licht groen 60
plot(MC_allkgkg[24], lw=2, color=tableau20[6], label='80mm 0.5m')   # rood 80





leg=plt.legend(loc=4)
leg.get_frame().set_linewidth(0.0)


#    if design_grid['grid'][i]==grid_n and design_grid['LAMBDA_WIND_BARRIER'][i]==0.05 and design_grid['MEW_WIND_BARRIER'][i]==20:
#        if design_grid['MRC_WIND_BARRIER'][i]==2:
#            p=1
#        else:
#            plot(MC_allkgkg[i], lw=0.5, color=tableau20[4], label='3')
#    if design_grid['grid'][i]==grid_n and design_grid['LAMBDA_WIND_BARRIER'][i]==0.05 and  design_grid['MEW_WIND_BARRIER'][i]==40:
#        if design_grid['MRC_WIND_BARRIER'][i]==2:
#            p=1
#        else:
#            plot(MC_allkgkg[i], lw=0.5, color=tableau20[8], label='4')
#    if design_grid['grid'][i]==grid_n and design_grid['LAMBDA_WIND_BARRIER'][i]==0.05 and  design_grid['MEW_WIND_BARRIER'][i]==80:
#        if design_grid['MRC_WIND_BARRIER'][i]==2:
#            p=1
#        else:
#            plot(MC_allkgkg[i], lw=0.5, color=tableau20[10], label='4')
            
            
            
#plt.legend(frameon=False)

plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                labelbottom="on", left="off", right="off", labelleft="on")   


text(2000,35, "RELATIVE HUMIDITY (%) @ SURFACE ", fontsize=17, ha="left") 
savefig('C:/Users/jelle/Desktop/Masterclima_RH3.png', bbox_inches="tight")



#and design_grid['MRC_WIND_BARRIER'][i]==0
























