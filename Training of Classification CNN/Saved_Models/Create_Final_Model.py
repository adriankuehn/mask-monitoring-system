##import tensorflow as tf
##import keras
##from keras.datasets import mnist
##from keras import models
##from keras import layers
##from keras.layers import Lambda
##from keras.utils import to_categorical
##from keras.models import model_from_json
##import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense,Activation,Flatten,Dropout
from keras.layers import Conv2D,MaxPooling2D


def Save_Model_Main(model):
    Index='__FINAL__RGB'
    model_json = model.to_json()                                                                                          
    with open("model"+str(Index)+".json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("model"+str(Index)+".h5")
    
def create_model():
    model=Sequential()
    model.add(Conv2D(32,(3,3),input_shape=(200,170,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Conv2D(64,(3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Flatten())
    model.add(Dropout(0.1))
    model.add(Dense(50,activation='relu'))
    model.add(Dense(1,activation='sigmoid'))
    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['acc'])
    model.summary()

    return(model)


Epoche = "07"  
print('Neu Laden der '+str(Epoche)+' Epoche')
model_F = create_model()
model_F.load_weights('saved-model-'+str(Epoche)+'.hdf5')
Save_Model_Main(model_F)



