import os
import pickle
import numpy as np
from PIL import Image as PLi
from tensorflow.keras.preprocessing import image as TFi



path = './pic/'
temp_path = './temp/temp.bmp'
l = 64 
s = 32
x_train = []
y_train = []

def cut (image_path, coords):
    
    obj = PLi.open(image_path)
    cuted = obj.crop(coords)
    cuted.save(temp_path)  

    large = TFi.load_img(temp_path, target_size=(l,l))
    small = TFi.load_img(temp_path, target_size=(s,s))

    y = TFi.img_to_array(large)
    x = TFi.img_to_array(small)
    
    y = y.reshape(l,l,3)
    x = x.reshape(s,s,3)
    
    y_train.append(y) 
    x_train.append(x) 

    
filelist = sorted(os.listdir(path))
for name in filelist:
    try:
        target = PLi.open(path+name)  
        width, height = target.size 
        print(name+' '+str(width)+'x'+str(height))
        h = height//l
        w = width//l
        for j in range(0, h+1):
            for i in range(0, w+1):
                crds = (l*i, l*j, l*(i+1), l*(j+1))
                cut(path+name, crds)
            
    except BaseException:
        print ('Err '+name)

x_train = np.array(x_train)
y_train = np.array(y_train)
x_train = x_train/255
y_train = y_train/255
print(x_train.shape)
print(y_train.shape)
with open('./temp/x_train.pickle', 'wb') as f:
    pickle.dump(x_train, f)
with open('./temp/y_train.pickle', 'wb') as f:
    pickle.dump(y_train, f)