# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 11:42:03 2011

@author: Jelle Langmans
"""

make_sim = True
handle_res = False 

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from  numpy.random import randn
import  numpy.random as random
from pandas import Series, DataFrame
import os
import sys
import pickle 
from definities import material_lines
from definities import outputfolder_lines
from definities import give_random
# import the module for calling external programs (creating subprocesses)
import subprocess


###############################################################################
# TO DO 
###############################################################################
# 1) variatie in grid (snelle versie nog verbeteren, integreren in geheel)
###############################################################################



###############################################################################
# 1  INPUT VAN DE GEBRUIKER

# BASEFILE
basefile_name = 'C:/PostDoc/SIMULATIES/TESTPARAMETRIC/INPUT1'  #zonder extensie geven
basefile_name_rel = 'INPUT1'


# VARIANTIONS/UNCERTAINTIES IN MATERIAL PROPERTIES
# CELIT
Celit_name='Celit'
Celit_VAR=True
Celit_MEW={'min':3,'max':100,'dist':'uniform','var':True}
Celit_LAMBDA={'min':0.05,'max':0.5,'dist':'uniform','var':True}
Celit_KG={'min':7.2e-8,'max':7.2e-6,'dist':'uniform','var':False}
# MINERAL WOOL
MW_name='MINERALE WOL 20'
MW_VAR=False
MW_MEW={'min':3,'max':100,'verdeling':'dist','var':False}
MW_LAMBDA={'min':0.05,'max':0.5,'dist':'uniform','var':False}
MW_KG={'min':7.2e-8,'max':7.2e-6,'dist':'uniform','var':False}

materials=['one','two']
properties=['NAME','VAR','MEW', 'LAMBDA', 'KG']

data=[[Celit_name,MW_name],[Celit_VAR,MW_VAR],[Celit_MEW,MW_MEW],[Celit_LAMBDA,MW_LAMBDA],[Celit_KG,MW_KG]]

# Dataframe with all material properties 
    # example to extract: Materials.one['NAME']           by order in Dataframe
    # example to extract: Materials.one['VAR']            by order in Dataframe
    # example to extract: Materials.one['MEW']['var']     by order in Dataframe
 
Materials = DataFrame(data, columns=materials,index=properties)

# aantal files dat er gemaakt moeten worden
N=10
###############################################################################





###############################################################################
#  2  AANMAKEN VAN DE FILES

basefile_obj = open(basefile_name + '.dpj', 'r')
basefile = basefile_obj.readlines()
del basefile_obj



# Looking for lines of  material to be changed and storing in mat_lines
for i in Materials: 
    if i=='one':    
        a=material_lines(Materials[i]['NAME'],basefile)
        mat_lines=DataFrame(a)
    else:
        a=material_lines(Materials[i]['NAME'],basefile)
        mat_lines[Materials[i]['NAME']]=a    
# Looking for lines of outputfolder to be changed
output_line=outputfolder_lines(basefile)



# Make file to keep track of all changes
resultfile_obj = open(basefile_name + '_variation.txt', 'w')
resultfile_obj.write('file \t MEW\t LAMBDA \n') 

MEW_value=[1,1.55,2.40,3.72,5.77,8.94,13.9,21.5,33.33,51.6,80.04,124.06]
LAMBDA_value=[0.02,0.03,0.045,0.0675,0.1025,0.1518,0.2278,0.3417,0.5125]


n=0
for i in range(len(MEW_value)):
    for  j in range(len(LAMBDA_value)):
        # compose new filename
        naam=(i+j)+i*(len(LAMBDA_value)-1)
        filename = basefile_name + '_%02d' % naam
        filename_rel = basefile_name_rel + '_%02d' % naam
    
        basefile[output_line] = ' OUTPUT_FOLDER= $(PROJECT_DIR)\ ' + filename_rel + '.results\n'
    
        # Modifiying material properties
        
        mew_n=MEW_value[i]
        basefile[310] = '      MEW                   = %g -\n' % mew_n

        lambda_n=LAMBDA_value[j]
        basefile[306] = '      LAMBDA                   = %g W/mK\n' % lambda_n
          
        print 'Creating: ' + filename
        # open and write file
        fileobj = open(filename + '.dpj', 'w')
        fileobj.writelines(basefile)
        del fileobj
        n=n+1
        resultfile_obj.write('%g\t %g\t %g\t \n' %(n, mew_n,lambda_n))
        resultfile_obj.flush()
del resultfile_obj






###############################################################################

        
#for i in range(N+1):
#    alpha = 8 + (20-8)*float(i)/N
#    beta = (0.3 + (1.6-0.3)*float(i)/N)*1e-7
#    # compose new filename
#    filename = basefile_name + '_%02d' % i
#    folder = ' ' + filename + '.results'
#    # exchange line with alpha parameter
#    basefile[187] = ' EXCOEFF = %g W/m2K\n' % alpha
#    # exchange line with beta parameter
#    basefile[194] = ' EXCOEFF = %g s/m\n' % beta
#    # don’t forget to compose a new output folder
#    basefile[239] = ' OUTPUT_FOLDER= $(PROJECT_DIR)\ ' + filename + '.results\n'
#
#    print 'Creating: ' + filename
#    # open and write file
#    fileobj = open(filename + '.dpj', 'w')
#    fileobj.writelines(basefile)
#    del fileobj
#
#
#    if make_sim:
#
#        # call the DELPHIN solver , yet without command line arguments
#        retcode = subprocess.call([delphin_executable , "-x", "-v0", filename + '.dpj'])
#      
#        if retcode != 0:
#            print '\nCalculation error'
#            continue
#        else:
#            print '\nCalculation completed successfully'
#        
#    if handle_res:      
#        
#      
#       
#        # open and read output file
#        output_filename = folder + '\\temp_inside.out'
#        outfile_obj = open(output_filename , 'r')
#    
#        outdata_T = outfile_obj.readlines()
#        del outfile_obj
#        # strip header information (we know how it looks like)
#        outdata_T = outdata_T[13:]
#        # extract all values
#        values = []
#        for line in outdata_T:
#            nums = line.split()
#            values.append( float(nums[1]) )
#            # perform analysis and write results
#        minval = min(values)
#        resultfile_obj.write( '%g\t %g\t %g\n' % (alpha , beta, minval) )
#        # flush buffered output (so that we can monitor the progress from outside)
#        resultfile_obj.flush()
#        # close result file
#        #del resultfile_obj