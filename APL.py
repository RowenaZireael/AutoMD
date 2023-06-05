#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 20:42:01 2023

@author: yuchen
"""
import re
import numpy as np
import matplotlib.pyplot as plt

file_type=".xvg"
name=input('Please enter name of input file:')


with open(name+file_type) as file:
    lines=file.read()
#find xaxis label
find_x=re.search('xaxis  label "[^"]+"',lines).span()
print(find_x)
x_axis_label=lines[find_x[0]+14:find_x[1]-1]
print(x_axis_label)
#find yaxis unit
find_y=re.search('yaxis  label "[^"]+"',lines).span()
print(find_y)
y_axis_unit='Angstrom$^2$'
print(y_axis_unit)
#find legend

#find data
find_data=re.findall('[0-9]+\.[0-9]+  [0-9- ]+\.[0-9]+ [0-9- ]+\.[0-9]+',lines)
print(find_data)
x, y=[], []
for data in find_data:
    val=[float(i) for i in data.split(  )]             
    x.append(val[0])
    y.append(val[1]*val[2]*100/59)
    
#plot
plt.plot(x,y, marker='', label='Area per lipid')
plt.suptitle(name,fontsize=16)

plt.title('Average = '+str(round(np.mean(y),3))+' (Å$^2$)     Standard Deviation = '+str(round(np.std(y),3))+' (Å$^2$)',fontsize=9)

plt.xlabel(x_axis_label)


plt.ylabel(y_axis_unit)

plt.legend()
plt.gca().ticklabel_format(style='sci', scilimits=(-1,3), axis='y')
plt.savefig(name+'.png',dpi=500) 
plt.close()