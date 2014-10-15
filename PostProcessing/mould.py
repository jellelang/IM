# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 11:20:04 2014

@author: jelle
"""

import pandas as pd
import numpy as np

def mould(T,RH):
    M=np.zeros(len(RH))
    dt=1./24
        
    W=0   #(0 is pine)(1=spruce (minder kritisch))
    SQ=0  #veel sneller als dit op 1 staat  
    
    unfav=np.zeros(len(RH))
    for i in range(len(RH)):
        if (T[i]<0) | (RH[i]<80):
            unfav[i]=1
        else:
            unfav[i]=0
        if RH[i]>100:
            RH[i]=100
     
    for i in range(len(RH))[1:len(RH)]:     
            
            if T[i]<=20:
                RHcrit=-0.00267*T[i]**3+0.16*T[i]**2-3.13*T[i]+100
            else:
                RHcrit=80

            tm1=np.exp(-0.68*np.log(T[i])-13.9*np.log(RH[i])+0.14*W-0.33*SQ+66.02)
            tm3=np.exp(-0.74*np.log(T[i])-12.72*np.log(RH[i])+0.06*W+61.50)
            
            if M[i-1]<=1:
                k1=1
            if M[i-1]>1:
                k1=2/((tm3/tm1)-1)            
            if RHcrit==100:
                Mmax=0
            else:
                Mmax=max((1+7*(RHcrit-RH[i])/(RHcrit-100)-2*((RHcrit-RH[i])/(RHcrit-100))**2),0)
            k2=max((1-np.exp(2.3*(M[i-1]-Mmax))),0)
    
            #unfavorable conditions
            G=k1*k2/7/tm1
            # omdat je met uurlijkse data werkt maar t in dM/dt in dagen is
            deltaM=G*dt 
    
            #pas na 24h kun je kijken of er vermindering is
            if i>24:
                tunfav=0
                for j in range(24):
                    if unfav[i-j]==1:
                        tunfav=tunfav+1
                    if unfav[i-j]==0:
                        break
                    
                if 1<=tunfav & tunfav<=5:
                    deltaM=-0.032*dt
                if 6<tunfav & tunfav<=23:
                    deltaM=0
                if tunfav>23:
                    deltaM=-0.016*dt    
            
          
            
            M[i]=M[i-1]+deltaM
    
            if M[i]<0:
                M[i]=0
            

        #TF = isreal(M(i)):
        #if TF==0
        #    break   
    return M