# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 09:55:49 2014

@author: jelle
"""

import numpy as np
import pandas as pd
import csv



def vp(T,RH):
    RH=RH/100
    T=T+273
    PV=RH*np.exp(65.8-7066.3/T-5.98*np.log(T))
    return PV
    
def dewpoint(T,RH):   
    RH=RH/100
    b=17.67
    c=234.5
    g=np.log(RH)+b*T/(c+T)
    Td=(c*g)/(b-g)  
    return Td
