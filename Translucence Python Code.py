#!/usr/bin/env python
# coding: utf-8

# In[1]:


from platform import python_version
import numpy as np
import tifffile as tif
import os 
from collections import defaultdict
#print(python_version())


# In[2]:


def threeDImageArrays(path):
    
    once = 0
    dimension1 = 0 
    dimension2 = 0 
    
    channels_dict = defaultdict(int)  
    
    for filename in os.listdir(path): 
        try:
            if(once == 0): 
                rememmap = tif.memmap( path + "/" + filename)
                dimension1 = rememmap.shape[0]
                dimension2 = rememmap.shape[1]
                once += 1
            channel_num = int(filename[10:12]) 
            
            channels_dict[channel_num] += 1
            
        except ValueError:
            pass  
                
    main_dict = dict() 
    
    for ch, Zs in channels_dict.items(): 
        main_dict[ch] = np.random.randint(0, 5, (int(Zs/4), dimension1 * 2, dimension2 * 2), 'uint16')
    
    i = 0
    for filename in os.listdir(path): 
        try:
            x = int(filename[0:3][0]) 
            y = int(filename[0:3][-1])
            Z = int(filename[5:8])
            channel_num = int(filename[10:12])
            rememmap = tif.memmap( path + "/" + filename) 
            
            if(x == 0 and y == 0): 
                main_dict[channel_num][Z,0:dimension1,0:dimension2] = rememmap
            elif(x == 0 and y == 1):
                main_dict[channel_num][Z,0:dimension1*2,dimension2:dimension2*2] = rememmap
            elif(x == 1 and y == 0):
                main_dict[channel_num][Z,dimension1:dimension1*2,0:dimension2] = rememmap
            elif(x == 1 and y == 1):
                main_dict[channel_num][Z,dimension1:dimension1*2,dimension2:dimension2*2] = rememmap
                
        except ValueError:
            pass 
        
    for i,array in main_dict.items(): 
        new_file_name = "channel" + str(i) + ".tif" 
        tif.imwrite(new_file_name, array, photometric='minisblack') 
        #tif.imwrite(new_file_name, array, photometric='rgb') 
    
    return tuple(main_dict.values()) 
                  
#path = 'test-data' 
#print(threeDImageArrays(path)) 

