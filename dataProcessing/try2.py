# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 17:16:40 2021

@author: Ken
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 14:20:51 2021

@author: Ken
"""

import numpy as np
import pandas as pd

numberofstep = 80
initial_gap = 100     # 10mm
step_size = 25


df = pd.read_excel("example.XLSX", index_col=None, header = 0,)
time_range = df['time'].max() - df['time'].min()
time_per_step = time_range/ numberofstep

distance_group  = [] 
Z_stat =  []
time_temp = 0
# for i in np.linspace(1,numberofstep,numberofstep):
#     time_stamp = df['time'].min() + time_per_step  * (i)
#     # Z =  [y for x,y in zip(df['time'],df['Z']) if x <= time_stamp and x > time_temp]
#     # #print(Z)
#     # Z_stat.append((np.mean(Z),np.std(Z)))
#     # distnace = [distance_group.append(100+25*i) for x in df['time'] if x <= time_stamp and x > time_temp]
#     distnace = [distance_group.append(100+25*i) for x in df['time'] if x <= time_stamp and x > time_temp]
#     time_temp = time_stamp
    
i = 0
temp = 0
for step in np.linspace(1,len(df),numberofstep):
    step_gap = int(np.floor(step) - temp)
    print(step,temp)
    [distance_group.append(100+25*i) for x in range(step_gap)]
    i = i +1
    temp = step
    
df['distance'] = np.array(distance_group).tolist()

Z =  [y for x,y in zip(df['time'],df['Z']) if x <= time_stamp and x > time_temp]
#print(Z)
Z_stat.append((np.mean(Z),np.std(Z)))

df_np = df.to_numpy()

df1 = df.groupby(['distance']).agg(['mean', 'count'])
df1.columns = [ ' '.join(str(i) for i in col) for col in df1.columns]
df1.reset_index(inplace=True)

df.to_excel('output.xlsx', engine='xlsxwriter')  

df1.to_excel('output_stat.xlsx', engine='xlsxwriter')  



# time = 176267516  ~= 176 s 


