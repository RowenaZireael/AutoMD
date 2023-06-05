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

file = open(a+'/MOL_GMX.top')
lines = file.readlines()
file.close()

find_defaults=lines.index('[ defaults ]\n')
print(find_defaults)
find_system=lines.index('[ system ]\n')
print(find_system)

del lines[find_system:find_system+6]
del lines[find_defaults:find_defaults+3]
file_itp=open('/Users/yuchenzhou/Desktop/GROMACS/tmp/MOL_GMX.itp','w')
file_itp.writelines(lines)
if '_ZN' in protein_name:
    file_itp.write('; Ligand position restraints \n#ifdef POSRES_LIG \n#include "posre_MOL.itp" \n#endif')

file_itp.close()

file_pro = open('/Users/yuchenzhou/Desktop/GROMACS/Protein_Input_Files/'+protein_name+'/'+protein_name+'_processed.gro')
pro_lines = file_pro.readlines()
file_pro.close()

file_lig = open(a+'/MOL_GMX.gro')
lig_lines = file_lig.readlines()

pro_lines[1]='  '+str(int(pro_lines[1])+int(lig_lines[1]))+'\n'

file_com = open('/Users/yuchenzhou/Desktop/GROMACS/tmp/complex.gro','w')
file_com.writelines(pro_lines[:-1])
file_com.writelines(lig_lines[2:-1])
file_com.writelines(pro_lines[-1])
file_com.close()


