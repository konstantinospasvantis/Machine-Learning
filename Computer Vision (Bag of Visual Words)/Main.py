# -*- coding: utf-8 -*-
"""BoVW.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bNxoQWusjG6svKzIISlkWRffX8Kv7yAx
"""



pip install split-folders[full] #Installing the library for folder splitting into train and test data

#Using the splitfolers library to split the data into 2 folders, train and test
import splitfolders
from google.colab import drive
drive.mount('/content/drive')
input_folder='/content/drive/MyDrive/ShoesNO'
splitfolders.ratio(input_folder, output="/content/drive/MyDrive/Splitted_Dataset",
    seed=17, ratio=(.8,0, .2),group_prefix=None)

import cv2
import os
from sklearn.cluster import MiniBatchKMeans #KMeans
import numpy as np
#import secondary functions that will be used very frequent
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


#-----------------------------------------------------------------------------------------
#---------------- SUPPORTING FUNCTIONS GO HERE -------------------------------------------
#-----------------------------------------------------------------------------------------

# return a dictionary that holds all images category by category.
def load_images_from_folder(folder, inputImageSize ):
    images = {}
    for filename in os.listdir(folder):
        category = []
        path = folder + "/" + filename
        for cat in os.listdir(path):
            img = cv2.imread(path + "/" + cat)
            #print(' .. parsing image', cat)
            if img is not None:
                # grayscale it
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                #resize it, if necessary
                img = cv2.resize(img, (inputImageSize[0], inputImageSize[1]))

                category.append(img)
        images[filename] = category
        print(' . Finished parsing images. What is next?')
    return images


#Create Descriptors using SIFT
# Takes one parameter that is images dictionary
# Return an array whose first index holds the decriptor_list without an order
# And the second index holds the sift_vectors dictionary which holds the descriptors but this is seperated class by class
def detector_features(images):
    print(' . start detecting points and calculating features for a given image set')
    detector_vectors = {}
    descriptor_list = []
    #sift = cv2.xfeatures2d.SIFT_create()
    detectorToUse = cv2.xfeatures2d.SIFT_create()
    #detectorToUse = cv2.ORB_create()
    for nameOfCategory, availableImages in images.items():
        features = []
        for img in availableImages: # reminder: val
            kp, des = detectorToUse.detectAndCompute(img, None)
            descriptor_list.extend(des)
            features.append(des)
        detector_vectors[nameOfCategory] = features
        print(' . finished detecting points and calculating features for a given image set')
    return [descriptor_list, detector_vectors] # be aware of the []! this is ONE output as a list

# Creates descriptors using ORB
# Takes one parameter that is images dictionary
# Return an array whose first index holds the decriptor_list without an order
# And the second index holds the sift_vectors dictionary which holds the descriptors but this is seperated class by class
def detector_features_ORB(images):
    print(' . start detecting points and calculating features for a given image set')
    detector_vectors = {}
    descriptor_list = []
    #sift = cv2.xfeatures2d.SIFT_create()
    detectorToUse = cv2.ORB_create()
    #detectorToUse = cv2.ORB_create()
    for nameOfCategory, availableImages in images.items():
        features = []
        for img in availableImages: # reminder: val
            kp, des = detectorToUse.detectAndCompute(img, None)

            descriptor_list.extend(des)
            features.append(des)
        detector_vectors[nameOfCategory] = features
        print(' . finished detecting points and calculating features for a given image set')
    return [descriptor_list, detector_vectors] # be aware of the []! this is ONE output as a list


# A k-means clustering algorithm who takes 2 parameter which is number
# of cluster(k) and the other is descriptors list(unordered 1d array)
# Returns an array that holds central points.
def kmeansVisualWordsCreation(k, descriptor_list):
    print(' . calculating central points for the existing feature values.')
    #kmeansModel = KMeans(n_clusters = k, n_init=10)
    batchSize = np.ceil(descriptor_list.__len__()/50).astype('int')
    kmeansModel = MiniBatchKMeans(n_clusters=k, batch_size=batchSize, verbose=0,random_state=0)
    kmeansModel.fit(descriptor_list)
    visualWords = kmeansModel.cluster_centers_ # a.k.a. centers of reference
    print(' . done calculating central points for the given feature set.')
    return visualWords, kmeansModel

#Creation of the histograms. To create our each image by a histogram. We will create a vector of k values for each
# image. For each keypoints in an image, we will find the nearest center, defined using training set
# and increase by one its value
def mapFeatureValsToHistogram (DataFeaturesByClass, visualWords, TrainedKmeansModel):
    #depenting on the approach you may not need to use all inputs
    histogramsList = []
    targetClassList = []
    numberOfBinsPerHistogram = visualWords.shape[0]

    for categoryIdx, featureValues in DataFeaturesByClass.items():
        for tmpImageFeatures in featureValues: #yes, we check one by one the values in each image for all images
            tmpImageFeatures=tmpImageFeatures.astype(float)
            tmpImageHistogram = np.zeros(numberOfBinsPerHistogram)
            tmpIdx = list((TrainedKmeansModel.predict(tmpImageFeatures)))
            clustervalue, visualWordMatchCounts = np.unique(tmpIdx, return_counts=True)
            tmpImageHistogram[clustervalue] = visualWordMatchCounts
            # do not forget to normalize the histogram values
            numberOfDetectedPointsInThisImage = tmpIdx.__len__()
            tmpImageHistogram = tmpImageHistogram/numberOfDetectedPointsInThisImage
            #now update the input and output coresponding lists
            histogramsList.append(tmpImageHistogram)
            targetClassList.append(categoryIdx)

    return histogramsList, targetClassList

#here we run the code
#define a fixed image size to work with
inputImageSize = [200, 200, 3] 
#define the path to train and test files
TrainImagesFilePath ='/content/drive/MyDrive/Splitted_Dataset/train'
TestImagesFilePath = '/content/drive/MyDrive/Splitted_Dataset/test'
#load the train images
trainImages = load_images_from_folder(TrainImagesFilePath, inputImageSize)  # take all images category by category for train set
#calculate points and descriptor values per image
trainDataFeatures = detector_features(trainImages)
# Takes the descriptor list which is unordered one
TrainDescriptorList = trainDataFeatures[0]


#create the central points for the histograms using k means.
#here we use a rule of the thumb to create the expected number of cluster centers
numberOfClasses = trainImages.__len__() #retrieve num of classes from dictionary
possibleNumOfCentersToUse = 10 * numberOfClasses
visualWords, TrainedKmeansModel = kmeansVisualWordsCreation(possibleNumOfCentersToUse, TrainDescriptorList)
# Takes the sift feature values that is seperated class by class for train data, we need this to calculate the histograms
trainBoVWFeatureVals = trainDataFeatures[1]

#create the train input train output format
trainHistogramsList, trainTargetsList = mapFeatureValsToHistogram(trainBoVWFeatureVals, visualWords, TrainedKmeansModel)
#X_train = np.asarray(trainHistogramsList)
#X_train = np.concatenate(trainHistogramsList, axis=0)
X_train = np.stack(trainHistogramsList, axis= 0)

# Convert Categorical Data For Scikit-Learn
from sklearn import preprocessing

# Create a label (category) encoder object
labelEncoder = preprocessing.LabelEncoder()
labelEncoder.fit(trainTargetsList)
#convert the categories from strings to names
y_train = labelEncoder.transform(trainTargetsList)

"""# Training and evaluating"""

# train and evaluate the classifiers
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
print('Accuracy of K-NN classifier on training set: {:.2f}'.format(knn.score(X_train, y_train)))

from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(max_depth=7).fit(X_train, y_train)
print('Accuracy of Decision Tree classifier on training set: {:.2f}'.format(clf.score(X_train, y_train)))

from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)
print('Accuracy of GNB classifier on training set: {:.2f}'.format(gnb.score(X_train, y_train)))

from sklearn.svm import SVC
svm = SVC()
svm.fit(X_train, y_train)
print('Accuracy of SVM classifier on training set: {:.2f}'.format(svm.score(X_train, y_train)))

# ----------------------------------------------------------------------------------------
#now run the same things on the test data.
# DO NOT FORGET: you use the same visual words, created using training set.

#load the train images
testImages = load_images_from_folder(TestImagesFilePath, inputImageSize)  # take all images category by category for train set

#calculate points and descriptor values per image
testDataFeatures = detector_features(testImages)

# Takes the sift feature values that is seperated class by class for train data, we need this to calculate the histograms
testBoVWFeatureVals = testDataFeatures[1]

#create the test input / test output format
testHistogramsList, testTargetsList = mapFeatureValsToHistogram(testBoVWFeatureVals, visualWords, TrainedKmeansModel)
X_test = np.array(testHistogramsList)
labelEncoder.fit(trainTargetsList)

y_test = labelEncoder.transform(testTargetsList)

#classification tree
# predict outcomes for test data and calculate the test scores
y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)
#calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

#print the scores
print('')
print(' Printing performance scores using Sift for 80/20 train-test:')
print('')

print('Accuracy scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')

# knn predictions
#now check for both train and test data, how well the model learned the patterns
y_pred_train = knn.predict(X_train)
y_pred_test = knn.predict(X_test)
#calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

#print the scores
print('Accuracy scores of K-NN classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of K-NN classifie classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of K-NN classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of K-NN classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')


#naive Bayes
# now check for both train and test data, how well the model learned the patterns
y_pred_train = gnb.predict(X_train)
y_pred_test = gnb.predict(X_test)
# calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

# print the scores
print('Accuracy scores of GNB classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of GBN classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of GNB classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of GNB classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')


#support vector machines
# now check for both train and test data, how well the model learned the patterns
y_pred_train = svm.predict(X_train)
y_pred_test = svm.predict(X_test)
# calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

# print the scores
print('Accuracy scores of SVM classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of SVM classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of SVM classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of SVM classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')

"""# **ORB for 80/20**"""

print('Time to see the results using the ORB descriptor')
#calculate points and descriptor values per image
trainDataFeatures = detector_features_ORB(trainImages)
# Takes the descriptor list which is unordered one
TrainDescriptorList = trainDataFeatures[0]

#create the central points for the histograms using k means.
#here we use a rule of the thumb to create the expected number of cluster centers
numberOfClasses = trainImages.__len__() #retrieve num of classes from dictionary
possibleNumOfCentersToUse = 10 * numberOfClasses
visualWords, TrainedKmeansModel = kmeansVisualWordsCreation(possibleNumOfCentersToUse, TrainDescriptorList)
# Takes the sift feature values that is seperated class by class for train data, we need this to calculate the histograms
trainBoVWFeatureVals = trainDataFeatures[1]

#create the train input train output format
trainHistogramsList, trainTargetsList = mapFeatureValsToHistogram(trainBoVWFeatureVals, visualWords, TrainedKmeansModel)
#X_train = np.asarray(trainHistogramsList)
#X_train = np.concatenate(trainHistogramsList, axis=0)
X_train = np.stack(trainHistogramsList, axis= 0)

# Convert Categorical Data For Scikit-Learn
from sklearn import preprocessing

# Create a label (category) encoder object
labelEncoder = preprocessing.LabelEncoder()
labelEncoder.fit(trainTargetsList)
#convert the categories from strings to names
y_train = labelEncoder.transform(trainTargetsList)

# train and evaluate the classifiers
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
print('Accuracy of K-NN classifier on training set: {:.2f}'.format(knn.score(X_train, y_train)))


from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(max_depth=7).fit(X_train, y_train)
print('Accuracy of Decision Tree classifier on training set: {:.2f}'.format(clf.score(X_train, y_train)))


from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)
print('Accuracy of GNB classifier on training set: {:.2f}'.format(gnb.score(X_train, y_train)))


from sklearn.svm import SVC
svm = SVC()
svm.fit(X_train, y_train)
print('Accuracy of SVM classifier on training set: {:.2f}'.format(svm.score(X_train, y_train)))

#load the train images
testImages = load_images_from_folder(TestImagesFilePath, inputImageSize)  # take all images category by category for train set

#calculate points and descriptor values per image
testDataFeatures = detector_features_ORB(testImages)

# Takes the sift feature values that is seperated class by class for train data, we need this to calculate the histograms
testBoVWFeatureVals = testDataFeatures[1]

#create the test input / test output format
testHistogramsList, testTargetsList = mapFeatureValsToHistogram(testBoVWFeatureVals, visualWords, TrainedKmeansModel)
X_test = np.array(testHistogramsList)
labelEncoder.fit(trainTargetsList)

y_test = labelEncoder.transform(testTargetsList)


#classification tree
# predict outcomes for test data and calculate the test scores
y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)
#calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

#print the scores
print('')
print(' Printing performance scores using ORB for 80/20 train-test:')
print('')

print('Accuracy scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')

# knn predictions
#now check for both train and test data, how well the model learned the patterns
y_pred_train = knn.predict(X_train)
y_pred_test = knn.predict(X_test)
#calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

#print the scores
print('Accuracy scores of K-NN classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of K-NN classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of K-NN classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of K-NN classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')


#naive Bayes
# now check for both train and test data, how well the model learned the patterns
y_pred_train = gnb.predict(X_train)
y_pred_test = gnb.predict(X_test)
# calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

# print the scores
print('Accuracy scores of GNB classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of GBN classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of GNB classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of GNB classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')


#support vector machines
# now check for both train and test data, how well the model learned the patterns
y_pred_train = svm.predict(X_train)
y_pred_test = svm.predict(X_test)
# calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

# print the scores
print('Accuracy scores of SVM classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of SVM classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of SVM classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of SVM classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')

"""# Sift for 60/40"""

#Here we pass onto the second part of the assignment, splitting the dataset into 60/40
input_folder='/content/drive/MyDrive/ShoesNO'
splitfolders.ratio(input_folder, output="/content/drive/MyDrive/Splitted_Dataset(2)",
    seed=17, ratio=(.6,0, .4),group_prefix=None)

#here we run the code for the second part
#define the path to train and test files
TrainImagesFilePath ='/content/drive/MyDrive/Splitted_Dataset(2)/train'
TestImagesFilePath = '/content/drive/MyDrive/Splitted_Dataset(2)/test'
#load the train images
trainImages = load_images_from_folder(TrainImagesFilePath, inputImageSize)  # take all images category by category for train set
#calculate points and descriptor values per image
trainDataFeatures = detector_features(trainImages)
# Takes the descriptor list which is unordered one
TrainDescriptorList = trainDataFeatures[0]


#create the central points for the histograms using k means.
#here we use a rule of the thumb to create the expected number of cluster centers
numberOfClasses = trainImages.__len__() #retrieve num of classes from dictionary
possibleNumOfCentersToUse = 10 * numberOfClasses
visualWords, TrainedKmeansModel = kmeansVisualWordsCreation(possibleNumOfCentersToUse, TrainDescriptorList)
# Takes the sift feature values that is seperated class by class for train data, we need this to calculate the histograms
trainBoVWFeatureVals = trainDataFeatures[1]

#create the train input train output format
trainHistogramsList, trainTargetsList = mapFeatureValsToHistogram(trainBoVWFeatureVals, visualWords, TrainedKmeansModel)
#X_train = np.asarray(trainHistogramsList)
#X_train = np.concatenate(trainHistogramsList, axis=0)
X_train = np.stack(trainHistogramsList, axis= 0)

# Convert Categorical Data For Scikit-Learn
from sklearn import preprocessing

# Create a label (category) encoder object
labelEncoder = preprocessing.LabelEncoder()
labelEncoder.fit(trainTargetsList)
#convert the categories from strings to names
y_train = labelEncoder.transform(trainTargetsList)

# train and evaluate the classifiers
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
print('Accuracy of K-NN classifier on training set: {:.2f}'.format(knn.score(X_train, y_train)))

from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(max_depth=7).fit(X_train, y_train)
print('Accuracy of Decision Tree classifier on training set: {:.2f}'.format(clf.score(X_train, y_train)))

from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)
print('Accuracy of GNB classifier on training set: {:.2f}'.format(gnb.score(X_train, y_train)))

from sklearn.svm import SVC
svm = SVC()
svm.fit(X_train, y_train)
print('Accuracy of SVM classifier on training set: {:.2f}'.format(svm.score(X_train, y_train)))

# ----------------------------------------------------------------------------------------
#now run the same things on the test data.
# DO NOT FORGET: you use the same visual words, created using training set.

#load the train images
testImages = load_images_from_folder(TestImagesFilePath, inputImageSize)  # take all images category by category for train set

#calculate points and descriptor values per image
testDataFeatures = detector_features(testImages)

# Takes the sift feature values that is seperated class by class for train data, we need this to calculate the histograms
testBoVWFeatureVals = testDataFeatures[1]

#create the test input / test output format
testHistogramsList, testTargetsList = mapFeatureValsToHistogram(testBoVWFeatureVals, visualWords, TrainedKmeansModel)
X_test = np.array(testHistogramsList)
labelEncoder.fit(trainTargetsList)

y_test = labelEncoder.transform(testTargetsList)

#classification tree
# predict outcomes for test data and calculate the test scores
y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)
#calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

#print the scores
print('')
print(' Printing performance scores using Sift for 60/40 train-test:')
print('')

print('Accuracy scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')

# knn predictions
#now check for both train and test data, how well the model learned the patterns
y_pred_train = knn.predict(X_train)
y_pred_test = knn.predict(X_test)
#calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

#print the scores
print('Accuracy scores of K-NN classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of K-NN classifie classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of K-NN classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of K-NN classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')


#naive Bayes
# now check for both train and test data, how well the model learned the patterns
y_pred_train = gnb.predict(X_train)
y_pred_test = gnb.predict(X_test)
# calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

# print the scores
print('Accuracy scores of GNB classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of GBN classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of GNB classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of GNB classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')


#support vector machines
# now check for both train and test data, how well the model learned the patterns
y_pred_train = svm.predict(X_train)
y_pred_test = svm.predict(X_test)
# calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

# print the scores
print('Accuracy scores of SVM classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of SVM classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of SVM classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of SVM classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')

"""# ORB for 60/40"""

print('Time to see the results using the ORB descriptor for the second part')
#calculate points and descriptor values per image
trainDataFeatures = detector_features_ORB(trainImages)
# Takes the descriptor list which is unordered one
TrainDescriptorList = trainDataFeatures[0]

#create the central points for the histograms using k means.
#here we use a rule of the thumb to create the expected number of cluster centers
numberOfClasses = trainImages.__len__() #retrieve num of classes from dictionary
possibleNumOfCentersToUse = 10 * numberOfClasses
visualWords, TrainedKmeansModel = kmeansVisualWordsCreation(possibleNumOfCentersToUse, TrainDescriptorList)
# Takes the sift feature values that is seperated class by class for train data, we need this to calculate the histograms
trainBoVWFeatureVals = trainDataFeatures[1]

#create the train input train output format
trainHistogramsList, trainTargetsList = mapFeatureValsToHistogram(trainBoVWFeatureVals, visualWords, TrainedKmeansModel)
#X_train = np.asarray(trainHistogramsList)
#X_train = np.concatenate(trainHistogramsList, axis=0)
X_train = np.stack(trainHistogramsList, axis= 0)

# Convert Categorical Data For Scikit-Learn
from sklearn import preprocessing

# Create a label (category) encoder object
labelEncoder = preprocessing.LabelEncoder()
labelEncoder.fit(trainTargetsList)
#convert the categories from strings to names
y_train = labelEncoder.transform(trainTargetsList)

# train and evaluate the classifiers
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
print('Accuracy of K-NN classifier on training set: {:.2f}'.format(knn.score(X_train, y_train)))


from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(max_depth=7).fit(X_train, y_train)
print('Accuracy of Decision Tree classifier on training set: {:.2f}'.format(clf.score(X_train, y_train)))


from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)
print('Accuracy of GNB classifier on training set: {:.2f}'.format(gnb.score(X_train, y_train)))


from sklearn.svm import SVC
svm = SVC()
svm.fit(X_train, y_train)
print('Accuracy of SVM classifier on training set: {:.2f}'.format(svm.score(X_train, y_train)))

#load the train images
testImages = load_images_from_folder(TestImagesFilePath, inputImageSize)  # take all images category by category for train set

#calculate points and descriptor values per image
testDataFeatures = detector_features_ORB(testImages)

# Takes the sift feature values that is seperated class by class for train data, we need this to calculate the histograms
testBoVWFeatureVals = testDataFeatures[1]

#create the test input / test output format
testHistogramsList, testTargetsList = mapFeatureValsToHistogram(testBoVWFeatureVals, visualWords, TrainedKmeansModel)
X_test = np.array(testHistogramsList)
labelEncoder.fit(trainTargetsList)

y_test = labelEncoder.transform(testTargetsList)


#classification tree
# predict outcomes for test data and calculate the test scores
y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)
#calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

#print the scores
print('')
print(' Printing performance scores using ORB for 60/40 train-test :')
print('')

print('Accuracy scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of Decision Tree classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')

# knn predictions
#now check for both train and test data, how well the model learned the patterns
y_pred_train = knn.predict(X_train)
y_pred_test = knn.predict(X_test)
#calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

#print the scores
print('Accuracy scores of K-NN classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of K-NN classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of K-NN classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of K-NN classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')


#naive Bayes
# now check for both train and test data, how well the model learned the patterns
y_pred_train = gnb.predict(X_train)
y_pred_test = gnb.predict(X_test)
# calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

# print the scores
print('Accuracy scores of GNB classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of GBN classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of GNB classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of GNB classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')


#support vector machines
# now check for both train and test data, how well the model learned the patterns
y_pred_train = svm.predict(X_train)
y_pred_test = svm.predict(X_test)
# calculate the scores
acc_train = accuracy_score(y_train, y_pred_train)
acc_test = accuracy_score(y_test, y_pred_test)
pre_train = precision_score(y_train, y_pred_train, average='macro')
pre_test = precision_score(y_test, y_pred_test, average='macro')
rec_train = recall_score(y_train, y_pred_train, average='macro')
rec_test = recall_score(y_test, y_pred_test, average='macro')
f1_train = f1_score(y_train, y_pred_train, average='macro')
f1_test = f1_score(y_test, y_pred_test, average='macro')

# print the scores
print('Accuracy scores of SVM classifier are:',
      'train: {:.6f}'.format(acc_train), 'and test: {:.6f}.'.format(acc_test))
print('Precision scores of SVM classifier are:',
      'train: {:.6f}'.format(pre_train), 'and test: {:.6f}.'.format(pre_test))
print('Recall scores of SVM classifier are:',
      'train: {:.6f}'.format(rec_train), 'and test: {:.6f}.'.format(rec_test))
print('F1 scores of SVM classifier are:',
      'train: {:.6f}'.format(f1_train), 'and test: {:.6f}.'.format(f1_test))
print('')