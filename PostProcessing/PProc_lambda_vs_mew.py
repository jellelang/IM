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
import mould




basefile_name = 'C:/JELLE/SIMULATIES/ INPUT5' #opletten met spatie (vorige keer weggelaten omdat ik files manueel heb aangepast voor reeks 3)
basefile_name2 = 'C:/JELLE/SIMULATIES/INPUT5'



N = 107 # define the number of variation step

# open file for result


#script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
#rel_path = "2091/data.txt"
#abs_file_path = os.path.join(script_dir, rel_path)


# retrieve all the maximum moisture content levels at the middle height at the 
# interface between exterior panel and insulation 

results=[]
results_cond=[]
M_max=[]
for i in range(N+1):       
        # open and read output file
        filename = basefile_name + '_%02d' % i
        folder = filename + '.results'        
        output_filename = folder + '/mc_m.out' 
        data=pd.read_csv(output_filename,skiprows=range(13), header=None,sep='\s+')
        # hier kan je dan bv zoeken hoever in de file het eigelijk begint        
        # s+ omdat er meerdere separtors zijn 
        data.columns=['TIJD', 'MC']  
        data.MC.max()
        results.append(data.MC.max())
        
        output_filename_max = folder + '/cavity.out' 
        condens=pd.read_csv(output_filename_max,skiprows=range(13), header=None,sep='\s+')
        results_cond.append(condens[1].max()) #[4]  range(8890)

        output_filename_RH = folder + '/RH1.out' 
        RH=pd.read_csv(output_filename_RH,skiprows=range(13), header=None,sep='\s+')
        output_filename_T = folder + '/T1.out' 
        T=pd.read_csv(output_filename_T,skiprows=range(13), header=None,sep='\s+')

        T=np.array(T[1])
        RH=np.array(RH[1])
        M=mould.mould(T,RH)
        M_max.append(M.max())
        
        

        
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










