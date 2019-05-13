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
wv=92.2
zH = np.linspace(3.149606E-02, 4.000, 64)
photorate_CO = pd.read_table('photorate_CO_922.dat', sep=" ")
photorate_H2 = pd.read_table('photorate_H2_922.dat', sep=" ")
photorate_N2 = pd.read_table('photorate_N2_922.dat', sep=" ")
#-- plot section
fig1,ax = plt.subplots()
plt.title('photorates of CO and H2 for each coordinates; wavelength=%.1fnm' % wv, fontsize = 17)
plt.xlabel('photorates (s-1)', fontsize = 17)
plt.ylabel('elevation (z/H)', fontsize = 17)
plt.xlim(1e-16, 5e-11)
plt.ylim(0,4)

#CO
plt.semilogx(photorate_CO['040AU'], np.fliplr([zH])[0], linewidth=0.7, color = 'black', linestyle='-', label='solid line: CO')
plt.semilogx(photorate_CO['050AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='-', color = 'black')
plt.semilogx(photorate_CO['060AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='-', color = 'black')
plt.semilogx(photorate_CO['080AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='-', color = 'black')
plt.semilogx(photorate_CO['100AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='-', color = 'black')
plt.semilogx(photorate_CO['120AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='-', color = 'black')
plt.semilogx(photorate_CO['140AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='-', color = 'black')
plt.semilogx(photorate_CO['160AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='-', color = 'black')
plt.semilogx(photorate_CO['180AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='-', color = 'black')
plt.semilogx(photorate_CO['200AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='-', color = 'black')
plt.semilogx(photorate_CO['220AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='-', color = 'black')
plt.semilogx(photorate_CO['250AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='-', color = 'black')
plt.semilogx(photorate_CO['300AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='-', color = 'black')

#H2
plt.semilogx(photorate_H2['040AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='--', color = 'black', label='dashed line: H2')
plt.semilogx(photorate_H2['050AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='--', color = 'black')
plt.semilogx(photorate_H2['060AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='--', color = 'black')
plt.semilogx(photorate_H2['080AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='--', color = 'black')
plt.semilogx(photorate_H2['100AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='--', color = 'black')
plt.semilogx(photorate_H2['120AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='--', color = 'black')
plt.semilogx(photorate_H2['140AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='--', color = 'black')
plt.semilogx(photorate_H2['160AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='--', color = 'black')
plt.semilogx(photorate_H2['180AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='--', color = 'black')
plt.semilogx(photorate_H2['200AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='--', color = 'black')
plt.semilogx(photorate_H2['220AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='--', color = 'black')
plt.semilogx(photorate_H2['250AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='--', color = 'black')
plt.semilogx(photorate_H2['300AU'], np.fliplr([zH])[0], linewidth=0.7, linestyle='--', color = 'black')


#plt.semilogx(av2, z/(H), linewidth=1, color="black", linestyle='-', label="T from Williams and Best (2014)")
#plt.semilogx(av_naut, z/(H), linewidth=1, color="black", linestyle='--', label="T from Williams and Best (2014)")
plt.legend()
plt.show()
