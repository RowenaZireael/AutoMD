#/usr/bin/env python
"""
Created on Tue Apr 18 2023

@author: Rowena & ChatGPT
"""

import numpy as np
import MDAnalysis as mda
import matplotlib.pyplot as plt

# 加载动力学轨迹
u = mda.Universe('md.gro', 'md_center.xtc')

# 选择所有磷原子
lipids = u.select_atoms('name P31')

# 选择所有蛋白质原子
protein_atoms = u.select_atoms('protein')


time=0

# 定义空列表，用于存储每一帧蛋白质深度

x, y = [], []


# 循环遍历每一帧
for ts in u.trajectory:
    # 选择下层膜的磷原子
    
    lower_lipids = lipids.select_atoms('prop z < 36')

    # 计算下层膜磷原子的Z轴坐标的平均值并四舍五入到5个小数位
    
    lower_z_mean = np.around(lower_lipids.positions[:, 2].mean(), decimals=5)
   


    # 获取当前帧中蛋白质原子的Z轴坐标
    z_coords = protein_atoms.positions[:, 2]

    # 计算蛋白质嵌入膜深度
    z_max = z_coords.max()
 
    depth = z_max - lower_z_mean

    # 将当蛋白质嵌入膜的深度添加到列表中,将time添加到列表中
    x.append(time)
    y.append(depth)
    
    time+=0.01
y_value_mean = np.convolve(y, np.ones(500)/500, mode='valid')
x_mean = x[249:len(x)-250]
#average
y_mean = np.mean(y)
y_std = np.std(y)
#plot
plt.plot(x,y, marker='', linewidth=1, label = 'Protein Embedding Depth (Å)')
plt.plot(x_mean, y_value_mean, linewidth=1, label='5ns Avg (Å)')
plt.suptitle('Protein Embedding Depth',fontsize=16)
plt.title('Average = '+str(round(y_mean,3))+' '+'Å'+'     Standard Deviation = '+str(round(y_std,3))+' '+'Å',fontsize=12)                 
plt.xlabel('Time (ns)',fontsize=12)
plt.ylabel('Protein Embedding Depth (Å)',fontsize=12)
plt.legend(frameon=False)
plt.gca().ticklabel_format(style='sci', scilimits=(-1,3), axis='y')
plt.tight_layout()
plt.savefig('protein_depth.png',dpi=500, transparent = True) 
plt.close()


   
    



