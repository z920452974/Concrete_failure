# -*- coding: utf-8 -*-
"""concrete_data_failure.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zGsRueC9y1YU9QVbv1jBu3OOYYgm8MKq

The following cells download and unzip the data (concrete data)
"""

!wget https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DL0321EN/data/concrete_data_week4.zip

!unzip concrete_data_week4.zip

"""Using the VGG16 pre-trained model"""

# imports
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, load_model
from keras.layers import Dense, AveragePooling2D, Flatten

# number of classes (0 and 1) and batch size
n_classes = 2
batch_size = 100

# data generator
data_generator = ImageDataGenerator(preprocessing_function = preprocess_input)

# train data
train_generator = data_generator.flow_from_directory('concrete_data_week4/train',
                                              target_size = (224, 224), batch_size = batch_size)

#validation data
validation_generator = data_generator.flow_from_directory('concrete_data_week4/valid',
                                                    target_size = (224, 224), batch_size = batch_size)

# sequential model
model = Sequential()
model.add(VGG16(weights = 'imagenet', include_top = False, pooling = 'avg'))
model.layers[0].trainable = False
model.add(Dense(128, activation = 'relu'))
model.add(Dense(n_classes, activation = 'softmax'))

# summary of the model
model.summary()

# model compile
model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

n_epochs = 2

# model fit
model.fit(train_generator, epochs = n_epochs, validation_data = validation_generator)

# save the model
model.save('classifier_vgg16_model.h5')

"""Use the following cells to evaluate your models."""

# loading the vgg16 model
vgg16_model = load_model('classifier_vgg16_model.h5')

# image generator
data_generator = ImageDataGenerator()

# and the test set generator
test_generator = data_generator.flow_from_directory("concrete_data_week4/test",
                                                    target_size = (224,224), shuffle = False)

# performance of VGG16 model
vgg16 = vgg16_model.evaluate(test_generator)
vgg16

# The VGG16 has 0.0320 loss and 0.9940 (99.40%) accuracy

"""Use the following cells to make your predictions."""

# prediction function of the models
vgg16_predict = vgg16_model.predict(test_generator)

# vgg16 predictions
vgg16_predict[0:5]

# The VGG16 predict, in the first five images: (chosing the maximum value)
# POSITIVE
# POSITIVE
# POSITIVE
# POSITIVE
# POSITIVE