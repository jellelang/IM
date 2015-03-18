# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 09:55:49 2014

@author: jelle
"""

from __future__ import division
import numpy as np
import pandas as pd
import csv



def vp(T,RH):
    RH=RH/100
    T=T+273.15
    PV=RH*np.exp(65.8094-7066.27/T-5.976*np.log(T))
    return PV
    
def dewpoint(T,RH):   
    RH=RH/100
    b=17.67
    c=234.5
    g=np.log(RH)+b*T/(c+T)
    Td=(c*g)/(b-g)  
    return Td
