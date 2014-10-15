# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 11:42:03 2011

@author: RBa
"""

import os, pp, numpy, shutil

import sys

sys.path.append(r'C:\JELLE\SIMULATIES')

import pymosim

work_dir = r'C:\JELLE\SIMULATIES'
os.chdir(work_dir)

# first we must make a dictionary of the parameteric we want to do
# and we add the parameters and their values we want to run
#dictionary = {}
#dictionary.update({r'building_forGrid.heaSys.onOffDelay' : numpy.array([300,600,900,1200])})
#dictionary.update({r'building_forGrid.heaSys.betaFactorHeatPump' : numpy.array([0.7,0.8,0.9])})
#dictionary.update({r'building_forGrid.whichUser' : numpy.array([3,30])})
#dictionary.update({r'building_forGrid.heaSys.tesTank.volumeTank' : numpy.array([0.200,0.300,0.400])})
#dictionary.update({r'building_forGrid.heaSys.HPControl.dTSafetyTop' : numpy.array([3,5])})

# now we set everything ready for parallel python, the return consistst of a 
# list of cd-paths where all sub-sets are located as for parallel python
sub_dir = []
for i in range(101):
    sub_dir.append('INPUT2_%02d' %i)

# initialise parallel python
ppservers=()
job_server = pp.Server(ppservers = ppservers, ncpus=7)
# define the inputs and start the simulations
inputs = tuple(sub_dir)
jobs = [(input, job_server.submit(pymosim.start_parametric_run, args = (input,), modules = ("subprocess","os"))) for input in inputs]

job_server.wait() 
job_server.destroy()

#pymosim.close_parametric_run(work_dir, sub_dir)



    




