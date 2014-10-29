# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 15:19:16 2014

@author: jelle
"""

import numpy as np
import pandas as pd
import csv
from physics import vp, dewpoint
import matplotlib.pyplot as plt
from datetime import datetime
import delphin



data_VLIET=pd.read_csv('Klimaat_jan_jun_2014_VLIET.csv')

data_VLIET_NE=pd.read_csv('VLIET_JAN_JUN_NE.dat',skiprows=range(3),sep='\t')
data_VLIET_SW=pd.read_csv('VLIET_JAN_JUN_ZW.dat',skiprows=range(3),sep='\t')

STRALING_NE=data_VLIET_NE['G_Gk']
STRALING_SW=data_VLIET_SW['G_Gk']
Ta=data_VLIET['temp']
Td=dewpoint(data_VLIET['temp'],data_VLIET['rv'])
Tsky=(Ta+273)*((0.8+Td/250)**0.25)-273
RH=data_VLIET['rv']
PV=vp(data_VLIET['temp'],data_VLIET['rv'])



#to do: functie van maken en dan van alle input-data die doorlopen
delphin.climate_file('T_sky',Tsky)
delphin.climate_file('RAD_NE',STRALING_NE)
delphin.climate_file('RAD_SW',STRALING_SW)
delphin.climate_file('Ta',Ta)
delphin.climate_file('PV',PV)
delphin.climate_file('RH',RH)




