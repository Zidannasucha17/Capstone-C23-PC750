# -*- coding: utf-8 -*-
"""FER2013_CNN_From_Scratch.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tjdvA60GHc2ARg3CpYX8nUnKFqyBwvo7
"""

! pip install -q kaggle

from google.colab import files
files.upload()

! mkdir ~/.kaggle

! cp '/content/kaggle.json' ~/.kaggle/

! chmod 600 /content/kaggle.json

! kaggle datasets download -d msambare/fer2013

!mkdir Dataset
!cp /content/fer2013.zip /content/Dataset

!unzip -q /content/Dataset/fer2013.zip -d /content/Dataset

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator

img_size = (48, 48)
BATCH_SIZE = 32
train_dir = '/content/Dataset/train'
val_dir = '/content/Dataset/test'

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   fill_mode='nearest')

validation_datagen = ImageDataGenerator(rescale = 1./255)

train_data = train_datagen.flow_from_directory(train_dir,
                                               target_size=img_size,
                                               class_mode='categorical',
                                               batch_size=BATCH_SIZE,
                                               color_mode='grayscale',
                                               subset='training') #setting_training_data

validation_data = validation_datagen.flow_from_directory(val_dir,
                                                         target_size=img_size,
                                                         class_mode='categorical',
                                                         batch_size=BATCH_SIZE,
                                                         color_mode='grayscale') #setting_validation_data

from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Dropout, Flatten, Dense, MaxPooling2D
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape = (48, 48, 1)),
    tf.keras.layers.MaxPooling2D(pool_size = (2,2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size = (2,2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size = (2,2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.MaxPooling2D(pool_size = (2,2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(7, activation='softmax')
])

model.summary()
model.compile(
    loss = 'categorical_crossentropy',
    optimizer = tf.keras.optimizers.Adam(),
    metrics = ["accuracy",
               tf.keras.metrics.Precision(),
               tf.keras.metrics.Recall()]
    )

history = model.fit(
    train_data,
    steps_per_epoch = train_data.samples//BATCH_SIZE,
    epochs = 400,
    validation_data = validation_data,
    validation_steps = validation_data.samples//BATCH_SIZE
    )

import matplotlib.pyplot as plt
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
plt.ylim([min(plt.ylim()),1])
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.ylabel('Cross Entropy')
plt.ylim([0,1.0])
plt.title('Training and Validation Loss')
plt.xlabel('epoch')
plt.show()

export_dir = '/tmp/saved_model'
tf.saved_model.save(model, export_dir)