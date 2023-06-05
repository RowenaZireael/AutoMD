#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 15:20:23 2022

@author: yuchenzhou
"""

import os
a=os.getcwd()
print(a)


protein_name=input('Enter Protein Name:')

file = open(a+'/MOL_GMX.itp')
lines = file.readlines()
file.close()

find_atomtypes=lines.index('[ atomtypes ]\n')
print(find_atomtypes)
find_moleculetype=lines.index('[ moleculetype ]\n')
print(find_moleculetype)

atomtypesdata=lines[find_atomtypes+2:find_moleculetype-1]
print(atomtypesdata)

del lines[find_atomtypes-1:find_moleculetype]

file_itp=open('/Users/yuchenzhou/Desktop/GROMACS/tmp/MOL_GMX.itp','w')
file_itp.writelines(lines)
file_itp.close()

file_pro = open('/Users/yuchenzhou/Desktop/GROMACS/Mem_Pro_Input_Files/'+protein_name+'/'+'step5_input.gro')
pro_lines = file_pro.readlines()
file_pro.close()

file_lig = open(a+'/MOL_GMX.gro')
lig_lines = file_lig.readlines()

pro_lines[1]='  '+str(int(pro_lines[1])+int(lig_lines[1]))+'\n'

file_com = open('/Users/yuchenzhou/Desktop/GROMACS/tmp/step5_input.gro','w')
file_com.writelines(pro_lines[:-1])
file_com.writelines(lig_lines[2:-1])
file_com.writelines(pro_lines[-1])
file_com.close()

file_topol = open('/Users/yuchenzhou/Desktop/GROMACS/Mem_Pro_Input_Files/'+protein_name+'/'+'topol.top')
topol_lines = file_topol.readlines()
file_topol.close()

find_system=topol_lines.index('[ system ]\n')

file_comtop = open('/Users/yuchenzhou/Desktop/GROMACS/tmp/topol.top','w')
file_comtop.writelines(topol_lines[0:find_system-1])
file_comtop.writelines('#include "MOL_GMX.itp"\n')

file_comtop.writelines(topol_lines[find_system-1:])
file_comtop.writelines('MOL                1')

file_comtop.close()

file_FF = open('/Users/yuchenzhou/Desktop/GROMACS/tmp/toppar/forcefield.itp')
FF_lines = file_FF.readlines()
file_FF.close()
find_bondtypes=FF_lines.index('[ bondtypes ]\n')
FF_lines[find_bondtypes-3]='      K+    19    39.1000      1.000     A    4.73602e-01          1.37235e-03\n'
FF_lines[find_bondtypes-2]='    Zn2+    30    65.4000      2.000     A    1.95998e-01          5.23000e-02\n'

file_FF = open('/Users/yuchenzhou/Desktop/GROMACS/tmp/toppar/forcefield.itp','w')
file_FF.writelines(FF_lines[0:find_bondtypes-1])
file_FF.writelines(atomtypesdata)
file_FF.writelines(FF_lines[find_bondtypes-1:])
file_FF.close()
