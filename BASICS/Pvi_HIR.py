# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 09:55:49 2014
Deze file schrijft de interne dampdruk uit als functie van
        % buitendampdruk: Pve
        % n: ventilatie veelvoud
        % V: volume van de kamer
        % buitentemperatuur: Te
        % binnentemperatuur: Ti
        % HIR: hygric inertia response  


@author: jelle
"""

from __future__ import division
import numpy as np
import pandas as pd
import csv

# laat toe om alle functie en classes die gedefinieerd zijn in BASICS te gebruiken
import sys,os
path='C:/PostDoc/Python/IM/BASICS'
sys.path.append(path)
#from BASICS import *
from physics import *


    # n ventilatievoud in (1/h)
    # V volume (m³)
    # HIR* (zie artikel Vereecken 2009)
    # moistprod (vector met twee waarden, dag/nacht productie)
    

def VP_i(n,V,HIR,moistprod,T_ex,RH_ex):


    moistprod=[0.12,0]    
    # waarden gebruikt in doctoraat
    # n=0.5 of 0.15 #zie Limb,2001 (75-150 m³/h) is al weinig, normaal minium 75 m³/h in belgië
    # V=50  #is al een kleine kamer
    # HIR=1.5/1000   # zie Janssen 2009 (0, 0.59, 0.737, ... 3.558) 
    Rv=462 #J/kgK 
    # Gvp(1,8)=0;
    #zie randcondities Hens (is al zeer veel 1 persoon per 10 m² geduurden 16h per dag)

    T_ex=np.array(T_ex)+273.15
    RH_ex=np.array(RH_ex)
    PV_ex=vp(T_ex-273.15,RH_ex)   
    T_in=np.ones(8760)*293.15
    PV_in=vp(20,50)*np.ones(8760)
    #PV_ex=np.ones(8760)*1500

    uur=range(0,8760)        
    t=3600
    
    stappen=range(8,8760,24)   
    Gvp=np.zeros(8760)    
    for i in stappen:
        Gvp[i:i+16]=moistprod[0]/3600; 
        Gvp[i+17:i+24]=moistprod[1]; 


    ############## HIR-method #################################################
    for i in uur[1:8760]:
        a=PV_ex[i]*n*V/3600/T_in[i]/Rv + Gvp[i] +  PV_in[i-1]/t*(V/Rv/T_in[i]+100*HIR*V/vp((T_in[i]-273.15),100))
        b=(V/Rv/T_in[i]+100*HIR*V/vp((T_in[i]-273.15),100))/t + n*V/3600/Rv/T_in[i]
        PV_in[i]=a/b
        
#        if T_e(i)>293.15
#        pv_i(i)=pv_e(i);
#        elseif pv_i(i)>Pvsat(T_i(i)-273.15)
#        pv_i(i)=0.995*Pvsat(T_i(i)-273.15);
    return PV_in
    
