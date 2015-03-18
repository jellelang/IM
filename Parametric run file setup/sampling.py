# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 11:04:04 2015

@author: jelle
"""



import sys,os
path='C:/PostDoc/Python/IM/BASICS/pyDOE-0.3.7'
sys.path.append(path)
from pyDOE import *
from scipy.stats.distributions import norm

#basis: dit is voor eentje
lhd = lhs(2, samples=5)
lhd = norm(loc=0, scale=1).ppf(lhd)  # this applies to both factors here



#vier verdelingen en maak een reeks van 20 samples
design = lhs(4, samples=20)
from scipy.stats.distributions import norm
means = [1, 2, 3, 4]
stdvs = [0.1, 0.5, 1, 0.25]
for i in xrange(4):
    design[:, i] = norm(loc=means[i], scale=stdvs[i]).ppf(design[:, i])

