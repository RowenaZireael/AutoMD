# Created on iPad.
# Author: Rowena Zireael

import re
import os
import numpy as np
import matplotlib.pyplot as plt

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
            y_axis_unit=re.search('\([^\)]+\)',y_axis).group()
            print(y_axis_unit)
            #find legend
            try:    
                find_l_start=re.search('s0 legend "[A-Za-z]+"',lines).span()
                legend=lines[find_l_start[0]+11:find_l_start[1]-1]+' '
                print(legend)
            except:
                #legend=input('Please customize legend:')
                legend='RMSD'
            #find data
            find_data=re.findall('[0-9]+\.[0-9]+  [0-9- ]+\.[0-9]+',lines)
            print(find_data)
            x, y=[], []
            for data in find_data:
                val=[float(i) for i in data.split(  )]             
                x.append(val[0])
                y.append(val[1])
            #average
            y_value_mean = np.convolve(y, np.ones(500)/500, mode='valid')
            x_mean = x[249:len(x)-250]
            
            y_mean = np.mean(y)
            y_std = np.std(y)
            #plot
            
            if max(y) > 0.6:
                plt.ylim((0,1))
            else:
                plt.ylim((0,0.6))

            plt.plot(x,y, marker='', label=legend+' '+y_axis_unit, linewidth=0.3)
            plt.plot(x_mean, y_value_mean, linewidth=1, label='5ns Avg'+' '+y_axis_unit)
            plt.suptitle(name[:-4],fontsize=16)
            plt.title('Average = '+str(round(y_mean,3))+' '+y_axis_unit[1:][:-1]+'     Standard Deviation = '+str(round(y_std,3))+' '+y_axis_unit[1:][:-1],fontsize=12)                 
            plt.xlabel(x_axis_label,fontsize=12)
            plt.ylabel(legend+' '+y_axis_unit,fontsize=12)
            plt.legend(frameon=False)
            plt.gca().ticklabel_format(style='sci', scilimits=(-2,3), axis='y')
            plt.tight_layout()
            plt.savefig(name[:-4]+'.png',dpi=500, transparent = True) 
            plt.close()
            
            
            
        