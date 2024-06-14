# EXCTRACT BRANCHING RATIOS

rb.f90 is a subroutine that generates an output with the value of the branching ratio of reactions of species located in folder cross-sections.
This is needed to run Nautilus with the new calculation method of the photorates. see full documentation in documentation.pdf

------------------------------------
# DEPENDENCIES
* gfortran >= 7.3
* Python >= 3.7
* Numpy
* Re

------------------------------------
# INPUTS AND OUTPUTS

## -Inputs:
    cross-sections/*.txt:
        -- contains cross sections of different molecules. file names are the molecule names. 

## -Outputs:
    param.txt:
        -- each row is a molecule names. Molecule located in cross-sections

    branching_ratios.in:
        -- each row is a photodissociation reaction on left column and its branching ratio on right column.

-----------------------------------
# GENERAL USE
Here is the general description.

## Files and directory needed:
```
* rb.f90 
* create_param.py
* cross-sections/
```

WARNING: cross-sections/ subdirectory must be located in the same folder as rb.f90 and create_param.py. 

## Procedure
```
1) run create_param.py
2) run rb.f90
```

## functionnality
```
--create_param.py: creates a file param.txt, in which rows are molecule names of all the files in cross-sections/.
    This is used by routine rb.f90.

--run rb.f90: creates a file branching_ratios.in. Reads gas_species.in to find all photodissociation reactions of 
    molecules inside param.txt in order to calculate their branching ratios.
```



