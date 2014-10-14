# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 10:33:09 2014

@author: jelle
"""





import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

basefile_name = 'INPUT1'
basefile_obj = open(basefile_name + '.dpj', 'r')
del basefile_obj


N = 6 # define the number of variation steps

# open file for result


#script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
#rel_path = "2091/data.txt"
#abs_file_path = os.path.join(script_dir, rel_path)


# retrieve all the maximum moisture content levels at the middle height at the 
# interface between exterior panel and insulation 

results=[]
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

# construct DataFrame with a) lambda b) MEW c) Max_mc

overview = pd.read_csv(basefile_name + '_variation.txt',sep='\s+')
overview['MC_max']=results[0:N]

overview['_60']=overview['MC_max']<60
overview['_65']=((overview['MC_max']>=60) & (overview['MC_max']<65))
overview['_70']=((overview['MC_max']>=65) & (overview['MC_max']<70))
overview['_75']=((overview['MC_max']>=70) & (overview['MC_max']<75))
overview['_80']=((overview['MC_max']>=75) & (overview['MC_max']<80))
overview['_81']=overview['MC_max']>80

colors=[]
for i in overview['MC_max']:
    if i<60:
        colors.append(0.1)
    if (i>=60) & (i<65):
        colors.append(0.2)
    if (i>=65) & (i<70):
        colors.append(0.4)
    if (i>=70) & (i<75):
        colors.append(0.6)   
    if (i>=75) & (i<80):
        colors.append(0.8)
    if i>=80:
        colors.append(0.9)
        
        
        
        

x = overview['MEW']
y = overview['LAMBDA']
#colors = np.random.rand(N)
area = np.ones(N)*60  

plt.scatter(x, y, s=area, c=overview['MC_max'], alpha=0.7, linewidths=0)
plt.colorbar()

plt.show()


plt.scatter

plt.plot(overview['MEW'][overview['_60']],overview['LAMBDA'][overview['_60']],'o')
plt.plot(overview['MEW'][overview['_65']],overview['LAMBDA'][overview['_65']],'o')
plt.plot(overview['MEW'][overview['_70']],overview['LAMBDA'][overview['_70']],'o')
plt.plot(overview['MEW'][overview['_75']],overview['LAMBDA'][overview['_75']],'o')
plt.plot(overview['MEW'][overview['_80']],overview['LAMBDA'][overview['_80']],'o')

plt.show()