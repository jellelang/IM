# -*- coding: utf-8 -*-
"""
Created on Tue Oct 07 13:03:57 2014

@author: jelle
"""


from pandas import Series, DataFrame
import  numpy.random as random





#------------------------------------------------------------------------------
# Input: Name of material and basefile
# Output: Series with number of lines of LAMBDA, MEW and KG
def material_lines(Material_in,basefile):
    line_material=-1
    ok=True
    Material='      NAME                     = %s\n' % Material_in
    for i in basefile:
        line_material=line_material+1
        if i == Material:
            ok=False        
            del Material
            break
    if ok:
        print('ERROR!!!  %s not found' % Material_in)  
# Look for line Lambda
    line_LAMBDA=line_material-1
    for i in basefile[line_material:] :       
        line_LAMBDA=line_LAMBDA+1
        if i[:12] == '      LAMBDA':
            break
        if (i == '  [MATERIAL]\n') | (i =='[CONDITIONS]\n'):
            print('ERROR !!! LAMBDA of %s not found' %Material_in)        
            break
# Look for line MEW
    line_MEW=line_material-1
    for i in basefile[line_material:] :       
        line_MEW=line_MEW+1
        if i[:9] == '      MEW':
            break
        if (i == '  [MATERIAL]\n') | (i =='[CONDITIONS]\n'):
            print('ERROR !!! MEW of %s not found' %Material_in)        
            break    
# Look for line KG        
    line_KG=line_material-1
    for i in basefile[line_material:] :       
        line_KG=line_KG+1
        if i[:8] == '      KG':
            break 
        if (i == '  [MATERIAL]\n') | (i =='[CONDITIONS]\n'):
            print('ERROR !!! KG of %s not found' %Material_in)        
            break
    lines=Series([line_LAMBDA, line_MEW,line_KG], index=['LAMBDA', 'MEW', 'KG'], name=Material_in)
    return lines
#------------------------------------------------------------------------------    
# find position line in which output folder is defined
# Input: basefile
def outputfolder_lines(basefile):
    line_output=-1
    ok=True
    for i in basefile:
        line_output=line_output+1
        if i[:-16] == '    OUTPUT_FOLDER            = $(PROJECT_DIR)':
            ok=False        
            break
    if ok:
        print('ERROR!!!  output folder not found')  
    return line_output      
#------------------------------------------------------------------------------
def give_random(dictionary):  
    if dictionary['dist']=='uniform':
        new_value = random.uniform(dictionary['min'],dictionary['max'])     
    #if dictionary['dist']=='normal':   
    return new_value

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    