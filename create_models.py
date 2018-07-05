import keras
from keras.models import Sequential, Input, Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv1D, MaxPooling1D
from keras.layers.normalization import BatchNormalization
from keras.models import load_model

import numpy as np

W = Sequential()
W.add(Conv1D(64, kernel_size=16,activation='relu',input_shape=(64,1),padding='same'))
W.add(MaxPooling1D(pool_size=4,padding='same'))
W.add(Conv1D(128, kernel_size=16,activation='relu',input_shape=(64,1),padding='same'))
W.add(MaxPooling1D(pool_size=4,padding='same'))
W.add(Flatten())
W.add(Dense(512, activation='relu'))  
W.add(Dense(256, activation='relu'))	               
W.add(Dense(1, activation='sigmoid'))
#Compile model
W.compile(loss=keras.losses.binary_crossentropy, optimizer=keras.optimizers.Adam(), metrics=["binary_accuracy"])
W.summary()


state = np.array([[ 0.,  4.,  0.,  6.,  0.,  3.,  0.,  0.],
       [ 0.,  3.,  0.,  0.,  1.,  0.,  4.,  0.],
       [ 1.,  0.,  0.,  0.,  0.,  0.,  1.,  0.],
       [ 0.,  0.,  1.,  1.,  0.,  1.,  0.,  0.],
       [ 0., -1.,  1., -1.,  0., -1.,  2., -1.],
       [ 0.,  0.,  0.,  0.,  0.,  2., -6., -4.],
       [ 0.,  0.,  0.,  0.,  0.,  5., -1.,  0.],
       [ 0.,  0.,  0.,  0.,  0., -3.,  0.,  0.]])
state = state.ravel()
state = (state + 6.0)/12.0
state = np.reshape(state,(-1,64,1))

state2 = np.array([[ 0.,  4.,  0.,  6.,  0.,  3.,  0.,  0.],
       [ 0.,  3.,  0.,  0.,  1.,  0.,  4.,  0.],
       [ 1.,  0.,  0.,  0.,  0.,  0.,  1.,  0.],
       [ 0.,  0.,  1.,  1.,  0.,  1.,  0.,  0.],
       [ 0., -1.,  1., -1.,  0., -1.,  2., -1.],
       [ 0.,  0.,  0.,  0.,  0.,  2., -6., -4.],
       [ 0.,  1.,  0.,  0.,  0.,  5., -1.,  0.],
       [ 0.,  0.,  0.,  0.,  0., -3.,  0.,  0.]])
state2 = state2.ravel()
state2 = (state2 + 6.0)/12.0
state2 = np.reshape(state2,(-1,64,1))

states = np.vstack((state, state2))

print W.predict(states)
W.save('Models\\walt.h5')


B = Sequential()
B.add(Conv1D(64, kernel_size=16,activation='relu',input_shape=(64,1),padding='same'))
B.add(MaxPooling1D(pool_size=4,padding='same'))
B.add(Conv1D(128, kernel_size=16,activation='relu',input_shape=(64,1),padding='same'))
B.add(MaxPooling1D(pool_size=4,padding='same'))
B.add(Flatten())
B.add(Dense(512, activation='relu'))  
B.add(Dense(256, activation='relu'))	               
B.add(Dense(1, activation='sigmoid'))
#Compile model
B.compile(loss=keras.losses.binary_crossentropy, optimizer=keras.optimizers.Adam(), metrics=["binary_accuracy"])
B.summary()

print W.predict(state2)

B.save('Models\\bob.h5')
