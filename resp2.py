#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 11:04:40 2022

@author: yuchenzhou
"""

import os

a=os.getcwd()

file_gas = open(a+'/ligand_g.mol2')
lines_gas = file_gas.readlines()
file_gas.close()

file_liq = open(a+'/ligand_l.mol2')
lines_liq = file_liq.readlines()
file_liq.close()

print(lines_gas[8])

atom_num=int(lines_gas[2].split()[0])
print('atom number =',atom_num)

print(lines_gas[8+atom_num-1])

resp_index=8

for i in lines_gas[resp_index:resp_index+atom_num]:
    resp_gas=i.split()[-1]
    print('RESP in gas phase:   '+resp_gas)
    resp_liq=lines_liq[resp_index].split()[-1]
    print('RESP in liquid phase:'+resp_liq)
    resp2=format(float(resp_gas)*0.5+float(resp_liq)*0.5,'.6f')
    print('RESP2(0.5):          '+resp2)   
    lines_gas[resp_index]=i.replace(resp_gas,resp2)
    resp_index+=1    

file_resp2 = open(a+'/ligand.mol2','w')
file_resp2.writelines(lines_gas)
file_resp2.close()

