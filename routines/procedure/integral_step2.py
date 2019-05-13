#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
file name: integral_step2.
author: Sacha Gavino
date: March 2019
language: PYTHON 3.7
version of program: 1.2
main: integrate vertically over molecular number densities .
comments: the whole functions (maybe turned into methods in object soon) will be used in other files, one file for each step and a main file.
          For the moment we code the main() in this herein file during the developing phase.
"""
import os
import sys
import glob

import numpy as np
import pandas as pd
import re
from astropy.constants import au, m_p

import constants as cst


#-- FUNCTION 1: create a list of computed radii.
def radii():
    files = [f for f in sorted(os.listdir('../MODEL/gas/')) if re.findall(r'[0-9]+AU', f)]
    radii = [re.sub('.txt', '', fname) for fname in files]

    return radius
#----------------------------------------------

#-- FUNCTION 2: create a list of computed species.
def X():
    files = [f for f in os.listdir('../cross-sections/') if re.findall('0.1nm', f)]
    X = [re.sub('_0.1nm.txt', '', fname) for fname in files]

    return X
#------------------------------------------------

#-- FUNCTION 3: extract physical structure and dz.
def structure(radius):
    structure = pd.read_table('../MODEL/gas/%s.txt' % radius, sep=" ")
    z = structure['z'].values #altitudes in AU.
    dz = (structure['z'][10] - structure['z'][11])*au.to('cm').value # dz is constant along the vertical, so we only need to compute it at one height.

    return structure, dz
#------------------------------------------------

#-- FUNCTION 4: extract cross-sections values.
def cross_sections(species, wavelength):
    cross_sections = pd.read_table('../cross-sections/%s_0.1nm.txt' %  species, sep=" ", comment='#', header=None)
    name_cs = ['wv', 'abs', 'diss', 'ion'] # column names: wavelength(wv), absorption(abs), dissociation(diss), ionization(ion)
    cross_sections.columns = name_cs
    photoabs = cross_sections.loc[cross_sections['wv'] == wavelength, 'abs'].iloc[0]
    photodiss = cross_sections.loc[cross_sections['wv'] == wavelength, 'diss'].iloc[0]
    photoion = cross_sections.loc[cross_sections['wv'] == wavelength, 'ion'].iloc[0]

    return photoabs, photodiss, photoion
#---------------------------------------------

#-- FUNCTION 5: extract ISRF field values.
def i_isrf(files, wavelength):
    i_isrf = pd.read_table('../radiation_fields/%s.txt' % files, sep=" ", comment='#', header=None)
    name_field = ['wv', 'field'] # column names: wavelength(wv), radiation field(field)
    i_isrf.columns = name_field 
    dlambda = (i_isrf['wv'][11] - i_isrf['wv'][10]) #dlambda is constant. Will give the range (lambda, lambda + dlambda) in each we compute the photorate
    field = i_isrf.loc[i_isrf['wv'] == wavelength, 'field'].iloc[0]
    return dlambda, field
#---------------------------------------------

#-- FUNCTION 6: return the extinction efficiency.
def q_ext(A, wavelength, size, q_c):
	lambda_c = 2*np.pi*size*1e+7 # *1e+7 because the grain sizes are given in cm. So you don't need to convert the grain sizes in nm, it is done here. 
	if wavelength <= np.pi*size*1e+7:

		return A  #regime A. When lambda <= pi*size

	elif np.pi*size*1e+7 < wavelength < 2*np.pi*size*1e+7:

		return q_c*(wavelength/lambda_c)**(np.log10(q_c)/np.log10(2)) #regime B. When pi*size < lambda < 2pi*size

	elif wavelength >= 2*np.pi*size*1e+7:

		return q_c*(wavelength/lambda_c)**(-2) #regime C. When lambda >= 2pi*size
#-----------------------------------------------

#-- FUNCTION 7: return the molecular opacity at all elevations.
def molecular_opacity(species, structure, cross_section, radius, dz):
    n_species=structure['n('+species+')'].rename(radius)
    species_col = n_species.cumsum() #.values

    return species_col*cross_section*dz
#-------------------------------------------------------------

#-- FUNCTION 8: return the dust opacity at all elevations.
def dust_opacity(size, radius, Q, a, dz):
    species_density=dust_density[size].rename(radius)
    species_col = species_density.cumsum() #.values

    return species_col*Q*dz*a**2
#---------------------------------------------------------


#_________________________________________________#
#                      MAIN                       #
#_________________________________________________#
if __name__ == "__main__":

    """
    insert step 1. --> extract data from the ab/
    given by Nautilus computation during the run
    at each timestep we want to extract the data.
    """
    


    #---------variables---------
    files = 'standard_DRAINE_ISRF_1978' 
    wavelength = 92.2 # in nanometer here. WARNING: when defining a wavelength, always give it with a 0.1nm resolution (examples: 2.30nm, 21.40nm, 0.40nm etc.).
    radii = radii() # radii in list, used to loop on radii and define names of columns in (r,z) opacity tables.
    X = X() # species names in list, used to loop on species.
    gas_opacity_frame=pd.DataFrame()
    dust_opacity_frame=pd.DataFrame()
    #---------------------------
    
    #for radius in radii:
    dz = z = Q = 0
    tau_m = tau_d = structure = dust_density = 0

    #-----extract physical structures and dz-----   
    structure = pd.read_table('../MODEL/gas/%s.txt' % radius, sep=" ")
    z = structure['z'].values #altitudes in AU.
    dz = (structure['z'][10] - structure['z'][11])*au.to('cm').value # dz is constant along the vertical, so we only need to compute it at one arbitrary height.
    #--------------------------------------------

    #-----extract dust densities-----
    dust_density = pd.read_table('../MODEL/%s/dust_density.in' % radius, sep=" ")
    #print(dust['size1'])
    #--------------------------------

    #-----extract dust sizes-----
    size_table = pd.read_table('../MODEL/%s/sizes.in' % radius, sep=" ", index_col=0, names=['value'])
    #print(size.loc['size1'].value)
    dust_list = size_table.index.values
    dust_sizes = size_table['value'].values
    #----------------------------

    #molecules
    for species in X:
        #-----extract cross-sections values-----
        photoabs, photodiss, photoion = cross_sections(species, wavelength)
        #---------------------------------------

        #-----get gas opacity in each coordinates from 4H to midplane:-----
        tau_m += np.exp(-molecular_opacity(species, structure, photoabs, radius, dz))
        #------------------------------------------------------------------

    #-----stack opacities of each radius to dataframe-----
    gas_opacity_frame = pd.concat([gas_opacity_frame, tau_m], axis=1)
    #-----------------------------------------------------

    #dust
    for size in dust_list:
        #-----get size and geometrical dust cross-sections-----
        a = size_table.loc[size].value
        dust_cs = a**2
        #------------------------------------------------------

        #-----get extinction efficiency-----
        Q = q_ext(1., wavelength, a, 4.)
        #-----------------------------------

        #-----get dust opacity in each coordinates from 4H to midplane:-----
        tau_d += np.exp(-dust_opacity(size, radius, Q, a, dz))
        #-------------------------------------------------------------------

        #-----stack opacities of each radius to dataframe-----
        dust_opacity_frame = pd.concat([dust_opacity_frame, tau_d], axis=1)
        #-----------------------------------------------------
    
    #-----sum of both opacities-----
    total_opacity_frame = gas_opacity_frame.add(dust_opacity_frame, fill_value=0)
    #-------------------------------
    
    for species in X:
        #-----extract cross-sections values-----
        photoabs, photodiss, photoion = cross_sections(species, wavelength)
        #---------------------------------------

        #-----extract field values-----
        dlambda, field = i_isrf(files, wavelength)
        #---------------------------------------

        #-----photorates of species X-----
        photorate_frame = total_opacity_frame.multiply(photodiss*field*dlambda, fill_value=0)
        #-------------------------------

        #-----save dataframe to file-----
        print(photorate_frame)
        photorate_frame.to_csv('photorate_%s_922.dat' % species, sep=' ', float_format='%.5E', header=radii, index=False)
        #--------------------------------


    #-----save dataframe to file-----
    #print(gas_frame)
    gas_opacity_frame.to_csv('gas_opacity922.dat', sep=' ', float_format='%.5E', header=radii, index=False)
    #print(dust_frame)
    dust_opacity_frame.to_csv('dust_opacity922.dat', sep=' ', float_format='%.5E', header=radii, index=False)
    #print(total_frame)
    total_opacity_frame.to_csv('total_opacity922.dat', sep=' ', float_format='%.5E', header=radii, index=False)
    #--------------------------------

    

    """
    insert step 3. --> make the opacity computed
    at each coordinates usable by Nautilus for
    the next timestep.
    """


    '''
    at the end of step 2, we want a table of opacity in each coordinates. table (rows:64, column:13).
    '''

