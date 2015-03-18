# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 15:45:30 2015

@author: jelle
"""

# Boundaries

from __future__ import division
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

# laat toe om alle functie en classes die gedefinieerd zijn in BASICS te gebruiken
import sys,os
path='C:/PostDoc/Python/IM/BASICS'
sys.path.append(path)
#from path import *

from physics import *
from Pvi_HIR import *


n=0.5
V=50
HIR=1.5/1000
moistprod=[0.12,0]


# ruwe data inlezen
data=pd.read_csv('C:/PostDoc/Python/IM/Boundary_conditions/Uccle-hour.dat', sep=';',skiprows=range(3))
data.columns=['m', 'd', 'h','T_a','RH','G_gh','FF','DD','RR']
T_ex=data.T_a.values
RH_ex=data.RH.values
VP=VP_i(n,V,HIR,moistprod,T_ex,RH_ex)




