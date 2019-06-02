import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense, BatchNormalization
from keras import applications
from datetime import datetime as dt
from keras import regularizers as reg
from keras.optimizers import RMSprop
from keras.utils import to_categorical
import warnings
warnings.filterwarnings("ignore")
from keras.callbacks import ModelCheckpoint

def graph(x,y,xlabel,ylabel):
    plt.plot(x,y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def neural_network(input_shape,layer_activation,dense_unit,dense_activation,optim,loss_comp):	

    
	classifier = Sequential()
	classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = layer_activation))
	classifier.add(MaxPooling2D(pool_size = (2, 2)))


	classifier.add(Conv2D(32, (3, 3), activation = layer_activation))
	classifier.add(MaxPooling2D(pool_size = (2, 2)))

	classifier.add(Conv2D(32, (3, 3), activation = layer_activation))
	classifier.add(MaxPooling2D(pool_size = (2, 2)))

	classifier.add(Flatten())
	# Step 4 - Full connection
	classifier.add(Dense(units = 128, activation = layer_activation))
	classifier.add(Dense(units = dense_unit, activation = dense_activation))
	# Compiling the CNN
	classifier.compile(optimizer = optim, loss = loss_comp, metrics = ['accuracy'])
	classifier.summary()

def data_zone_csv(x):
	'''
	CSV = data_zone_csv
	'''
	self=pd.read_csv(x)
	return self

def vgg16(input_shap,dense_unit,dense_activation,optim,loss_comp):
    model = Sequential()
    model.add(ZeroPadding2D((1, 1), input_shape=input_shap))
    model.add(Convolution2D(64, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(64, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(128, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(128, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(Flatten())
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(dense_unit, activation=dense_activation))
    model.summary()
    model.compile(optimizer = optim, loss = loss_comp, metrics = ['accuracy'])
    
    
def Transfer_learning(train_data,val_data,epochs,batch_size):
    '''
    Keywords :
    train_data = training dataset
    val_data = Validation dataset
    epochs = number of epochs
    batch_size = batch size
    '''
    global_start=dt.now()

    #Dimensions of our flicker images is 256 X 256
    img_width, img_height = 256, 256

    #Declaration of parameters needed for training and validation
    epochs = epochs
    batch_size = batch_size

    #Get the bottleneck features by  Weights.T * Xi
    def save_bottlebeck_features():
        datagen = ImageDataGenerator(rescale=1./255)

        #Load the pre trained VGG16 model from Keras, we will initialize only the convolution layers and ignore the top layers.
        model = applications.VGG16(include_top=False, weights='imagenet')

        generator_tr = datagen.flow_from_directory(train_data,
                                                target_size=(img_width, img_height),
                                                batch_size=batch_size,
                                                class_mode=None, #class_mode=None means the generator won't load the class labels.
                                                shuffle=False) #We won't shuffle the data, because we want the class labels to stay in order.
        nb_train_samples = len(generator_tr.filenames) #3600. 1200 training samples for each class
        bottleneck_features_train = model.predict_generator(generator_tr, nb_train_samples // batch_size)
        np.save('weights/bottleneck_features_train.npy',bottleneck_features_train) #bottleneck_features_train is a numpy array

        generator_ts = datagen.flow_from_directory(val_data,
                                                target_size=(img_width, img_height),
                                                batch_size=batch_size,
                                                class_mode=None,
                                                shuffle=False)
        nb_validation_samples = len(generator_ts.filenames) #1200. 400 training samples for each class
        bottleneck_features_validation = model.predict_generator(generator_ts, nb_validation_samples // batch_size)
        np.save('weights/bottleneck_features_validation.npy',bottleneck_features_validation)
        print("Got the bottleneck features in time: ",dt.now()-global_start)

        num_classes = len(generator_tr.class_indices)

        return nb_train_samples,nb_validation_samples,num_classes,generator_tr,generator_ts

    nb_train_samples,nb_validation_samples,num_classes,generator_tr,generator_ts=save_bottlebeck_features()
    
    def train_top_model():
        global_start=dt.now()

        train_data = np.load('weights/bottleneck_features_train.npy')
        validation_data = np.load('weights/bottleneck_features_validation.npy')

        train_labels=generator_tr.classes  
        validation_labels=generator_ts.classes


        model = Sequential()
        model.add(Flatten(input_shape=train_data.shape[1:])) #Ignore the first index. It contains ID

        model.add(Dense(256, activation='relu',kernel_initializer='he_normal',kernel_regularizer=reg.l1_l2(l1=0.001, l2=0.001))) #Best weight initializer for relu is he_normal
        model.add(BatchNormalization()) #Add a BatchNormalization layer to control internel covariance shift
        model.add(Dropout(rate=0.5)) #Using droput for regularization

        model.add(Dense(256, activation='relu',kernel_initializer='he_normal',kernel_regularizer=reg.l1_l2(l1=0.001, l2=0.001)))
        model.add(BatchNormalization()) #Add a BatchNormalization layer to control internel covariance shift
        model.add(Dropout(rate=0.5))

        model.add(Dense(1, activation='sigmoid',kernel_initializer='glorot_uniform')) #Because we have 3 classes. Remember, softmax is to multi-class, what sigmoid (log reg) is to binary

        optim=RMSprop(lr=0.0001, epsilon=1e-8, decay=1e-6)  
        model.compile(loss='binary_crossentropy',optimizer=optim,metrics=['accuracy'])
        model.summary()

        #Save the weights for the best epoch accuracy
        checkpointer = ModelCheckpoint(filepath="weights/bottleneck_features_model_weights.hdf5", monitor = 'val_acc',verbose=1, save_best_only=True)

        model.fit(x=train_data,
                  y=train_labels,
                  epochs=epochs,
                  validation_data=(validation_data, validation_labels),
                  callbacks=[checkpointer])    

        #Refit our model with the best weights saved before
        model.load_weights('weights/bottleneck_features_model_weights.hdf5')
        model.save('weights/bottleneck_feature_model.h5')
        print("The top layer trained in time: ",dt.now()-global_start)

        return model

    model=train_top_model()
