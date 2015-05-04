# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 09:22:52 2015

Demo of TeX rendering.

You can use TeX to render all of your matplotlib text if the rc
parameter text.usetex is set.  This works currently on the agg and ps
backends, and requires that you have tex and the other dependencies
described at http://matplotlib.sf.net/matplotlib.texmanager.html
properly installed on your system.  The first time you run a script
you will see a lot of output from tex and associated tools.  The next
time, the run may be silent, as a lot of the information is cached in
~/.tex.cache

"""
import numpy as np
import matplotlib.pyplot as plt
import sys
path='C:/Program Files (x86)/MiKTeX 2.9/miktex/bin'
sys.path.append(path)

# Example data
t = np.arange(0.0, 1.0 + 0.01, 0.01)
s = np.cos(4 * np.pi * t) + 2
fig1 = plt.figure(figsize=(8, 8)) 
plt.rc('text', usetex=True)
plt.rc('font', family='sans-serif') 
plt.plot(t, s)

font = {'fontname':'Arial', 'size':'16', 'color':'black', 'weight':'normal'}



plt.xlabel('time',fontsize=16)
plt.ylabel(r'\textbf{voltage} (mV)',fontsize=16)
plt.title(r'\TeX\ is Number '
          r'$\displaystyle\sum_{n=1}^\infty\frac{-e^{i\pi}}{2^n}$!',
          fontsize=16, color='gray')


# pas op het einde doen (je dit trouwens ook gebruiken om jan-feb-... te doen)
x=np.arange(0.0, 1.0 + 0.01, 0.1)
plt.xticks(x,list(x),**font)  
y=np.arange(1, 3 + 0.01, 0.5)
plt.yticks(y,list(y),**font)  



fig1.savefig('C:/Users/jelle/Desktop/subplot1.png',dpi=500)
plt.show()