#!/usr/bin/env python
# coding: utf-8

# In[33]:


from platform import python_version
import numpy as np
import tifffile as tif
import os
from collections import defaultdict
#print(python_version())


# In[34]:


def threeDImageArrays(path):
    
    once = 0
    dimension1 = 0 # A dimension of 3D array
    dimension2 = 0 # A dimension of 3D array
    
    channels_dict = defaultdict(int) # This dictionary keeps track of how many channels there are and the number of Z values
    
    for filename in os.listdir(path): # Running through the file names first to see which dimensions the 3D Array should be
        try:
            if(once == 0): # Assuming all the files the same size, the dimensions of the first file is taken
                rememmap = tif.memmap( path + "/" + filename)
                dimension1 = rememmap.shape[0]
                dimension2 = rememmap.shape[1]
                once += 1
            channel_num = int(filename[10:12]) # Temporary variable for the channel number
            
            channels_dict[channel_num] += 1 # Sets channel number as key and increments the value by one
            
        except ValueError:
            pass  # This is in place to avoid errors being thrown for unknown file names
                
    main_dict = dict() # The dictionary which will keep track of the #3D array associated with each channel
    
    for ch, Zs in channels_dict.items(): # For each channel create a 3D array based on the Z value
        main_dict[ch] = np.random.randint(0, 5, (int(Zs/4), dimension1 * 2, dimension2 * 2), 'uint16')
    
    i = 0
    for filename in os.listdir(path): # For loops through all files in the directory
        try:
            x = int(filename[0:3][0]) # Separate the file name string and turn it into a int
            y = int(filename[0:3][-1])
            Z = int(filename[5:8])
            channel_num = int(filename[10:12])
            rememmap = tif.memmap( path + "/" + filename) # Put the TIFF into the memory-mapped numpy array
            
            if(x == 0 and y == 0): # These if statements check to see where the tile should go in the array and proceed to place it there
                main_dict[channel_num][Z,0:dimension1,0:dimension2] = rememmap
            elif(x == 0 and y == 1):
                main_dict[channel_num][Z,0:dimension1*2,dimension2:dimension2*2] = rememmap
            elif(x == 1 and y == 0):
                main_dict[channel_num][Z,dimension1:dimension1*2,0:dimension2] = rememmap
            elif(x == 1 and y == 1):
                main_dict[channel_num][Z,dimension1:dimension1*2,dimension2:dimension2*2] = rememmap
                
        except ValueError:
            pass # This is in place to avoid errors being thrown for unknown file names
        
    for i,array in main_dict.items(): 
        new_file_name = "channel" + str(i) + ".tif" # Create a file names for TIFF files
        tif.imwrite(new_file_name, array, photometric='minisblack') # Creates a TIFF file and writes the array to it
        #tif.imwrite(new_file_name, array, photometric='rgb') # This call instead of the one before would make the TIFF files in color
    
    return tuple(main_dict.values()) # Return the 3D arrays in the form of a tuple
                 
#path = 'test-data' # An example path
#print(threeDImageArrays(path)) # An example call to the sample path

