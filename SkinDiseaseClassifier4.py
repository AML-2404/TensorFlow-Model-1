#More than 2 classes to predict

#MLOps

import matplotlib.pyplot as plt
import seaborn as sns

import keras
from keras.callbacks import EarlyStopping
from keras.models import Sequential
from keras.layers import Dense, Conv2D , MaxPool2D , Flatten , Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam

from sklearn.metrics import classification_report,confusion_matrix

import tensorflow as tf

import cv2
import os

import numpy as np


labels = ['Actinic Keratosis', 'Eczema','Ringworm']
img_size = 224

def get_data(data_dir):
    data = []
    for label in labels:
        path = os.path.join(data_dir, label)
        class_num = labels.index(label)
        for img in os.listdir(path):
            try:
                # img_arr = cv2.imread(os.path.join(path, img))[...,::-1] #convert BGR to RGB format
                image = cv2.imread(os.path.join(path, img))

                #Converting image to grayScale
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                resized_arr = cv2.resize(gray, (img_size, img_size)) # Reshaping images to preferred size

                data.append([resized_arr, class_num])
            except Exception as e:
                print(e)
    return np.array(data)

train = get_data('/Users/thejakamahaulpatha/PycharmProjects/HealthImageClassifier/dataset3/train')
val = get_data('/Users/thejakamahaulpatha/PycharmProjects/HealthImageClassifier/dataset3/test')

# print(train.shape)
# print(val.shape)

x_train = []
y_train = []
x_val = []
y_val = []

for feature, label in train:
  x_train.append(feature)
  y_train.append(label)

for feature, label in val:
  x_val.append(feature)
  y_val.append(label)

# Normalize the data
x_train = np.array(x_train) / 255
x_val = np.array(x_val) / 255

x_train.reshape(-1, img_size, img_size, 1)
y_train = np.array(y_train)

x_val.reshape(-1, img_size, img_size, 1)
y_val = np.array(y_val)

#Data augmentation on the train data:

datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range = 40,  # randomly rotate images in the range (degrees, 0 to 180)
        zoom_range = 0.4, # Randomly zoom image
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip = True,  # randomly flip images
        vertical_flip=True)  # randomly flip images



# print(x_train[0])
datagen.fit(x_train.reshape(x_train.shape[0], 224, 224,1)) # x_train.shape[0] = 3684

# Define the Model
model = Sequential()
model.add(Conv2D(32,3,padding="same", activation="relu", input_shape=(224,224,1)))
model.add(MaxPool2D())
# model.add(Dropout(0.2))

model.add(Conv2D(32, 3, padding="same", activation="relu"))
model.add(MaxPool2D())

# model.add(Dropout(0.2)) #Added since Validation loss is increasing
model.add(Conv2D(64, 3, padding="same", activation="relu"))
model.add(MaxPool2D())

model.add(Dropout(0.4))

model.add(Flatten())
model.add(Dense(128,activation="relu"))
model.add(Dense(3, activation="softmax"))

model.summary()

opt = Adam(lr=0.001)
model.compile(optimizer = opt , loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False) , metrics = ['accuracy'])
# model.compile(optimizer = opt , loss = tf.keras.losses.KLDivergence() , metrics = ['accuracy'])

#Adding Early Stopping
# es = EarlyStopping(monitor='val_loss',verbose=1,patience=20)

history = model.fit(x_train,y_train,epochs = 20 , validation_data = (x_val, y_val)) # ,callbacks=[es]
# history = model.fit(x_train,y_train,epochs = 20 , validation_split=0.1) # ,callbacks=[es]

def plotFunc():

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(20)
    sns.set_style('darkgrid')
    plt.figure(figsize=(15, 15))
    plt.subplot(2, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(2, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()

plotFunc()


def plotFunc2():
    # evaluate the model
    _, train_acc = model.evaluate(x_train, y_train, verbose=0)
    _, test_acc = model.evaluate(x_val, y_val, verbose=0)
    print('Train Accuracy: %.3f, Validation Accuracy: %.3f' % (train_acc, test_acc))
    # plot training history
    sns.set_style('darkgrid')
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.legend()
    plt.show()

# plotFunc2()


# predictions = model.predict_classes(x_val)
# model.predict
# predictions = predictions.reshape(1,-1)[0]
# print(classification_report(y_val, predictions, target_names = ['Rugby (Class 0)','Soccer (Class 1)']))
#
