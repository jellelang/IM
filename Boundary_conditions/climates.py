# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 17:25:41 2014

@author: jelle
"""
from __future__ import division
import numpy as np
import pandas as pd
import csv
from physics import vp, dewpoint
# laat toe om alle functie en classes die gedefinieerd zijn in BASICS te gebruiken
import sys,os
path='C:/PostDoc/Python/IM/BASICS'
sys.path.append(path)
#from BASICS import *
from physics import *
import matplotlib as plt


indoor_pv={'var':False,'n':0.5,'V':50,'HIR':1.5/1000,'moistprod':[0.12,0]}  #TO DO elke simulatie moet en vp_i.ccd krijgen (n bv normaal verdeelt)



#hier matrix met alles in maken
def construct_out_ccd(DATA):
    #create PV_ex
    DATA['VP_ex']=vp(DATA['T_ex'],DATA['RH_ex'])
    #create T_sky
    Ta=DATA['T_ex']
    Td=dewpoint(DATA['T_ex'],DATA['RH_ex'])
    c=DATA['CC']
    #DATA['T_sky']=(Ta+273)*((0.8+Td/250)**0.25)-273  
    DATA['T_sky']=Ta-(23.8-0.2*Ta)*(1-0.87*c/8) # als je cloud coverin factor niet hebt
    DATA['T_ground']=Ta
    return DATA






#hier matrix met alles in maken
def construct_in_ccd(DATA,indoor_par):
    #create PV_ex
    DATA['VP_in']=VP_i(indoor_par,DATA['T_ex'],DATA['RH_ex'])
    DATA['T_in']=indoor_par[2]*np.ones(8760) 
    T_in=indoor_par[2]*np.ones(8760) 
    DATA['RH_in']=DATA['VP_in']/vp(T_in,100*np.ones(8760))*100   
    #To Do: properder schrijven (gehaast)    
    for i in range(len(DATA['RH_in'])):
        if DATA['RH_in'][i]>=100:
            DATA['RH_in'][i]=99 
    return DATA




#writes one ccd
def write_ccd(path,type_input,value,name,indoor_par):
    if type_input=='T_sky':
        schrijf=open(path+'/'+name+'_T_sky.ccd', 'w')
        schrijf.write('TC	C	 \n')	
    if type_input=='RH_ex':
        schrijf=open(path+'/'+name+'_RH_ex.ccd', 'w')
        schrijf.write('RH	---	 \n')	
        value=value/100
    if type_input=='RH_in':
        schrijf=open(path+'/'+name+'_RH_in.ccd', 'w')
        schrijf.write('RH	---	 \n')	
        value=value/100
    if type_input=='T_ex':
        schrijf=open(path+'/'+name+'_T_ex.ccd', 'w')
        schrijf.write('TC	C	 \n')	
    if type_input=='T_ground':
        schrijf=open(path+'/'+name+'_T_ground.ccd', 'w')
        schrijf.write('TC	C	 \n')
    if type_input=='RAD':
        schrijf=open(path+'/'+name+'_RAD.ccd', 'w')
        schrijf.write('SHWRAD  W/m2\n')	    
    if type_input=='RAD_NE':
        schrijf=open(path+'/'+name+'_RAD_shrt_NE.ccd', 'w')
        schrijf.write('SHWRAD  W/m2\n')	
    if type_input=='RAD_SW':
        schrijf=open(path+'/'+name+'_RAD_shrt_SW.ccd', 'w')
        schrijf.write('SHWRAD  W/m2\n')	
    if type_input=='VP_ex':
        schrijf=open(path+'/'+name+'_VP_ex.ccd', 'w')
        schrijf.write('VAPPRESS 	Pa\n')        
    if type_input=='VP_in':
        schrijf=open(path+'/'+name+'_VP_in.ccd', 'w') 
        schrijf.write('# n: %0.0f \n' %indoor_par[0])  
        schrijf.write('# V: %0.0f \n' %indoor_par[1])  
        schrijf.write('# HIR: %0.0f \n' %indoor_par[3])  
        schrijf.write('# Moistprod: %0.0f \n' %indoor_par[4])  
        schrijf.write('VAPPRESS 	Pa\n')             
    if type_input=='T_in':
        schrijf=open(path+'/'+name+'_T_in.ccd', 'w')
        schrijf.write('TC	C	 \n')	                
    schrijf.write('\n')	
    for d in range(364):
       day=d
       for h in range (24):
         hour=h+1
         pos=day*24+hour
         if pos == len(value):
             break
         pos_shift=pos+5856
         if pos_shift>=8760:
             pos_shift=pos-(8760-5856)
         schrijf.write('%0.0f %2.0f:%0.0f0:0%0.0f %3.4f\n' %(day,hour,0,0,value[pos_shift]))
         if h == len(value): 
              break 
       if pos == len(value):
           break
    schrijf.flush()
    schrijf.close()
    
    
    
    
    
    
    
    
def VP_i(indoor_par,T_ex,RH_ex):
#Deze file schrijft de interne dampdruk uit als functie van
#        % buitendampdruk: Pve
#        % n: ventilatie veelvoud
#        % V: volume van de kamer
#        % buitentemperatuur: Te
#        % binnentemperatuur: Ti
#        % HIR: hygric inertia response  


    #opletten stukje overschreven om klimaat klasse te kunnen gebruiken

    n=indoor_par[0]
    V=indoor_par[1]
    T_in=(indoor_par[2]+273.15)*np.ones(8760)    
    HIR=indoor_par[3]
    moistprod=[indoor_par[4],0]#die nul is nu wel vast

    EN=indoor_par[5]
    EN_class=indoor_par[6]

    TV=indoor_par[7]
    TV_class=indoor_par[]

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
        if T_ex[i]>293.15:
            PV_in[i]=PV_ex[i]
        elif PV_in[i]>vp(T_in[i]-273.15,100):
            PV_in[i]=0.995*vp(T_in[i]-273.15,100)
         
    #ISO 13788:2001     
    if EN==True:   
        if EN_class==3.0:
            max_vp=550
        if EN_class==4.0:
            max_vp=810        
        for i in uur[1:8760]:
            if T_ex[i]<273.15:
                PV_in[i]=PV_ex[i]+max_vp
            if T_ex[i]>273.15 and T_ex[i]<293.15:
                PV_in[i]=PV_ex[i]+max_vp*(293.15-T_ex[i])/20
            if T_ex[i]>293.15:
                PV_in[i]=PV_ex[i]
            if PV_in[i]>vp(T_in[i]-273.15,100):
                PV_in[i]=0.995*vp(T_in[i]-273.15,100)          
     
    #TV
    if TV==True:   
        if TV_class==2.0:
            max_vp=436
            for i in uur[1:8760]:
                if T_ex[i]<(273.15+15.9):
                    PV_in[i]=PV_ex[i]+(max_vp-(T_ex[i]-273.15)*10)
                if T_ex[i]>(273.15+15.9):
                    PV_in[i]=PV_ex[i]
                if PV_in[i]>vp(T_in[i]-273.15,100):
                    PV_in[i]=0.995*vp(T_in[i]-273.15,100) 
        if TV_class==3.0:
            max_vp=713        
            for i in uur[1:8760]:
                if T_ex[i]<(273.15+15.9):
                    PV_in[i]=PV_ex[i]+(max_vp-(T_ex[i]-273.15)*10)
                if T_ex[i]>(273.15+15.9):
                    PV_in[i]=PV_ex[i]
                if PV_in[i]>vp(T_in[i]-273.15,100):
                    PV_in[i]=0.995*vp(T_in[i]-273.15,100)   
    return PV_in
    
    
    
  
    
    
    
#writes one ccd
def write_outdoor_ccd(path,data,name):
    types=['T_sky','RH_ex','T_ex','RAD','VP_ex','T_ground']
    for i in types:
        par=0
        write_ccd(path,i,data[i],name,par)
    
    
    
#writes one ccd
def write_indoor_ccd(path,data,name,indoor_par):
    types=['VP_in','T_in','RH_in'] #je zou T_in hier ook kunnen bijvoegen als je meerder T_in's wil maken
    for i in types:
        write_ccd(path,i,data[i],name,indoor_par)
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    