# Created on iPad.
# Author: Rowena Zireael

import re
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

file_dir="."
file_type=".xvg"

for root, dirs, files in os.walk(file_dir):
    for name in files:      
        if file_type in name:
            with open(name) as file:
                lines=file.read()
            #find xaxis label
            find_x=re.search('xaxis  label "[^"]+"',lines).span()
            print(find_x)
            x_axis_label=lines[find_x[0]+14:find_x[1]-1]
            print(x_axis_label)
            #find yaxis unit
            find_y=re.search('yaxis  label "[^"]+"',lines).span()
            print(find_y)
            y_axis=lines[find_y[0]:find_y[1]]
            #y_axis_unit=re.search('\([^\)]+\)',y_axis).group()
            #print(y_axis_unit)           
            #find data
            find_data=re.findall('[0-9]+           [0-9]+',lines)
            print(find_data)
            x, y=[], []
            for data in find_data:
                val=[float(i) for i in data.split(  )]             
                x.append(val[0]/1000)
                y.append(val[1])
            #average
            y_mean = np.mean(y)
            y_std = np.std(y)
            #plot
            plt.scatter(x,y, marker='|',linewidths=0.05,s=1000,color='black')
            plt.suptitle(name[:-4],fontsize=16)
            plt.title('Average = '+str(round(y_mean,3))+' '+'     Standard Deviation = '+str(round(y_std,3))+' ',fontsize=12)                 
            plt.xlabel('Time (ns)',fontsize=12)
            plt.ylabel('Number of Hydrogen Bonds',fontsize=12)  
            plt.gca().ticklabel_format(style='sci', scilimits=(-1,3), axis='y')
            plt.gca().yaxis.set_major_locator(MultipleLocator(1))
            #plt.gca().spines['right'].set_color('none')
            #plt.gca().spines['top'].set_color('none')
            plt.tight_layout()
            plt.savefig(name[:-4]+'.png',dpi=500, transparent = True) 
            plt.close()
            
            
            
        