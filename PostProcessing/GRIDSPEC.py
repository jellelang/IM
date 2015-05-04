# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 08:09:31 2015

@author: jelle
"""


import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import matplotlib
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import scipy.ndimage
sys.path.append('C:/PostDoc/Python/IM/PostProcessing')
import mould
from matplotlib import gridspec





fig1 = plt.figure(figsize=(8, 6)) 

gs1 = gridspec.GridSpec(3, 3)
gs1.update(left=0.05, right=0.52, wspace=0.05)
ax1 = plt.subplot(gs1[:-1, :])
ax2 = plt.subplot(gs1[-1, :-1])
ax3 = plt.subplot(gs1[-1, -1])

gs2 = gridspec.GridSpec(3, 3)
gs2.update(left=0.55, right=0.98, hspace=0.05)
ax4 = plt.subplot(gs2[:, :-1])
ax5 = plt.subplot(gs2[:-1, -1])
ax6 = plt.subplot(gs2[-1, -1])

fig1.savefig('C:/Users/jelle/Desktop/subplot1.png',dpi=100)


fig2 = plt.figure(figsize=(8, 8)) 

gs1 = gridspec.GridSpec(2, 1)
gs1.update(left=0.05, right=0.5, wspace=0.05)   # met gs kun je dan de grote en positie van elke subplot afzonderlijk bepalen als je wil
ax1 = plt.subplot(gs1[:-1, :])
ax2 = plt.subplot(gs1[1:, :])
gs2 = gridspec.GridSpec(2, 1)
gs2.update(left=0.56, right=0.98, wspace=0.05)
ax3 = plt.subplot(gs2[:-1, :])
ax4 = plt.subplot(gs2[1:, :])

fig2.savefig('C:/Users/jelle/Desktop/subplot1.png',dpi=100)



fig3 = plt.figure(figsize=(8, 8)) 

gs1 = gridspec.GridSpec(2, 2)
gs1.update(left=0.05, right=0.98, wspace=0.1, hspace=0.1)   # wspace boven elkaar, hspace is naast elkaar
ax1 = plt.subplot(gs1[0:1, 0:1])
ax2 = plt.subplot(gs1[1:2, 0:1])
ax3 = plt.subplot(gs1[0:1, 1:2])
ax4 = plt.subplot(gs1[1:2, 1:2])

fig3.savefig('C:/Users/jelle/Desktop/subplot1.png',dpi=100)
