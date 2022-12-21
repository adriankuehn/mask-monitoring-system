import os
import cv2
import numpy as np


Data=[]
Labels=[]
for img_path in os.listdir('archive/with_mask'):
    img=cv2.imread('archive/with_mask/'+img_path)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
    resized=cv2.resize(img,(170, 200))
    Data.append(resized)
    Labels.append(1)

print('Hälfte Fertig')
for img_path in os.listdir('archive/without_mask'):
    img=cv2.imread('archive/without_mask/'+img_path)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
    resized=cv2.resize(img,(170, 200))
    Data.append(resized)
    Labels.append(0)

Data=np.array(Data)/255.0
Labels=np.array(Labels)

print('Data.shape: ', Data.shape)
Data=np.reshape(Data,(Data.shape[0],200, 170,3))
print('Data.shape NEUEUE: ', Data.shape)
print('Labels.shape: ', Labels.shape)
    
np.save('Data', Data)
np.save('Labels', Labels)
print('Fertig')
