# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 10:33:09 2014

Color plots moisture, R en sd waarde: voor reeks 4 (eerste stap richting charts)

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
sys.path.append('C:/JELLE/IM/PostProcessing')
import mould
from matplotlib import gridspec
import sys
path='C:/Program Files (x86)/MiKTeX 2.9/miktex/bin'
sys.path.append(path)

basefile_name = 'C:/JELLE/PARAMETRIC/7/ INPUT1' 
basefile= 'C:/JELLE/PARAMETRIC/7/'

#INLEZEN VAN DE SIMULATIEGRID FILE
design_file=basefile+'INPUT1_designs.txt'
design_grid=pd.read_csv(design_file, skiprows=range(8),sep=',')
#drop first column
design_grid.drop(design_grid.columns[0],axis=1)


N = len(design_grid)

# open file for result

# retrieve all the maximum moisture content levels at the middle height at the 
# interface between exterior panel and insulation 

max_condens=[]
max_MC=[]
MC_all=[]
results_cond=[]
M_max=[]
R=[]
sd=[]
for i in range(len(design_grid)):       
        # open and read output file
        filename = basefile_name + '_%02d' % i
        folder = filename + '.results'        
        output_filename = folder + '/TOP_S.out' 
 


        if os.path.exists(output_filename)==True:
            data=pd.read_csv(output_filename,skiprows=range(13), header=None,sep='\s+')
            # hier kan je dan bv zoeken hoever in de file het eigelijk begint        
            # s+ omdat er meerdere separtors zijn 
            data.columns=['TIJD', 'MC']  
            max_MC.append(data.MC.max())
            MC_all.append(data.MC)            
        
            thick=0.018               
            R.append(thick/design_grid['LAMBDA_WIND_BARRIER'][i])
            sd.append(thick*design_grid['MEW_WIND_BARRIER'][i])

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
            max_MC.append(0.15*1200)
            MC_all.append(range(8761)) 
            R.append(0.36)
            sd.append(1.5)
        print('number %s' %i)
     
     
design_grid['R']=R    
design_grid['sd']=sd     

     

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
#



pos_grid0=np.repeat([False], len(design_grid)).tolist()
pos_grid1=np.repeat([False], len(design_grid)).tolist()
pos_grid2=np.repeat([False], len(design_grid)).tolist()
pos_grid3=np.repeat([False], len(design_grid)).tolist()
pos_grid4=np.repeat([False], len(design_grid)).tolist()
pos_grid5=np.repeat([False], len(design_grid)).tolist()
pos_grid6=np.repeat([False], len(design_grid)).tolist()
pos_grid7=np.repeat([False], len(design_grid)).tolist()
pos_grid8=np.repeat([False], len(design_grid)).tolist()
pos_grid9=np.repeat([False], len(design_grid)).tolist()


for i in range(len(design_grid)):
    if design_grid['grid'][i]==0 :
       pos_grid0[i]=True
    elif design_grid['grid'][i]==1:
       pos_grid1[i]=True
    elif design_grid['grid'][i]==2:
       pos_grid2[i]=True
    elif design_grid['grid'][i]==3: 
       pos_grid3[i]=True
    elif design_grid['grid'][i]==4:
       pos_grid4[i]=True
    elif design_grid['grid'][i]==5: 
       pos_grid5[i]=True
    elif design_grid['grid'][i]==6:
       pos_grid6[i]=True
    elif design_grid['grid'][i]==7: 
       pos_grid7[i]=True
    elif design_grid['grid'][i]==8:
       pos_grid8[i]=True
    elif design_grid['grid'][i]==9: 
       pos_grid9[i]=True




x=[]
y=[]
c1=[]
c2=[]
c3=[]
c4=[]
c5=[]
c6=[]
c7=[]
c8=[]
c9=[]


for i in range(len(design_grid)):
    if pos_grid0[i]==True:
        x.append(design_grid['sd'][i])
        y.append(design_grid['R'][i])
        c1.append(max_MC[i]/1200)
    if pos_grid1[i]==True:
        c2.append(max_MC[i]/1200)
    if pos_grid2[i]==True:
        c3.append(max_MC[i]/1200)
    if pos_grid3[i]==True:
        c4.append(max_MC[i]/1200)
    if pos_grid4[i]==True:
        c5.append(max_MC[i]/1200)
    if pos_grid5[i]==True:
        c6.append(max_MC[i]/1200)
    if pos_grid6[i]==True:
        c7.append(max_MC[i]/1200)
    if pos_grid7[i]==True:
        c8.append(max_MC[i]/1200)
    if pos_grid8[i]==True:
        c9.append(max_MC[i]/1200)






fig1 = plt.figure(figsize=(12, 20)) 
plt.rc('text', usetex=True)
plt.rc('font', family='sans-serif') 
font = {'fontname':'Arial', 'size':'20', 'color':'black', 'weight':'normal'}
font1 = {'fontname':'Arial', 'size':'16', 'color':'black', 'weight':'normal'}

v = np.linspace(0, 0.4, 100, endpoint=True)
grens=0.2

gs1 = gridspec.GridSpec(5,2)
gs1.update(top=0.9, bottom=0.1,left=0.1, right=0.9, wspace=0.55, hspace=0.55)   # wspace boven elkaar, hspace is naast elkaar

ax1 = plt.subplot(gs1[0:1, 0])
xx=pd.Series(x)
yy=pd.Series(y)
c1=pd.Series(c1)
x_un=xx.unique()
y_un=yy.unique()
X,Y=np.meshgrid(x_un,y_un)
VAL=np.reshape(c1, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,v,origin='lower')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'r',origin='lower',hold='on')
clabel(CS2,inline=True,fmt='%1.1f',fontsize=20,levels=[0.2],colors = 'r')
#CS=ax1.tricontourf(x,y,c1, v)
ylabel('R (K/m2/W)', **font)#
xlabel('sd (-)',**font)
xx=[0,0.3,0.6,0.9,1.2,1.5]
plt.xticks(xx,list(xx),**font)  
yy=[0,0.1,0.2,0.4]
plt.yticks(yy,list(yy),**font)  


ax2 = plt.subplot(gs1[1:2, 0])
xx=pd.Series(x)
yy=pd.Series(y)
c1=pd.Series(c1)
x_un=xx.unique()
y_un=yy.unique()
X,Y=np.meshgrid(x_un,y_un)
VAL=np.reshape(c2, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,v,origin='lower')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'r',origin='lower',hold='on')
clabel(CS2,inline=True,fmt='%1.1f',fontsize=20,levels=[0.2],colors = 'r')
#CS=ax1.tricontourf(x,y,c1, v)
#ax2.plot(x,y, 'ko ')
ylabel('R (K/m2/W)', **font)
xlabel('sd (-)',**font)
xx=[0,0.3,0.6,0.9,1.2,1.5]
plt.xticks(xx,list(xx),**font)  
yy=[0,0.1,0.2,0.4]
plt.yticks(yy,list(yy),**font)  
max_condens

ax3 = plt.subplot(gs1[2:3, 0])
xx=pd.Series(x)
yy=pd.Series(y)
c1=pd.Series(c1)
x_un=xx.unique()
y_un=yy.unique()
X,Y=np.meshgrid(x_un,y_un)
VAL=np.reshape(c3, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,v,origin='lower')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'r',origin='lower',hold='on')
clabel(CS2,inline=True,fmt='%1.1f',fontsize=20,levels=[0.2],colors = 'r')
#CS=ax1.tricontourf(x,y,c1, v)
#ax3.plot(x,y, 'ko ')
ylabel('R (K/m2/W)', **font)
xlabel('sd (-)',**font)
xx=[0,0.3,0.6,0.9,1.2,1.5]
plt.xticks(xx,list(xx),**font)  
yy=[0,0.1,0.2,0.4]
plt.yticks(yy,list(yy),**font)  

ax4 = plt.subplot(gs1[3:4, 0])
xx=pd.Series(x)
yy=pd.Series(y)
c1=pd.Series(c1)
x_un=xx.unique()
y_un=yy.unique()
X,Y=np.meshgrid(x_un,y_un)
VAL=np.reshape(c4, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,v,origin='lower')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'r',origin='lower',hold='on')
clabel(CS2,inline=True,fmt='%1.1f',fontsize=20,levels=[0.2],colors = 'r')
#CS=ax1.tricontourf(x,y,c1, v)
#ax4.plot(x,y, 'ko ')
ylabel('R (K/m2/W)', **font)
xlabel('sd (-)',**font)
xx=[0,0.3,0.6,0.9,1.2,1.5]
plt.xticks(xx,list(xx),**font)  
yy=[0,0.1,0.2,0.4]
plt.yticks(yy,list(yy),**font)  

ax5 = plt.subplot(gs1[4:5, 0])
xx=pd.Series(x)
yy=pd.Series(y)
c1=pd.Series(c1)
x_un=xx.unique()
y_un=yy.unique()
X,Y=np.meshgrid(x_un,y_un)
VAL=np.reshape(c5, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,v,origin='lower')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'r',origin='lower',hold='on')
clabel(CS2,inline=True,fmt='%1.1f',fontsize=20,levels=[0.2],colors = 'r')
#CS=ax1.tricontourf(x,y,c1, v)
#ax5.plot(x,y, 'ko ')
ylabel('R (K/m2/W)', **font)
xlabel('sd (-)',**font)
xx=[0,0.3,0.6,0.9,1.2,1.5]
plt.xticks(xx,list(xx),**font)  
yy=[0,0.1,0.2,0.4]
plt.yticks(yy,list(yy),**font)  


ax6 = plt.subplot(gs1[0:1, 1])
xx=pd.Series(x)
yy=pd.Series(y)
c1=pd.Series(c1)
x_un=xx.unique()
y_un=yy.unique()
X,Y=np.meshgrid(x_un,y_un)
VAL=np.reshape(c6, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,v,origin='lower')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'r',origin='lower',hold='on')
clabel(CS2,inline=True,fmt='%1.1f',fontsize=20,levels=[0.2],colors = 'r')
#CS=ax1.tricontourf(x,y,c1, v)
#ax6.plot(x,y, 'ko ')
ylabel('R (K/m2/W)', **font)
xlabel('sd (-)',**font)
xx=[0,0.3,0.6,0.9,1.2,1.5]
plt.xticks(xx,list(xx),**font)  
yy=[0,0.1,0.2,0.4]
plt.yticks(yy,list(yy),**font) 

ax7 = plt.subplot(gs1[1:2, 1])
xx=pd.Series(x)
yy=pd.Series(y)
c1=pd.Series(c1)
x_un=xx.unique()
y_un=yy.unique()
X,Y=np.meshgrid(x_un,y_un)
VAL=np.reshape(c7, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,v,origin='lower')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'r',origin='lower',hold='on')
clabel(CS2,inline=True,fmt='%1.1f',fontsize=20,levels=[0.2],colors = 'r')
#CS=ax1.tricontourf(x,y,c1, v)
#ax7.plot(x,y, 'ko ')
ylabel('R (K/m2/W)', **font)
xlabel('sd (-)',**font)
xx=[0,0.3,0.6,0.9,1.2,1.5]
plt.xticks(xx,list(xx),**font)  
yy=[0,0.1,0.2,0.4]
plt.yticks(yy,list(yy),**font) 

ax8 = plt.subplot(gs1[2:3, 1])
xx=pd.Series(x)
yy=pd.Series(y)
c1=pd.Series(c1)
x_un=xx.unique()
y_un=yy.unique()
X,Y=np.meshgrid(x_un,y_un)
VAL=np.reshape(c8, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,v,origin='lower')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'r',origin='lower',hold='on')
clabel(CS2,inline=True,fmt='%1.1f',fontsize=20,levels=[0.2],colors = 'r')
#CS=ax1.tricontourf(x,y,c1, v)
#ax8.plot(x,y, 'ko ')
ylabel('R (K/m2/W)', **font)
xlabel('sd (-)',**font)
xx=[0,0.3,0.6,0.9,1.2,1.5]
plt.xticks(xx,list(xx),**font)  
yy=[0,0.1,0.2,0.4]
plt.yticks(yy,list(yy),**font) 



ax9 = plt.subplot(gs1[3:4, 1])
xx=pd.Series(x)
yy=pd.Series(y)
c1=pd.Series(c1)
x_un=xx.unique()
y_un=yy.unique()
X,Y=np.meshgrid(x_un,y_un)
VAL=np.reshape(c9, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,v,origin='lower')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'r',origin='lower',hold='on')
clabel(CS2,inline=True,fmt='%1.1f',fontsize=20,levels=[0.2],colors = 'r')
#CS=ax1.tricontourf(x,y,c1, v)
#ax9.plot(x,y, 'ko ')
ylabel('R (K/m2/W)', **font)
xlabel('sd (-)',**font)
xx=[0,0.3,0.6,0.9,1.2,1.5]
plt.xticks(xx,list(xx),**font)  
yy=[0,0.1,0.2,0.4]
plt.yticks(yy,list(yy),**font) 



box = ax9.get_position()
axColor = plt.axes([0.58, 0.15, box.width, 0.05])

cbar = plt.colorbar(CS, cax = axColor, orientation="horizontal")
cbar.solids.set_edgecolor("face")
cbar.outline.set_visible(False)
cbar.ax.tick_params(labelsize=20)
mytks = [0, 0.1, 0.2, 0.3, 0.4]
cbar.set_ticks(mytks)
cbar.ax.set_yticklabels([str(a) for a in mytks], alpha=a)
cbar.set_label('Moisture content (kg/kg)', alpha=a, 
               rotation=0, fontsize=20, labelpad=20)
cbarytks = plt.getp(cbar.ax.axes, 'yticklines')
plt.setp(cbarytks, visible=False)

fig1.savefig('C:/Users/IM/Desktop/overzicht_4_MC_test.png',dpi=400)





cbar = plt.colorbar(CS, cax = axColor, orientation="horizontal")
cbar.solids.set_edgecolor("face")
cbar.outline.set_visible(False)
cbar.ax.tick_params(labelsize=30)
mytks = range(0,21,4)
cbar.set_ticks(mytks)
cbar.ax.set_yticklabels([str(a) for a in mytks], alpha=a)
cbar.set_label('Moisture content (kg/kg)', alpha=a, 
               rotation=0, fontsize=20, labelpad=20)
cbarytks = plt.getp(cbar.ax.axes, 'yticklines')
plt.setp(cbarytks, visible=False)



# create color bar
box = ax9.get_position()
# create color bar
axColor = plt.axes([0.58, 0.15, box.width, 0.05])
cb=colorbar(CS, cax = axColor, orientation="horizontal",label='condensation level (kg/m2)')
ax = cb.ax
text = ax.yaxis.label
font = matplotlib.font_manager.FontProperties(size=50)
text.set_font_properties(font)





grens=0.1
gr_min=0.1
gr_max=0.20

fig2 = plt.figure(figsize=(12, 14)) 

CS = plt.contourf(X,Y,VAL,[gr_min,gr_max],origin='lower')
CS2 = plt.contour(CS,levels=[grens],colors = 'g',origin='lower',hold='on')
clabel(CS2,inline=True,fmt='%1.1f',fontsize=20,levels=[0.2],colors = 'k')
ylabel('R (K/m2/W)', **font)
xlabel('sd (-)',**font)
plt.xticks(xx,list(xx),**font)  
plt.yticks(yy,list(yy),**font)  

c2=pd.Series(c2)
VAL=np.reshape(c2, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,[gr_min,gr_max],origin='lower',colors = 'g')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'k',origin='lower',hold='on')

c3=pd.Series(c3)
VAL=np.reshape(c3, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,[gr_min,gr_max],origin='lower',colors = 'g')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'k',origin='lower',hold='on')

c4=pd.Series(c4)
VAL=np.reshape(c4, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,[gr_min,gr_max],origin='lower',colors = 'r')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'k',origin='lower',hold='on')

c5=pd.Series(c5)
VAL=np.reshape(c5, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,[gr_min,gr_max],origin='lower')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'k',origin='lower',hold='on')

c6=pd.Series(c6)
VAL=np.reshape(c6, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,[gr_min,gr_max],origin='lower')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'k',origin='lower',hold='on')


c7=pd.Series(c7)
VAL=np.reshape(c7, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,[gr_min,gr_max],origin='lower')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'k',origin='lower',hold='on')

c8=pd.Series(c8)
VAL=np.reshape(c8, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,[gr_min,gr_max],origin='lower')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'k',origin='lower',hold='on')

c9=pd.Series(c9)
VAL=np.reshape(c9, (len(y_un),len(x_un)),order='F')
CS = plt.contourf(X,Y,VAL,[gr_min,gr_max],origin='lower')
CS2 = plt.contour(CS,v, levels=[grens],colors = 'k',origin='lower',hold='on')


fig2.savefig('C:/Users/jelle/Desktop/contour_grid5_t.png',dpi=400)




























