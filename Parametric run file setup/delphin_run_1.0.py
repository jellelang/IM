# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 11:42:03 2011

@author: Jelle Langmans
"""


from __future__ import division
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from  numpy.random import randn
import  numpy.random as random
from pandas import Series, DataFrame
import math
import sys,os
path='C:/PostDoc/Python/IM/Parametric run file setup'
sys.path.append(path)
from definities import *
# laat toe om alle functie en classes die gedefinieerd zijn in BASICS te gebruiken
import sys,os
path='C:/PostDoc/Python/IM/BASICS'
sys.path.append(path)
#from path import *
from physics import *
from Pvi_HIR import *
# import the module for calling external programs (creating subprocesses)
import subprocess

###############################################################################
# TO DO & notes
###############################################################################
# 1) opletten dat lijnen niet veranderen ondertussen: zorg ervoor dat elke aan-
# in de file tot hetzelfde aantal lijnen resulteert
# 2) nog bekijken hoe ik grid beter kan aanpassen
###############################################################################



###############################################################################
# 1  INPUT VAN DE GEBRUIKER

# BASEFILE & alternatieve grids
base_dir = 'C:/PostDoc/SIMULATIES/TESTPARAMETRIC' 
basefile_name = 'C:/PostDoc/SIMULATIES/TESTPARAMETRIC/INPUT1' 
basefile_name_rel = 'INPUT1'
grid={'var':True,'names':['grid1','grid2','grid3']}
indoor_pv={'var':False,'n':0.5,'V':50,'HIR':1.5/1000,'moistprod':[0.12,0]}  #TO DO elke simulatie moet en vp_i.ccd krijgen (n bv normaal verdeelt)
# dit is tijdelijk, moet aangepast worden
data=pd.read_csv('C:/PostDoc/Python/IM/Boundary_conditions/Uccle-hour.dat', sep=';',skiprows=range(3))
data.columns=['m', 'd', 'h','T_a','RH','G_gh','FF','DD','RR']



# VARIANTIONS/UNCERTAINTIES IN MATERIAL PROPERTIES

# uniform (min,max)
# normal  (mhu,sigma)
# distrete (range)
# design ([met waarden die moet aflopen])

# CELIT
# BASIC PARAMETERS
Celit_name='Celit'
Celit_MEW={'value':[5.0,10.0,20.0,40.0,80.0],'dist':'design','var':True}            
Celit_LAMBDA={'value':[0.05,0.1,0.2],'dist':'design','var':True} # [0.05,0.1,0.2]    
Celit_KG={'value':[0.05,0.1,0.2],'dist':'design','var':False}    
# MATERIAL FUNCTIONS
MRC=range(3)
grid_obj = open(base_dir+'/MRC.txt', 'r')
grid_file = grid_obj.readlines()
MRC_all=range(int((len(grid_file)-1)/3))
for i in range(int((len(grid_file)-1)/3)):
    MRC[0]=grid_file[i*3+2]
    MRC[1]=grid_file[i*3+3]
    MRC[2]=i+1
    MRC_all[i]=MRC #om te vermijden dat je heel de MRC in sommige files moet schrijven
Celit_MRC={'value':range(len(MRC_all)),'values':MRC_all,'dist':'design','var':True}    


# MINERAL WOOL
MW_name='MINERALE WOL 20'
MW_MEW={'value':[1,2],'dist':'design','var':False}               
MW_LAMBDA={'min':0.05,'max':0.5,'dist':'uniform','var':False}         
MW_KG={'mhu':0.1,'sigma':0.005,'dist':'normal','var':False} 
MW_MRC={'value':np.nan,'dist':'design','var':False}    
       
# OSB (intern dampscherm)
OSB_name='OSB Board'
OSB_MEW={'range':[100,200,300,400],'dist':'discrete','var':False}               
OSB_LAMBDA={'min':0.05,'max':0.5,'dist':'uniform','var':False}         
OSB_KG={'min':7.2e-8,'max':7.2e-6,'dist':'uniform','var':False}    
OSB_MRC={'value':np.nan,'dist':'design','var':False}    


materials=['one','two','three']
properties=['NAME','MEW', 'LAMBDA', 'KG','MRC']

data=[[Celit_name,MW_name,OSB_name],[Celit_MEW,MW_MEW,OSB_MEW],[Celit_LAMBDA,MW_LAMBDA,OSB_LAMBDA],[Celit_KG,MW_KG,OSB_LAMBDA],[Celit_MRC,MW_MRC,OSB_MRC]]

# Dataframe with all material properties 
    # example to extract: Materials.one['NAME']           by order in Dataframe
    # example to extract: Materials.one['VAR']            by order in Dataframe
    # example to extract: Materials.one['MEW']['var']     by order in Dataframe
 
Materials = DataFrame(data, columns=materials,index=properties)


###############################################################################

#alternatieve grids inlezen
dis_content=range(len(grid['names']))
as_content=range(len(grid['names']))
n=0

if grid['var']==True:
    for i in grid['names']:
        grid_obj = open(base_dir+'/'+i+'.dpj', 'r')
        grid_file = grid_obj.readlines()
        del grid_obj
        dis_lines=discretisation_lines(grid_file)
        as_lines=assignments_lines(grid_file)
        dis_content[n]=grid_file[np.min(dis_lines):np.max(dis_lines)+1]
        as_content[n]=grid_file[np.min(as_lines):np.max(as_lines)+1]
        n=n+1
###############################################################################
#klimaatfiles maken als het nodige is
if indoor_pv['var']==True:
    # ruwe data inlezen
    # TODO: hoe je aan T_ex en RH_ex komt herschrijven
    T_ex=data.T_a.values
    RH_ex=data.RH.values
    VP=VP_i(pv_in['n'],pv_in['V'],pv_in['n'],pv_in['moistprod'],T_ex,RH_ex)




###############################################################################

# aantal DESIGNS & UNCERTAINTIES voor materialen
n_design=1
n_uncert=0
index_m=[]
for i in Materials:
    for j in Materials.index:
           if type(Materials[i][j])==dict:
               if Materials[i][j]['dist']=='design' and\
                  Materials[i][j]['var']==True:
                      n_design=n_design*len(Materials[i][j]['value'])
               if Materials[i][j]['dist']!='design' and\
                  Materials[i][j]['var']==True:
                      n_uncert=n_uncert+1               
# aantal grid
n_design=n_design*len(grid['names']) #moet je wel zeker zijn dat grid steeds parameter is (niet steeds zo!)
                      
###############################################################################
#  2  AANMAKEN VAN DE DESIGN (TO DO HIERNA AANMAKEN VAN DE SAMPLES)

basefile_obj = open(basefile_name + '.dpj', 'r')
basefile = basefile_obj.readlines()
del basefile_obj

# Looking for lines of  material to be changed and storing in mat_lines



mat_lines = Series([])
for i in Materials:   
        a=material_lines(Materials[i]['NAME'],basefile)
        mat_lines=mat_lines.append(a)
# Discretisation block: lines 
dis_lines=discretisation_lines(basefile)
# Assignments block: lines
as_lines=assignments_lines(basefile)
# Looking for lines of outputfolder to be changed
output_line=outputfolder_lines(basefile)


#MATERIALS IN DESIGNS
design_opt=[]
design_value=[]
for i in Materials:
    for j in Materials.index:
           if type(Materials[i][j])==dict:
               if Materials[i][j]['dist']=='design' and\
                  Materials[i][j]['var']==True:
                      design_opt.append(j+'_'+Materials[i]['NAME'])
                      design_value.append(Materials[i][j]['value'])
#GRIDS IN DESIGNS
if grid['var']==True:
    design_opt.append('grid')
    design_value.append(range(len(grid['names'])))
#CLIMATES IN DESIGNS
if indoor_pv['var']==True:
    design_opt.append('PV_IN')
    design_value.append(range(len(indoor_pv['names'])))

#CONSTRUCT DATAFRAME WITH ALL DESIGN COMBINATIONS
design_grid=pd.DataFrame(cartesian(design_value),columns=design_opt)



# Make file to keep track of all changes
resultfile_obj = open(basefile_name + '_designs.txt', 'w')
# Schrijf vooropgestelde wijzigen weg
Materials.to_csv(resultfile_obj)
resultfile_obj.write('\n\n')
design_grid.to_csv(resultfile_obj)
#TODO:hier moet ook nog info over klimaat komen
#TODO:hier moet ook nog info over grid komen




#Series maken met referentie design in: daarna kan je er samples achtersteken
copyfile=basefile
design_files=[]

for j in design_grid.index:
    copyfile=basefile  
    for i in design_grid:
        # MATERIALEN
        if i[0:3]=='MEW':        
            copyfile[mat_lines[i]] = '      MEW                   = %g -\n' % design_grid[i][j]
        if i[0:6]=='LAMBDA':       
            copyfile[mat_lines[i]] = '      LAMBDA                   = %g W/mK\n' % design_grid[i][j]
        if i[0:2]=='KG':    
            copyfile[mat_lines[i]] = '      KG                   = %g W/mK\n' % design_grid[i][j]
        if i[0:3]=='MRC':    
            test=1 #TO DO nog een scriptje voor schrijven
        if i=='grid':
            for n in range(len(dis_lines)) :           
                copyfile[dis_lines[n]] = dis_content[int(design_grid[i][j])][n]
                copyfile[np.min(as_lines):]=as_content[int(design_grid[i][j])] 
        if i=='PV_IN':
            test=1 #TO DO
    design_files.append(copyfile)



#wegschrijven van de design_files als er geen uncertainties worden meegenomen (parameter study) 
if n_uncert==0: #er zijn worden geen onzekerheden meegenomen
    for i in range(len(design_files)):
        filename = basefile_name + '_%02d' % i
        filename_rel = basefile_name_rel + '_%02d' % i
        design_files[i][output_line] = ' OUTPUT_FOLDER= $(PROJECT_DIR)\ ' + filename_rel + '.results\n'
        fileobj = open(filename + '.dpj', 'w')
        fileobj.writelines(design_files[i])
        del fileobj
















#samples aanmaken: dit moet ik nog verder uitwerken    
if n_uncert!=0: #er zijn worden geen onzekerheden meegenomen
    n=0
    for i in range(N+1):
        # compose new filename
        filename = basefile_name + '_%02d' % i
        filename_rel = basefile_name_rel + '_%02d' % i
    
        basefile[output_line] = ' OUTPUT_FOLDER= $(PROJECT_DIR)\ ' + filename_rel + '.results\n'
    
        n=n+1
        resultfile_obj.write('%g\t' %(n))
     
        # Modifiying material properties
        for j in Materials.columns.values:
            if  Materials[j]['MEW']['var']==True:   
                mew_n=give_random(Materials[j]['MEW'])
                basefile[mat_lines[Materials[j]['NAME']]['MEW']] = '      MEW                   = %g -\n' % mew_n
                Changes[j]['MEW']=mew_n
            else:
                Changes[j]['MEW']=mew_n=float('nan')
            if  Materials[j]['LAMBDA']['var']==True:
                lambda_n=give_random(Materials[j]['LAMBDA'])
                basefile[mat_lines[Materials[j]['NAME']]['LAMBDA']] = '      LAMBDA                   = %g W/mK\n' % lambda_n
                Changes[j]['LAMBDA']=lambda_n
            else:
                Changes[j]['LAMBDA']=float('nan')        
            if  Materials[j]['KG']['var']==True:         
                kg_n=give_random(Materials[j]['KG'])
                basefile[mat_lines[Materials[j]['NAME']]['KG']] = '      KG                   = %g W/mK\n' % kg_n
                Changes[j]['KG']=kg_n
            else:
                Changes[j]['KG']=float('nan') 
            for i in parameters:
                resultfile_obj.write('%g\t' %(Changes[j][i]) )
        
        resultfile_obj.write('\n')
        resultfile_obj.flush()
        print 'Creating: ' + filename
        # open and write file
        fileobj = open(filename + '.dpj', 'w')
        fileobj.writelines(basefile)
        del fileobj
    del resultfile_obj


###############################################################################
