# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 16:58:15 2014

@author: jelle
"""

# Dit script leest data van VLIET op uurlijkse basis in (csv-file) en maakt file aan voor Meteonorm.
# Meteonorm zet deze file om in een stralingscomponent of tiled plane (Perez-model)
# Terug naar Python om Delphin input files aan te maken
import numpy as np
import pandas as pd
import csv
from physics import vp, dewpoint
import matplotlib.pyplot as plt



data_VLIET=pd.read_csv('Klimaat_jan_jun_2014_VLIET.csv')

data_ORG=pd.read_csv('FORMAT_METEONORM.dat',sep='\t',skiprows=[0])  

# In Vliet opgenomen in kW/m², ook tegenstraling eruit gehaald
data_VLIET['zonnestraling'][data_VLIET['zonnestraling']<0]=0
data_VLIET['zonnestraling']=data_VLIET['zonnestraling']*1000

Td=dewpoint(data_VLIET['temp'],data_VLIET['rv'])

data_ORG['G_Gh'][0:(len(data_VLIET['zonnestraling']))]=data_VLIET['zonnestraling']
data_ORG['Ta'][0:(len(data_VLIET['zonnestraling']))]=data_VLIET['temp']
data_ORG['Td'][0:(len(data_VLIET['zonnestraling']))]=Td

# hier data van VLIET in ORG schrijven
data_ORG.to_csv('VLIET.dat', sep='\t',index=False)

#' mn7 import file '
# zelf nog manueel dit lijnte (tussen '') bij aanvullen op eerste rij

# werkt enkel als je enkel globale straling ingeeft
