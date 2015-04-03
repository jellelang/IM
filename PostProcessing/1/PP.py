# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 10:33:09 2014

@author: jelle
"""





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


basefile_name = 'C:/PostDoc/SIMULATIES/PARAMETRIC/1/INPUT1' 
basefile_name2 = 'C:/JELLE/SIMULATIES/INPUT5'
basefile= 'C:/PostDoc/SIMULATIES/PARAMETRIC/1/'

#INLEZEN VAN DE SIMULATIEGRID FILE
design_file=basefile+'INPUT1_designs.txt'
design_grid=pd.read_csv(design_file, skiprows=range(8),sep=',')
#drop first column
design_grid.drop(design_grid.columns[0],axis=1)


N = len(design_grid)

# open file for result

# retrieve all the maximum moisture content levels at the middle height at the 
# interface between exterior panel and insulation 

max_MC=[]
MC_all=[]
results_cond=[]
M_max=[]
for i in range(N):       
        # open and read output file
        filename = basefile_name + '_%02d' % i
        folder = filename + '.results'        
        output_filename = folder + '/MC_WB_MW.out' 
        data=pd.read_csv(output_filename,skiprows=range(13), header=None,sep='\s+')
        # hier kan je dan bv zoeken hoever in de file het eigelijk begint        
        # s+ omdat er meerdere separtors zijn 
        data.columns=['TIJD', 'MC']  
        max_MC.append(data.MC.max())
        MC_all.append(data.MC)
        
        output_filename_max = folder + '/CONDENSATION.out' 
        condens=pd.read_csv(output_filename_max,skiprows=range(13), header=None,sep='\s+')
        results_cond.append(condens[1].max()) #[4]  range(8890)

        output_filename_RH = folder + '/RH_WB_MW.out' 
        RH=pd.read_csv(output_filename_RH,skiprows=range(13), header=None,sep='\s+')
        output_filename_T = folder + '/TC_WB_MW.out' 
        T=pd.read_csv(output_filename_T,skiprows=range(13), header=None,sep='\s+')

        T=np.array(T[1])
        RH=np.array(RH[1])
        #M=mould.mould(T,RH)
        #M_max.append(M.max())
        print('number %s' %i)
        






tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
for i in range(len(tableau20)):  
    r, g, b = tableau20[i]  
    tableau20[i] = (r / 255., g / 255., b / 255.)  

 
  
  
# You typically want your plot to be ~1.33x wider than tall. This plot is a rare  
# exception because of the number of lines being plotted on it.  
# Common sizes: (10, 7.5) and (12, 9)   
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

# Limit the range of the plot to only where the data is.  
# Avoid unnecessary whitespace.  
ylim(50, 500)  
xlim(0, 8760)  


# Verander de X-AS  
yticks(range(0, 501, 100), [str(x) + "%" for x in range(0, 501, 100)], fontsize=14)  
xticks(range(0, 8760, 735), [x for x in ['S','O','N','D','J','F','M','A','M','J','J','A']], fontsize=14) 
  
# Provide tick lines across the plot to help your viewers trace along  
# the axis ticks. Make sure that the lines are light and small so they  
# don't obscure the primary data lines.  
for y in range(100, 501, 100):  
    plot(range(0, 8760), [y] * len(range(0, 8760)), "--", lw=0.5, color="black", alpha=0.3)  
  
# Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
plt.tick_params(axis="both", which="both", bottom="off", top="off",  
                labelbottom="on", left="off", right="off", labelleft="on")   
  
 

for i in range(N):
    plot(MC_all[i], lw=0.5, color=tableau20[15])

plot(MC_all[1], lw=2.5, color=tableau20[4])
plot(MC_all[350], lw=2.5, color=tableau20[6])



text(10, 480, "     INTERSTITIAL CONDENSATION WITHIN STRUCTURE", fontsize=17, ha="left") 
savefig("C:/Users/jelle/Desktop/test_figure.png", bbox_inches="tight")





      
# construct DataFrame with a) lambda b) MEW c) Max_mc

overview = pd.read_csv(basefile_name2 + '_variation.txt',sep='\s+')
overview = overview[0:N+1]
overview['MC_max']=results

        
x = overview['MEW']
y = overview['LAMBDA']
c=results_cond    #overview['MC_max']
mold=M_max
mc=overview['MC_max']


#colors = np.random.rand(N)
area = np.ones(N)*60  
#plt.scatter(x, y, s=area, c, alpha=0.7, linewidths=0)
#plt.colorbar()
#plt.show()


# iet met contour plot maken
x_un=x.unique()
y_un=y.unique()
X, Y = np.meshgrid(x_un, y_un)
c_un=np.array(c)*3/1000
m_un=np.array(mold)
mc_un=np.array(mc)


C=c_un.reshape(len(y_un),len(x_un),order='F')
M=m_un.reshape(len(y_un),len(x_un),order='F')
MC=mc_un.reshape(len(y_un),len(x_un),order='F')



#CONDENSATIE

plt.figure()
CS = plt.contourf(X, Y, C)
plt.title('Maximum condensation (l/m^2)')
axes = plt.gca()
axes.set_xlim([0,120])
plt.xlabel('MEW (-)')
plt.ylabel('LAMBDA (W/m^2K)')
colorbar(CS)
plt.show()


#MOULD GROWTH

plt.figure()
CS = plt.contourf(X, Y, M)
plt.title('MOULD INDEX (-)')
axes = plt.gca()
axes.set_xlim([0,20])
plt.xlabel('MEW (-)')
plt.ylabel('LAMBDA (W/m^2K)')
colorbar(CS)
plt.show()


#VOCHTINHOUD

plt.figure()
CS = plt.contourf(X, Y, MC)
plt.title('Moisture content (kg/m^3)')
axes = plt.gca()
axes.set_xlim([0,120])
plt.xlabel('MEW (-)')
plt.ylabel('LAMBDA (W/m^2K)')
colorbar(CS)
plt.show()










