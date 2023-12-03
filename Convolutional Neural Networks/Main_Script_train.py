# -*- coding: utf-8 -*-
"""CNN_machine_learning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1s2_gYvJeGY-0L1lCjiHKkPpx5GrshiQ2
"""

#Konstantinos Pasvantis
#Applied Computer Science - Aida
#email: aid23005@uom.edu.gr
#aid23005
from tensorflow import keras 
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
import matplotlib.pyplot as plt
import random
from google.colab import drive
import tensorflow as tf
import numpy as np
drive.mount('/content/drive')
#define some parametes related to specific training problem
batch_size = 128 #reduce this if you want to run this locally, at your pc
num_classes = 10 #this is problem specific
epochs = 10 # to save some time. Typically you need more that 100.

print('Splitting the Dataset...')
(X_train, y_train), (X_test, y_test) = keras.datasets.cifar10.load_data()
(X_train,y_train),(X_valid,y_valid)=(X_train[:40000],y_train[:40000]),(X_train[40000:],y_train[40000:])
#Scaling the data:
X_train=X_train/255
X_valid=X_valid/255
X_test=X_test/255
#Classes of Cifar-10
classes=['airplane','automobile', 'bird','cat','deer','dog','frog','horse','ship','truck']
print('Data Creation Completed')
print('We have '+str(X_train.shape[0]) + ' samples on train set of shape: '+ str(X_train.shape[1:4]) )
print('The validation set consists of '+str(X_valid.shape[0])+' paradigms and the test set has '+str(X_train.shape[0])+' images to predict.')

print('Lets see some images of every class!')
#Printing 4 random images class by class in grayscale
class_to_demonstrate=0
while (sum(y_train == class_to_demonstrate) > 4):
  tmp_idxs_to_use = np.where(y_train== class_to_demonstrate)
  plt.figure()
  # plot 4 images as gray scale
  plt.subplot(221)
  plt.imshow(X_train[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_train==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  plt.subplot(222)
  plt.imshow(X_train[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_train==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  plt.subplot(223)
  plt.imshow(X_train[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_train==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  plt.subplot(224)
  plt.imshow(X_train[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_train==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  tmp_title = 'Images of ' + str(classes[class_to_demonstrate])
  plt.suptitle(tmp_title)
  # update the class to demonstrate index
  class_to_demonstrate = class_to_demonstrate + 1

y_train = keras.utils.to_categorical(y_train, num_classes)
y_valid= keras.utils.to_categorical(y_valid, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

#First Model
# Here we define the first model
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(32, 32, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(num_classes, activation='softmax'))
#Here we compile the model 
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=tf.keras.optimizers.Adam(),
              metrics=['accuracy'])
print('CNN Topology setup Completed')
print('Training the Model, please wait this may take a while...')
# Fit model parameters, given a set of training data
model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(X_valid,y_valid)) 
# calculate some common performance scores and save the first model
score = model.evaluate(X_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
model.save('/content/drive/MyDrive/CIFAR-10-CNN.h5')

#Second Model (MSE)
# Here we define the second model
print('Splitting the Dataset...')
(X_train, y_train), (X_test, y_test) = keras.datasets.cifar10.load_data()
(X_train,y_train),(X_valid,y_valid)=(X_train[:40000],y_train[:40000]),(X_train[40000:],y_train[40000:])
#Scaling the data:
X_train=X_train/255
X_valid=X_valid/255
X_test=X_test/255
y_train = keras.utils.to_categorical(y_train, num_classes)
y_valid= keras.utils.to_categorical(y_valid, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(32, 32, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(num_classes, activation='softmax'))
#Here we compile the model 
model.compile(loss=keras.losses.mse,
              optimizer=tf.keras.optimizers.Adam(),
              metrics=['accuracy'])
print('CNN Topology setup Completed')
print('Training the Model, please wait this may take a while...')
# Fit model parameters, given a set of training data
model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(X_valid,y_valid)) 
# calculate some common performance scores and save the model
score = model.evaluate(X_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
model.save('/content/drive/MyDrive/CIFAR-10-CNN_2.h5')
print('The model is saved')

#Third Model
# Here we define the third model
print('Splitting the Dataset...')
(X_train, y_train), (X_test, y_test) = keras.datasets.cifar10.load_data()
(X_train,y_train),(X_valid,y_valid)=(X_train[:40000],y_train[:40000]),(X_train[40000:],y_train[40000:])
#Scaling the data:
X_train=X_train/255
X_valid=X_valid/255
X_test=X_test/255
y_train = keras.utils.to_categorical(y_train, num_classes)
y_valid= keras.utils.to_categorical(y_valid, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
# Here we define the second model
model = Sequential()
model.add(Conv2D(128, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(10, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
print('Training the Model, please wait this may take a while...')
# fit model parameters, given a set of training data
model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(X_valid,y_valid)) 
# calculate some common performance scores 
score = model.evaluate(X_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
model.save('/content/drive/MyDrive/CIFAR-10-CNN_3.h5')
print('The model is saved')