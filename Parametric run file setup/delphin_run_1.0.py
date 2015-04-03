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
direct_py='C:/JELLE' #'C:/PostDoc/SIMULATIES'
direct_sim='C:/JELLE' #'C:/PostDoc/SIMULATIES'

path1=direct_py+ '/IM/Parametric run file setup'
path2=direct_py+ '/IM/BASICS'
path3=direct_py+ '/IM/Boundary_conditions'

path=path1
sys.path.append(path)
from definities import *
# laat toe om alle functie en classes die gedefinieerd zijn in BASICS te gebruiken
import sys,os
path=path2
sys.path.append(path)
path=path3
sys.path.append(path)
#from path import *
from physics import *
from Pvi_HIR import *
import climates
# import the module for calling external programs (creating subprocesses)
import subprocess

###############################################################################
# TO DO & notes
###############################################################################
# 1) opletten dat lijnen niet veranderen ondertussen: zorg ervoor dat elke aan-
# 2) in de file tot hetzelfde aantal lijnen resulteert.
###############################################################################



###############################################################################
# 1  INPUT VAN DE GEBRUIKER
###############################################################################

#BASEFILE 
base_dir = direct_sim+'/PARAMETRIC/1' 
basefile_name = direct_sim+'/PARAMETRIC/1/INPUT1' 
basefile_name_rel = 'INPUT1'


#ALTERNATIVE GRIDS
grid={'var':True,'names':['grid1','grid2','grid3','grid4','grid5','grid6']}

#CLIMATES: moet eigenlijk steeds op True staan, want je moet altijd een klimaat maken
Climate_n={'value':[0.5],'dist':'design','var':True} 
Climate_V={'value':[50.0],'dist':'design','var':True} 
Climate_T={'value':[20.0],'dist':'design','var':True} 
Climate_HIR={'value':[0.0015],'dist':'design','var':True} 
Climate_moistprod={'value':[0.12],'dist':'design','var':True} #het is enkel de piekwaarde die je op deze manier meegeeft 
Climate_pos={'value':['Uccle-hour_N'],'dist':'design','var':True}
Climate_path=path3+'/'
Climate_columns=['m', 'd', 'h','Ta','RH','G_gh','FF','DD','RAIN','RAD','CC']

#MATERIAL PROPERTIES  [uniform (min,max);normal  (mhu,sigma);distrete (range), design ([met waarden die moet aflopen])]

# MATERIAL 1
# BASIC PARAMETERS
name1='WIND_BARRIER'
MEW1={'value':[5.0,10.0,20.0,40.0,80.0],'dist':'design','var':True}            
LAMBDA1={'value':[0.05,0.1,0.2],'dist':'design','var':True} # [0.05,0.1,0.2]    
KG1={'value':[0.05,0.1,0.2],'dist':'design','var':False}    
# MATERIAL FUNCTIONS
MRC=range(4)
grid_obj = open(base_dir+'/MRC.txt', 'r')
grid_file = grid_obj.readlines()
MRC_all=range(int((len(grid_file)-1)/3))
for i in range(int((len(grid_file)-1)/3)):
    MRC[0]=grid_file[i*3+2]
    MRC[1]=grid_file[i*3+3]
    MRC[2]=i+1
    MRC_all[i]=MRC #om te vermijden dat je heel de MRC in sommige files moet schrijven
MRC1={'value':range(len(MRC_all)),'values':MRC_all,'dist':'design','var':True}    

# MATERIAL 2
name2='MINERALE WOL 20'
MEW2={'value':[1,2],'dist':'design','var':False}               
LAMBDA2={'min':0.05,'max':0.5,'dist':'uniform','var':False}         
KG2={'mhu':0.1,'sigma':0.005,'dist':'normal','var':False} 
MRC2={'value':np.nan,'dist':'design','var':False}    
       
# MATERIAL 3
name3='OSB Board'
MEW3={'range':[100,200,300,400],'dist':'discrete','var':False}               
LAMBDA3={'min':0.05,'max':0.5,'dist':'uniform','var':False}         
KG3={'min':7.2e-8,'max':7.2e-6,'dist':'uniform','var':False}    
MRC3={'value':np.nan,'dist':'design','var':False}    


materials=['one','two','three']
properties=['NAME','MEW', 'LAMBDA', 'KG','MRC']

data=[[name1,name2,name3],[MEW1,MEW2,MEW3],[LAMBDA1,LAMBDA2,LAMBDA3],[KG1,KG2,LAMBDA3],[MRC1,MRC2,MRC3]]

Materials = DataFrame(data, columns=materials,index=properties)


###############################################################################
# READ ALTERNATIVE GRIDS
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
# NUMBER OF DESIGNS & UNCERTAINTIES FOR MATERIALS, GRIDS & CLIMATES (TO BOUNDARY LAYERS,...)
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
# aantal climates
# buitenklimaat is steeds een design value
n_design=n_design*len(Climate_pos['value'])
# binnenklimaat kan zowel een design parameter als een onzekerheid zijn
if Climate_n['dist'] == 'design':
    n_design=n_design*len(Climate_n['value'])
else:
    n_uncert=n_uncert+1
if Climate_V['dist'] == 'design':
    n_design=n_design*len(Climate_V['value'])
else:
    n_uncert=n_uncert+1
if Climate_T['dist'] == 'design': 
    n_design=n_design*len(Climate_T['value'])
else:
    n_uncert=n_uncert+1
if Climate_HIR['dist'] == 'design': 
    n_design=n_design*len(Climate_HIR['value'])
else:
    n_uncert=n_uncert+1
if Climate_moistprod['dist'] == 'design':
    n_design=n_design*len(Climate_moistprod['value'])
else:
    n_uncert=n_uncert+1



###############################################################################
# Climate files maken TO DO ook in input files nodige aanpassingen doen


design_grid_climate=pd.DataFrame(cartesian([Climate_n['value'],Climate_V['value'],Climate_T['value'],Climate_HIR['value'],Climate_moistprod['value']]),columns=['n','V','T','HIR','Moistprod'])


#eerste de climates maken, dan in een volgende stap toevoegen aan files (dit stukje code moet dus nog omlaag)
for i in Climate_pos['value']:
    # construct the outdoor climates
    num_cl=0   
    climate_data=pd.read_csv(Climate_path+i+'.dat', sep=';',skiprows=range(3))
    climate_data.columns=Climate_columns
    climate_out=climates.construct_out_ccd(climate_data)
    climates.write_outdoor_ccd(base_dir,climate_out,i)  
    for j in design_grid_climate.index:
        num_cl=num_cl+1
        indoor_par=[design_grid_climate['n'][j],design_grid_climate['V'][j],design_grid_climate['T'][j],design_grid_climate['HIR'][j],design_grid_climate['Moistprod'][j]]
        climate_in=climates.construct_in_ccd(climate_data,indoor_par)
        climates.write_indoor_ccd(base_dir,climate_in,i+'_'+str(num_cl),indoor_par)  
   
    
              
###############################################################################
#  2  AANMAKEN VAN DE DESIGN (TO DO HIERNA AANMAKEN VAN DE SAMPLES)

basefile_obj = open(basefile_name + '.dpj', 'r')
basefile = basefile_obj.readlines()
del basefile_obj

# Looking for lines of  material to be changed and storing in mat_lines



mat_lines = Series([], dtype=int)
for i in Materials:   
        a=material_lines(Materials[i]['NAME'],basefile)
        mat_lines=mat_lines.append(a)
# Discretisation block: lines 
dis_lines=discretisation_lines(basefile)
# Assignments block: lines
as_lines=assignments_lines(basefile)
# Looking for lines of outputfolder to be changed
output_line=outputfolder_lines(basefile)
# Looking for lines of climate data
climate_line=climate_lines(basefile)

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
if Climate_pos['var']==True:
    design_opt.append('Location')
    design_value.append(range(len(Climate_pos['value'])))
    

Climate_in_value=[]
if Climate_n['dist']=='design' and\
   Climate_n['var']==True:
       design_opt.append('n')
       design_value.append(range(len(Climate_n['value'])))
       Climate_in_value.append(range(len(Climate_n['value'])))
if Climate_V['dist']=='design' and\
   Climate_V['var']==True:
       design_opt.append('V')
       design_value.append(range(len(Climate_V['value'])))
       Climate_in_value.append(range(len(Climate_V['value'])))
if Climate_T['dist']=='design' and\
   Climate_T['var']==True:
       design_opt.append('T_in')
       design_value.append(range(len(Climate_T['value'])))   
       Climate_in_value.append(range(len(Climate_T['value'])))
if Climate_HIR['dist']=='design' and\
   Climate_HIR['var']==True:
       design_opt.append('HIR')
       design_value.append(range(len(Climate_HIR['value'])))   
       Climate_in_value.append(range(len(Climate_HIR['value'])))
if Climate_moistprod['dist']=='design' and\
   Climate_moistprod['var']==True:
       design_opt.append('moistprod')
       design_value.append(range(len(Climate_moistprod['value'])))
       Climate_in_value.append(range(len(Climate_moistprod['value'])))



#CONSTRUCT DATAFRAME WITH ALL DESIGN COMBINATIONS
design_grid=pd.DataFrame(cartesian(design_value),columns=design_opt)
Climate_in_grid=pd.DataFrame(cartesian(Climate_in_value),columns=['n','V','T','HIR','moistprod'])
#HIER MAAK JE EEN EXTRA KOLOM IN DESIGN_GRID OM AAN TE DUIDEN OVER WELK BINNENKLIMAAT HET GAAT
ind=[]
for i in design_grid.index:
    n=-1
    for j in Climate_in_grid.index:
        n=n+1
        if (Climate_in_grid.ix[j, 'n':'moistprod'].values==design_grid.ix[i, 'n':'moistprod'].values).all():
            ind.append(Climate_in_grid.index.tolist()[n])

design_grid['Climate_in']=ind








# Make file to keep track of all changes
resultfile_obj = open(basefile_name + '_designs.txt', 'w')
# Schrijf vooropgestelde wijzigen weg
Materials.to_csv(resultfile_obj)
resultfile_obj.write('\n\n')
design_grid.to_csv(resultfile_obj)
#TODO:hier moet ook nog info over klimaat komen
#TODO:hier moet ook nog info over grid komen





#Series maken met referentie design in: daarna kan je er samples achtersteken
copyfile=list(basefile) #je moet er list voorzetten anders verandert basefile samen met copyfile (zijn dan hetzelfde)
design_files=[]

for j in design_grid.index:
    copyfile=list(basefile)
    for i in design_grid:
        # MATERIALEN
        if i[0:3]=='MEW':        
            copyfile[mat_lines[i]] = '      MEW                   = %g -\n' % design_grid[i][j]
        if i[0:6]=='LAMBDA':       
            copyfile[mat_lines[i]] = '      LAMBDA                   = %g W/mK\n' % design_grid[i][j]
        if i[0:2]=='KG':    
            copyfile[mat_lines[i]] = '      KG                   = %g W/mK\n' % design_grid[i][j]
        if i[0:3]=='MRC':       
            for m in Materials:
                if i=='MRC_'+Materials[m]['NAME']:
                    MRC_local=Materials[m]['MRC']['values']   
                    copyfile[mat_lines[i]] = '%s' % MRC_local[int(design_grid[i][j])][0]
                    copyfile[mat_lines[i]+1] = '%s \n' % MRC_local[int(design_grid[i][j])][1]
                    pc = reverse('%s' % MRC_local[int(design_grid[i][j])][0])
                    ol = reverse('%s' % MRC_local[int(design_grid[i][j])][1])
                    copyfile[mat_lines[i]+3] =  ol+'\n'
                    copyfile[mat_lines[i]+4] =  pc      
        if i=='grid':
            for n in range(len(dis_lines)) :           
                copyfile[dis_lines[n]] = dis_content[int(design_grid[i][j])][n]
                copyfile[np.min(as_lines):]=as_content[int(design_grid[i][j])] 
        if i=='Location':
                # outdoor
                if climate_line[1]!=0: copyfile[climate_line[1]+2] ='FILENAME                 = $(PROJECT_DIR)\\' + '%s_T_ex.ccd \n' %Climate_pos['value'][int(design_grid[i][j])]
                if climate_line[3]!=0: copyfile[climate_line[3]+2] ='FILENAME                 = $(PROJECT_DIR)\\' + '%s_VP_ex.ccd \n' %Climate_pos['value'][int(design_grid[i][j])]              
                if climate_line[4]!=0: copyfile[climate_line[4]+2] ='FILENAME                 = $(PROJECT_DIR)\\' + '%s_RAD.ccd \n' %Climate_pos['value'][int(design_grid[i][j])]
                if climate_line[5]!=0: copyfile[climate_line[5]+2] ='FILENAME                 = $(PROJECT_DIR)\\' + '%s_T_sky.ccd \n' %Climate_pos['value'][int(design_grid[i][j])]
                if climate_line[6]!=0: copyfile[climate_line[6]+2] ='FILENAME                 = $(PROJECT_DIR)\\' + '%s_PR_ex.ccd \n' %Climate_pos['value'][int(design_grid[i][j])]
                if climate_line[7]!=0: copyfile[climate_line[7]+2] ='FILENAME                 = $(PROJECT_DIR)\\' + '%s_PR_in.ccd \n' %Climate_pos['value'][int(design_grid[i][j])]
                # indoor
                if climate_line[0]!=0:  copyfile[climate_line[0]+2] ='FILENAME                 = $(PROJECT_DIR)\\' + '%s_%s_T_in.ccd \n' %(Climate_pos['value'][int(design_grid[i][j])], str(int(design_grid[i][j])+1))
                if climate_line[2]!=0:  copyfile[climate_line[2]+2] ='FILENAME                 = $(PROJECT_DIR)\\' + '%s_%s_VP_in.ccd \n' %(Climate_pos['value'][int(design_grid[i][j])], str(int(design_grid[i][j])+1))
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
