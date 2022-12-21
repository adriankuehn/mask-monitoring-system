import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense,Activation,Flatten,Dropout
from keras.layers import Conv2D,MaxPooling2D
from sklearn.model_selection import train_test_split


def darstellung_training(history):
    acc = history.history['acc']
    val_acc = history.history['val_acc']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(len(acc))
    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.legend()
    plt.figure()
    plt.plot(epochs, loss, 'bo', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.show()


train_data=np.load('Data.npy')
train_labels=np.load('Labels.npy')

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

filepath = "Saved_Models/saved-model-{epoch:02d}.hdf5"
model_checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath=filepath, save_best_only = False, save_weights_only = False, save_freq='epoch')
history=model.fit(train_data, train_labels, epochs=10,
  validation_split=0.2, shuffle=True, verbose=2, callbacks=[model_checkpoint])

darstellung_training(history)
