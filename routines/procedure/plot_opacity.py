#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import sys

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
from matplotlib.ticker import NullFormatter
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
rcParams["figure.figsize"] = [10, 8]

#-- data extraction
wv=88.4
zH = np.linspace(3.149606E-02, 4.000, 64)
tau = pd.read_table('gas_opacity884.dat', sep=" ")
tau_d = pd.read_table('dust_opacity884.dat', sep=" ")
#-- plot section
fig1,ax = plt.subplots()
plt.title('molecular opacity in color and of dust in black; wavelength=%.1fnm' % wv, fontsize = 17)
plt.xlabel('opacity', fontsize = 17)
plt.ylabel('elevation z/H', fontsize = 17)
plt.xlim(1e-4, 1e6)
plt.ylim(0,4)

plt.semilogx(tau['040AU'], np.fliplr([zH])[0], linewidth=0.7, label='040')
plt.semilogx(tau['050AU'], np.fliplr([zH])[0], linewidth=0.7, label='050')
plt.semilogx(tau['060AU'], np.fliplr([zH])[0], linewidth=0.7, label='060')
plt.semilogx(tau['080AU'], np.fliplr([zH])[0], linewidth=0.7, label='080')
plt.semilogx(tau['100AU'], np.fliplr([zH])[0], linewidth=0.7, label='100')
plt.semilogx(tau['120AU'], np.fliplr([zH])[0], linewidth=0.7, label='120')
plt.semilogx(tau['140AU'], np.fliplr([zH])[0], linewidth=0.7, label='140')
plt.semilogx(tau['160AU'], np.fliplr([zH])[0], linewidth=0.7, label='160')
plt.semilogx(tau['180AU'], np.fliplr([zH])[0], linewidth=0.7, label='180')
plt.semilogx(tau['200AU'], np.fliplr([zH])[0], linewidth=0.7, label='200')
plt.semilogx(tau['220AU'], np.fliplr([zH])[0], linewidth=0.7, label='220')
plt.semilogx(tau['250AU'], np.fliplr([zH])[0], linewidth=0.7, label='250')
plt.semilogx(tau['300AU'], np.fliplr([zH])[0], linewidth=0.7, label='300')

plt.semilogx(tau_d['040AU'], np.fliplr([zH])[0], linewidth=0.7, color='black', label='size interval (cm): (5e-7, 2.24e-4) ')
plt.semilogx(tau_d['050AU'], np.fliplr([zH])[0], linewidth=0.7, color='black')
plt.semilogx(tau_d['060AU'], np.fliplr([zH])[0], linewidth=0.7, color='black')
plt.semilogx(tau_d['080AU'], np.fliplr([zH])[0], linewidth=0.7, color='black')
plt.semilogx(tau_d['100AU'], np.fliplr([zH])[0], linewidth=0.7, color='black')
plt.semilogx(tau_d['120AU'], np.fliplr([zH])[0], linewidth=0.7, color='black')
plt.semilogx(tau_d['140AU'], np.fliplr([zH])[0], linewidth=0.7, color='black')
plt.semilogx(tau_d['160AU'], np.fliplr([zH])[0], linewidth=0.7, color='black')
plt.semilogx(tau_d['180AU'], np.fliplr([zH])[0], linewidth=0.7, color='black')
plt.semilogx(tau_d['200AU'], np.fliplr([zH])[0], linewidth=0.7, color='black')
plt.semilogx(tau_d['220AU'], np.fliplr([zH])[0], linewidth=0.7, color='red')
plt.semilogx(tau_d['250AU'], np.fliplr([zH])[0], linewidth=0.7, color='red')
plt.semilogx(tau_d['300AU'], np.fliplr([zH])[0], linewidth=0.7, color='red')
#plt.semilogx(av2, z/(H), linewidth=1, color="black", linestyle='-', label="T from Williams and Best (2014)")
#plt.semilogx(av_naut, z/(H), linewidth=1, color="black", linestyle='--', label="T from Williams and Best (2014)")
plt.legend()
plt.show()
