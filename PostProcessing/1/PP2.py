# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 10:33:09 2014

Color plots

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


basefile_name = 'F:/2/INPUT1' 
basefile= 'F:/2/'

#INLEZEN VAN DE SIMULATIEGRID FILE
design_file=basefile+'INPUT1_designs.txt'
design_grid=pd.read_csv(design_file, skiprows=range(8),sep=',')
#drop first column
design_grid.drop(design_grid.columns[0],axis=1)


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
        output_filename = folder + '/MIDDLE_S.out' 

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
        else:
            max_MC.append(5)
            MC_all.append(range(8761))  
        print('number %s' %i)
        

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

 
  
  
# OPMAAK PLOT

#colors = np.random.rand(N)
#area = np.ones(N)*60  
#plt.scatter(x, y, s=area, c, alpha=0.7, linewidths=0)
#plt.colorbar()
#plt.show()




pos_MRC0=[] 
pos_MRC1=[] 
pos_MRC2=[] 
pos_MRC3=[] 
x=[]
y=[]
for i in range(len(design_grid)):
    if design_grid['grid'][i]==5 and design_grid['MRC_WIND_BARRIER'][i]==0:
       pos_MRC0.append(True)
       pos_MRC1.append(False)
       pos_MRC2.append(False)
       pos_MRC3.append(False)
    elif design_grid['grid'][i]==5 and design_grid['MRC_WIND_BARRIER'][i]==1:
       pos_MRC0.append(False)
       pos_MRC1.append(True)
       pos_MRC2.append(False)
       pos_MRC3.append(False)
    elif design_grid['grid'][i]==5 and design_grid['MRC_WIND_BARRIER'][i]==2:
       pos_MRC0.append(False)
       pos_MRC1.append(False)
       pos_MRC2.append(True)
       pos_MRC3.append(False)
    elif design_grid['grid'][i]==5 and design_grid['MRC_WIND_BARRIER'][i]==3:
       pos_MRC0.append(False)
       pos_MRC1.append(False)
       pos_MRC2.append(False)
       pos_MRC3.append(True)
    else:
       pos_MRC0.append(False)
       pos_MRC1.append(False)
       pos_MRC2.append(False)
       pos_MRC3.append(False)


x = design_grid['MEW_WIND_BARRIER'][pos_MRC0]
y = design_grid['LAMBDA_WIND_BARRIER'][pos_MRC0]
c_MRC0=max_MC[pos_MRC0]
c_MRC1=max_MC[pos_MRC1]
c_MRC2=max_MC[pos_MRC2]
c_MRC3=max_MC[pos_MRC3]



x_un=x.unique()
y_un=y.unique()
X, Y = np.meshgrid(x_un, y_un)
c_un_MRC0=np.array(c_MRC0)/1200
c_un_MRC1=np.array(c_MRC1)/1200
c_un_MRC2=np.array(c_MRC2)/1200
c_un_MRC3=np.array(c_MRC3)/1200

C_MRC0=c_un_MRC0.reshape(len(y_un),len(x_un),order='F')
C_MRC1=c_un_MRC1.reshape(len(y_un),len(x_un),order='F')
C_MRC2=c_un_MRC2.reshape(len(y_un),len(x_un),order='F') 
C_MRC3=c_un_MRC3.reshape(len(y_un),len(x_un),order='F')





fig1 = plt.figure(figsize=(12, 14)) 
plt.rc('text', usetex=True)
plt.rc('font', family='sans-serif') 
font = {'fontname':'Arial', 'size':'20', 'color':'black', 'weight':'normal'}
font1 = {'fontname':'Arial', 'size':'16', 'color':'black', 'weight':'normal'}

v = np.linspace(0.01, 0.4, 50, endpoint=True)


gs1 = gridspec.GridSpec(2,1)
gs1.update(top=0.98, bottom=0.2,left=0.1, right=0.45, wspace=0.16, hspace=0.16)   # wspace boven elkaar, hspace is naast elkaar

ax1 = plt.subplot(gs1[0:1, 0])
CS=ax1.contourf(X, Y, C_MRC0,v)
ylabel('$\lambda$', **font)
xlabel('$\mu$',**font)
x=[5,20,40,80]
plt.xticks(x,list(x),**font)  
y=[0.05,0.1,0.2]
plt.yticks(y,list(y),**font)  


ax2 = plt.subplot(gs1[1:2, 0])
CS=ax2.contourf(X, Y, C_MRC1,v)
ylabel('$\lambda$', **font)
xlabel('$\mu$',**font)
plt.xticks(x,list(x),**font)  
y=[0.05,0.1,0.2]
plt.yticks(y,list(y),**font)  


gs2 = gridspec.GridSpec(1,1)
gs2.update(top=0.98, bottom=0.618, left=0.55, right=0.9, wspace=0.16, hspace=0.16)   # wspace boven elkaar, hspace is naast elkaar
ax3 = plt.subplot(gs2[0, 0])
CS=ax3.contourf(X, Y, C_MRC2,v)
ylabel('$\lambda$', **font)
xlabel('$\mu$',**font)
plt.xticks(x,list(x),**font)  
y=[0.05,0.1,0.2]
plt.yticks(y,list(y),**font)  


gs3 = gridspec.GridSpec(1,1)
gs3.update(top=0.561, bottom=0.2, left=0.55, right=0.98, wspace=0.16, hspace=0.16)   # wspace boven elkaar, hspace is naast elkaar

ax4 = plt.subplot(gs3[0,0])
CS=ax4.contourf(X, Y, C_MRC3,v)
ylabel('$\lambda$', **font)
xlabel('$\mu$',**font)
colorbar(CS)
plt.xticks(x,list(x),**font)  
y=[0.05,0.1,0.2]
plt.yticks(y,list(y),**font)  


text(-65, 0.3, "MRC DURI", fontsize=17, ha="left") 
text(30, 0.3, "MRC NO BUFFER", fontsize=17, ha="left") 
text(-65, 0.12, "MRC HYDRO", fontsize=17, ha="left") 
text(30, 0.12, "MRC3 MENUI", fontsize=17, ha="left") 



fig1.savefig('C:/Users/jelle/Desktop/contour_grid5_t.png',dpi=400)




























