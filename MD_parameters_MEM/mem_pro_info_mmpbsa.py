#/usr/bin/env python
"""
Created on Tue Apr 18 2023

@author: Rowena & ChatGPT
"""

import numpy as np
import MDAnalysis as mda

# 加载动力学轨迹
u = mda.Universe('femd.gro', 'femd_center.xtc')

# 选择所有磷原子
lipids = u.select_atoms('name P31')

# 选择所有蛋白质原子
protein_atoms = u.select_atoms('protein')

# 选择所有配体原子

MOL_atoms = u.select_atoms('resname MOL')

# 初始化空列表用于存储每一帧的膜厚度和膜中心位置
memthick_collection = []
memcenter_collection = []
frame_num=0

# 定义空列表，用于存储每一帧的Z轴最大值和最小值和Z坐标中心和磷脂膜中心到蛋白质中心的距离和配体最大Z坐标
z_max_list = []
z_min_list = []
z_mid_list = []
depth_list = []
distance_list = []
MOL_depth = []
# 循环遍历每一帧
for ts in u.trajectory:
    # 选择上层膜和下层膜的磷原子
    upper_lipids = lipids.select_atoms('prop z >= 36')
    lower_lipids = lipids.select_atoms('prop z < 36')

    # 计算上层膜和下层膜磷原子的Z轴坐标的平均值并四舍五入到5个小数位
    upper_z_mean = np.around(upper_lipids.positions[:, 2].mean(), decimals=5)
    lower_z_mean = np.around(lower_lipids.positions[:, 2].mean(), decimals=5)
   
    print('Frame '+str(frame_num))
    print('membrane upper leaf = '+str(upper_z_mean)+'     membrane lower leaf = '+str(lower_z_mean))
    frame_num+=1
    # 计算膜的中心Z轴坐标并四舍五入到5个小数位
    membrane_center = np.around((upper_z_mean + lower_z_mean) / 2, decimals=5)
    print('membrane center = '+str(membrane_center))
    # 计算膜的厚度并四舍五入到两个小数位
    membrane_thickness = np.around(np.abs(upper_z_mean - lower_z_mean), decimals=5)
    print('membrane thickness = '+str(membrane_thickness))
  
    # 将平均值添加到膜厚度和膜中心列表中
    memcenter_collection.append(membrane_center)
    memthick_collection.append(membrane_thickness)



    # 获取当前帧中蛋白质原子的Z轴坐标
    z_coords = protein_atoms.positions[:, 2]

    # 获取当前帧中蛋白质原子Z轴上的最大值和最小值,计算蛋白质Z坐标中心,计算蛋白质嵌入膜深度，计算膜中心到蛋白质中心距离
    z_max = z_coords.max()
    z_min = z_coords.min()
    z_mid = (z_max + z_min)/2
    depth = z_max - lower_z_mean
    distance = membrane_center - z_mid

    # 将当前帧的Z轴最大值和最小值和中心和蛋白质嵌入膜的深度添加到列表中,将膜中心到蛋白质中心的距离添加到列表中
    z_max_list.append(z_max)
    z_min_list.append(z_min)
    z_mid_list.append(z_mid)
    depth_list.append(depth)
    distance_list.append(distance)
    print(z_max)
    print(z_min)


    # 获取当前帧中配体原子的Z轴坐标
    z_MOL = MOL_atoms.positions[:, 2]
    # 获取当前帧中蛋白质原子Z轴上的最大值和最小值,计算蛋白质Z坐标中心,计算蛋白质嵌入膜深度，计算膜中心到蛋白质中心距离
    MOL_max = z_MOL.max()  
    lig_depth = MOL_max - lower_z_mean
    # 将当前帧的Z轴最大值和最小值和中心和蛋白质嵌入膜的深度添加到列表中,将膜中心到蛋白质中心的距离添加到列表中
    MOL_depth.append(lig_depth)
    



# 计算膜的平均中心Z轴坐标并四舍五入到5个小数位
membrane_center_mean = np.around(float(np.mean(memcenter_collection)) , decimals=5)
# 计算膜的平均厚度并四舍五入到5个小数位
membrane_thickness_mean = np.around(float(np.mean(memthick_collection)) , decimals=5)


# 计算蛋白质中心位置的平均值和标准差
z_mid_mean = np.around(float(np.mean(z_mid_list)), decimals=5)
z_mid_std = np.around(float(np.std(z_mid_list)), decimals=5)

# 计算膜中心和厚度的标准差并四舍五入到5个小数位
membrane_center_std = np.around(float(np.std(memcenter_collection)), decimals=5)
membrane_thickness_std = np.around(float(np.std(memthick_collection)), decimals=5)

# 计算嵌入膜深度的平均值和标准差
depth_mean = np.around(float(np.mean(depth_list)), decimals=5)
depth_std = np.around(float(np.std(depth_list)), decimals=5)

# 计算膜中心到蛋白质中心距离的平均值和标准差
distance_mean = np.around(float(np.mean(distance_list)), decimals=5)
distance_std = np.around(float(np.std(distance_list)), decimals=5)

# 计算配体嵌入膜深度的平均值和标准差
MOL_depth_mean = np.around(float(np.mean(MOL_depth)), decimals=5)
MOL_depth_std = np.around(float(np.std(MOL_depth)), decimals=5)


# 打印膜中心和厚度的平均值和标准差
print('-----------------------------------------------------')
print(f"Membrane center average: {membrane_center_mean} ± {membrane_center_std}")
print(f"Membrane thickness average: {membrane_thickness_mean} ± {membrane_thickness_std}")


# 打印蛋白质中心位置和嵌入膜深度的平均值和标准差
print('-----------------------------------------------------')
print(f"Protein center average: {z_mid_mean} ± {z_mid_std}")
print(f"Protein embedding depth average: {depth_mean} ± {depth_std}")

# 打印膜中心到蛋白质中心距离的平均值和标准差
print('-----------------------------------------------------')
print(f"Membrane center to protein center: {distance_mean} ± {distance_std}")
print('-----------------------------------------------------')

# 参数写入mmpbsa.in文件
file = open('mmpbsa.in')
lines = file.readlines()
file.close()

find_mthick=lines.index('  mthick               = 40.0                                           # Membrane thickness\n')
lines[find_mthick]='  mthick               = '+str(membrane_thickness_mean)+'\n'

find_mctrdz=lines.index('  mctrdz               = 0.0                                            # Distance to offset membrane in Z direction\n')
lines[find_mctrdz]='  mctrdz               = '+str(membrane_center_mean)+'\n'

file = open('mmpbsa.in','w')
file.writelines(lines)
file.close()
    
file_z = open('Z_Info.dat','w')
file_z.write('Membrane center             '+str(membrane_center_mean)+'\n')
file_z.write('Membrane thickness          '+str(membrane_thickness_mean)+'\n')
file_z.write('Protein center              '+str(z_mid_mean)+'\n')
file_z.write('Protein embedding depth     '+str(depth_mean)+'\n')
file_z.write('Pro_Mem_center_distance     '+str(distance_mean)+'\n')
file_z.write('Ligand embedding depth      '+str(MOL_depth_mean)+'\n')
file_z.close()
