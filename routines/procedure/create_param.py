#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file name: create_param.
author: Sacha Gavino
date: June 2019
language: PYTHON 3.7
version of program: 1.0
main: create a parameter file that will be read by Nautilus to loop over the cross-sections files.
comments: must be run before launching Nautilus.
"""
import os

import numpy as np
import re


#-- FUNCTION : create a list of file names.
def X():
    files = [f for f in os.listdir('cross-sections/') if re.findall('.txt', f)]
    X = [re.sub('.txt', '', fname) for fname in files]

    return X



#_________________________________________________#
#                      MAIN                       #
#_________________________________________________#
if __name__ == "__main__":

    X = X()
    np.savetxt('cross-sections/param.txt', X, fmt='%s', delimiter=' ', newline='\n', encoding=None)