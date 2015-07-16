# -*- coding: utf-8 -*-
"""
Created on Tue Oct 07 13:03:57 2014

@author: jelle
"""


from pandas import Series, DataFrame
import  numpy.random as random
import numpy as np




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
# Look for lines MRC        
    line_MRC=line_material-1
    for i in basefile[line_material:] :       
        line_MRC=line_MRC+1
        if i == '      FUNCTION                 = Ol(pC)\n':
            break 
        if (i == '  [MATERIAL]\n') | (i =='[CONDITIONS]\n'):
            print('ERROR !!! KG of %s not found' %Material_in)        
            break
# Look for line OEFF        
    line_OEFF=line_material-1
    for i in basefile[line_material:] :       
        line_OEFF=line_OEFF+1
        if i[:10] == '      OEFF':
            break 
        if (i == '  [MATERIAL]\n') | (i =='[CONDITIONS]\n'):
            print('ERROR !!! OEFF of %s not found' %Material_in)        
            break   
# Look for line AW       
    line_AW=line_material-1
    for i in basefile[line_material:] :       
        line_AW=line_AW+1
        if i[:8] == '      AW':
            break 
        if (i == '  [MATERIAL]\n') | (i =='[CONDITIONS]\n'):
            print('ERROR !!! AW of %s not found' %Material_in)        
            break  
    line_MRC=line_MRC+1 #dan zit op de juiste plaats
    ind=['LAMBDA_'+Material_in, 'MEW_'+Material_in, 'KG_'+Material_in,'MRC_'+Material_in,'OEFF_'+Material_in,'AW_'+Material_in]
    lines=Series([line_LAMBDA, line_MEW,line_KG,line_MRC,line_OEFF,line_AW], index=ind)
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
# find the lines in which the discretisation grid is provided
# Input: basefile
def discretisation_lines(basefile):
    line_output=-1
    ok=True
    for i in basefile:
        line_output=line_output+1
        if i == '[DISCRETISATION]\n':
            ok=False        
            break
    if ok:
        print('ERROR!!!  discretisation block not found')  
    lines=range(line_output+2,(line_output+8))        
    return lines      
#------------------------------------------------------------------------------
# find the lines in which the assignments grid are
# Input: basefile
def assignments_lines(basefile):
    line_output=-1
    ok=True
    for i in basefile:
        line_output=line_output+1
        if i == '[ASSIGNMENTS]\n':
            ok=False        
            break
    if ok:
        print('ERROR!!!  discretisation block not found')  
    lines=range(line_output+2,(len(basefile)))      
    return lines    
#------------------------------------------------------------------------------
# find the lines in which the assignments grid are
# Input: basefile
def climate_lines(basefile):
    # T_out PV_out RAD T_sky T_in PV_in (eventueel PRES nog bijmaken later)    
    climate_file=['T_in','T_out','VP_in','VP_out','RAD','T_sky','PR_out','PR_in','RH_in','RH_out']
    lines=[]    
    for j in range(len(climate_file)):
        line_output=-1
        ok=True
        for i in basefile:
            line_output=line_output+1
            if i[-(len(climate_file[j])+1):-1]==climate_file[j] and\
               basefile[line_output-2]=='    [CLIMATE_COND]\n':          
                    ok=False        
                    break
        if ok:
            print('ERROR!!!  %s not block not found'  %climate_file[j])  
            line_output=0           
        lines.append(line_output) 
    return lines  
#------------------------------------------------------------------------------

def give_random(dictionary):  
    if dictionary['dist']=='uniform':
        new_value = random.uniform(dictionary['min'],dictionary['max'])     
    if dictionary['dist']=='normal':   
        new_value = random.normal(dictionary['mhu'], dictionary['sigma'])
    if dictionary['dist']=='discrete':   
        new_value = random.choice(dictionary['range'])
    return new_value

    
    
    
    
#combinatie maken
def cartesian(arrays, out=None):
    """
    Generate a cartesian product of input arrays.

    Parameters
    ----------
    arrays : list of array-like
        1-D arrays to form the cartesian product of.
    out : ndarray
        Array to place the cartesian product in.

    Returns
    -------
    out : ndarray
        2-D array of shape (M, len(arrays)) containing cartesian products
        formed of input arrays.

    Examples
    --------
    >>> cartesian(([1, 2, 3], [4, 5], [6, 7]))
    array([[1, 4, 6],
           [1, 4, 7],
           [1, 5, 6],
           [1, 5, 7],
           [2, 4, 6],
           [2, 4, 7],
           [2, 5, 6],
           [2, 5, 7],
           [3, 4, 6],
           [3, 4, 7],
           [3, 5, 6],
           [3, 5, 7]])

    """

    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1, arrays[0].size):
            out[j*m:(j+1)*m,1:] = out[0:m,1:]
    return out    
    
    
    
#draait een string van getallen om (handig om de MRC (Ol(pc) om te draaien)    
def reverse(string):
     f = [float(x) for x in string.split()]
     f.reverse()
     string=['']
     for i in f:
         string_i= '%s ' % str(i)
         string.append(string_i)
         string_rev = ''.join(string)   
     return (string_rev)      
    
    
    
    
    
    
    
    
    