# -*- coding: utf-8 -*-
"""CNN_ML_test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XjEtZkmnLs5A1l_9PkrdALsKwAPkI7p4
"""

#Konstantinos Pasvantis
#Applied Computer Science - Aida
#email: aid23005@uom.edu.gr
#aid23005
from tensorflow import keras #remember that keras is now included in tensorflow
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
import matplotlib.pyplot as plt
import random
import tensorflow as tf
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score , confusion_matrix
import numpy as np
(X_train, y_train), (X_test, y_test) = keras.datasets.cifar10.load_data()
(X_train,y_train),(X_valid,y_valid)=(X_train[:40000],y_train[:40000]),(X_train[40000:],y_train[40000:])
classes=['airplane','automobile', 'bird','cat','deer','dog','frog','horse','ship','truck']
X_train=X_train/255
X_valid=X_valid/255
X_test=X_test/255

#Load the first Model and predict class of test and train images
loaded_model = tf.keras.models.load_model('/content/drive/MyDrive/CIFAR-10-CNN.h5')
y_train_predictions_vectorized = loaded_model.predict(X_train)
y_train_predictions = np.argmax(y_train_predictions_vectorized, axis=1)
y_test_predictions_vectorized = loaded_model.predict(X_test)
y_test_predictions = np.argmax(y_test_predictions_vectorized, axis=1)

#Have a look at some common metric scores 
acc_train=accuracy_score(y_train, y_train_predictions)
acc_test = accuracy_score(y_test, y_test_predictions)
pre_train=precision_score(y_train, y_train_predictions, average='macro')
pre_test = precision_score(y_test, y_test_predictions, average='macro')
rec_train=recall_score(y_train, y_train_predictions, average='macro')
rec_test = recall_score(y_test, y_test_predictions, average='macro')
f1_train=f1_score(y_train, y_train_predictions, average='macro')
f1_test = f1_score(y_test, y_test_predictions, average='macro')
#print the scores
print('')
print(' Printing performance scores:')
print('')

print('Accuracy scores of CNN classifier are:',
      'train: {:.2f}'.format(acc_train), 'and test: {:.2f}.'.format(acc_test))
print('Precision scores of CNN classifier are:',
      'train: {:.2f}'.format(pre_train), 'and test: {:.2f}.'.format(pre_test))
print('Recall scores of CNN classifier are:',
      'train: {:.2f}'.format(rec_train), 'and test: {:.2f}.'.format(rec_test))
print('F1 scores of CNN classifier are:',
      'train: {:.2f}'.format(f1_train), 'and test: {:.2f}.'.format(f1_test))
print('')
print('Printing the Confusion matrix:')
print(confusion_matrix(y_test_predictions,y_test))

len(np.where(y_test==1)[0])

print('Time to see the predicted images of the first model')

class_to_demonstrate=0
while (sum(y_train == class_to_demonstrate) > 4):
  tmp_idxs_to_use = np.where(y_test_predictions== class_to_demonstrate)
  plt.figure()
  # plot 4 images as gray scale
  plt.subplot(221)
  plt.imshow(X_test[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_test_predictions==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  plt.subplot(222)
  plt.imshow(X_test[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_test_predictions==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  plt.subplot(223)
  plt.imshow(X_test[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_test_predictions==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  plt.subplot(224)
  plt.imshow(X_test[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_test_predictions==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  tmp_title = 'What my CNN predicted to be  ' + str(classes[class_to_demonstrate])
  plt.suptitle(tmp_title)
  # update the class to demonstrate index
  class_to_demonstrate = class_to_demonstrate + 1

#Second Model (MSE)
#Load the second Model and predict class of test and train images
(X_train, y_train), (X_test, y_test) = keras.datasets.cifar10.load_data()
(X_train,y_train),(X_valid,y_valid)=(X_train[:40000],y_train[:40000]),(X_train[40000:],y_train[40000:])
classes=['airplane','automobile', 'bird','cat','deer','dog','frog','horse','ship','truck']
X_train=X_train/255
X_valid=X_valid/255
X_test=X_test/255
loaded_model = tf.keras.models.load_model('/content/drive/MyDrive/CIFAR-10-CNN_2.h5')
y_train_predictions_vectorized = loaded_model.predict(X_train)
y_train_predictions = np.argmax(y_train_predictions_vectorized, axis=1)
y_test_predictions_vectorized = loaded_model.predict(X_test)
y_test_predictions = np.argmax(y_test_predictions_vectorized, axis=1)
#Have a look at some common metric scores 
acc_train=accuracy_score(y_train, y_train_predictions)
acc_test = accuracy_score(y_test, y_test_predictions)
pre_train=precision_score(y_train, y_train_predictions, average='macro')
pre_test = precision_score(y_test, y_test_predictions, average='macro')
rec_train=recall_score(y_train, y_train_predictions, average='macro')
rec_test = recall_score(y_test, y_test_predictions, average='macro')
f1_train=f1_score(y_train, y_train_predictions, average='macro')
f1_test = f1_score(y_test, y_test_predictions, average='macro')
#print the scores
print('')
print(' Printing performance scores:')
print('')

print('Accuracy scores of CNN classifier are:',
      'train: {:.2f}'.format(acc_train), 'and test: {:.2f}.'.format(acc_test))
print('Precision scores of CNN classifier are:',
      'train: {:.2f}'.format(pre_train), 'and test: {:.2f}.'.format(pre_test))
print('Recall scores of CNN classifier are:',
      'train: {:.2f}'.format(rec_train), 'and test: {:.2f}.'.format(rec_test))
print('F1 scores of CNN classifier are:',
      'train: {:.2f}'.format(f1_train), 'and test: {:.2f}.'.format(f1_test))
print('')
print('Printing the Confusion matrix:')
print(confusion_matrix(y_test_predictions,y_test))

print('Time to see the predicted images of the second model')
class_to_demonstrate=0
while (sum(y_train == class_to_demonstrate) > 4):
  tmp_idxs_to_use = np.where(y_test_predictions== class_to_demonstrate)
  plt.figure()
  # plot 4 images as gray scale
  plt.subplot(221)
  plt.imshow(X_test[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_test_predictions==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  plt.subplot(222)
  plt.imshow(X_test[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_test_predictions==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  plt.subplot(223)
  plt.imshow(X_test[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_test_predictions==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  plt.subplot(224)
  plt.imshow(X_test[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_test_predictions==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  tmp_title = 'What my CNN predicted to be  ' + str(classes[class_to_demonstrate])
  plt.suptitle(tmp_title)
  # update the class to demonstrate index
  class_to_demonstrate = class_to_demonstrate + 1

#Third Model (Extra convolutioal Layers)
#Load the third Model and predict class of test and train images
(X_train, y_train), (X_test, y_test) = keras.datasets.cifar10.load_data()
(X_train,y_train),(X_valid,y_valid)=(X_train[:40000],y_train[:40000]),(X_train[40000:],y_train[40000:])
classes=['airplane','automobile', 'bird','cat','deer','dog','frog','horse','ship','truck']
X_train=X_train/255
X_valid=X_valid/255
X_test=X_test/255
loaded_model = tf.keras.models.load_model('/content/drive/MyDrive/CIFAR-10-CNN_3.h5')
y_train_predictions_vectorized = loaded_model.predict(X_train)
y_train_predictions = np.argmax(y_train_predictions_vectorized, axis=1)
y_test_predictions_vectorized = loaded_model.predict(X_test)
y_test_predictions = np.argmax(y_test_predictions_vectorized, axis=1)
#Have a look at some common metric scores 
acc_train=accuracy_score(y_train, y_train_predictions)
acc_test = accuracy_score(y_test, y_test_predictions)
pre_train=precision_score(y_train, y_train_predictions, average='macro')
pre_test = precision_score(y_test, y_test_predictions, average='macro')
rec_train=recall_score(y_train, y_train_predictions, average='macro')
rec_test = recall_score(y_test, y_test_predictions, average='macro')
f1_train=f1_score(y_train, y_train_predictions, average='macro')
f1_test = f1_score(y_test, y_test_predictions, average='macro')
#print the scores
print('')
print(' Printing performance scores:')
print('')

print('Accuracy scores of third model of CNN classifier are:',
      'train: {:.2f}'.format(acc_train), 'and test: {:.2f}.'.format(acc_test))
print('Precision scores of third model of CNN classifier are:',
      'train: {:.2f}'.format(pre_train), 'and test: {:.2f}.'.format(pre_test))
print('Recall scores ofthird model of CNN classifier are:',
      'train: {:.2f}'.format(rec_train), 'and test: {:.2f}.'.format(rec_test))
print('F1 scores of third model of CNN classifier are:',
      'train: {:.2f}'.format(f1_train), 'and test: {:.2f}.'.format(f1_test))
print('')
print('Printing the Confusion matrix:')
print(confusion_matrix(y_test_predictions,y_test))

print('Time to see the predicted images of the third model')
class_to_demonstrate=0
while (sum(y_train == class_to_demonstrate) > 4):
  tmp_idxs_to_use = np.where(y_test_predictions== class_to_demonstrate)
  plt.figure()
  # plot 4 images as gray scale
  plt.subplot(221)
  plt.imshow(X_test[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_test_predictions==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  plt.subplot(222)
  plt.imshow(X_test[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_test_predictions==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  plt.subplot(223)
  plt.imshow(X_test[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_test_predictions==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  plt.subplot(224)
  plt.imshow(X_test[tmp_idxs_to_use[0][random.randint(0,len(np.where(y_test_predictions==class_to_demonstrate)[0]))], :, :, 0], cmap=plt.get_cmap('gray'))
  tmp_title = 'What my CNN predicted to be  ' + str(classes[class_to_demonstrate])
  plt.suptitle(tmp_title)
  # update the class to demonstrate index
  class_to_demonstrate = class_to_demonstrate + 1