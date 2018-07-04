import keras
from keras.models import Sequential, Input, Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv1D, MaxPooling1D
from keras.layers.normalization import BatchNormalization
from keras.models import load_model

import numpy as np

W = Sequential()
W.add(Conv1D(64, kernel_size=8,activation='linear',input_shape=(64,1),padding='same'))
W.add(MaxPooling1D(pool_size=4,padding='same'))
W.add(Conv1D(128, kernel_size=8,activation='linear',input_shape=(64,1),padding='same'))
W.add(MaxPooling1D(pool_size=4,padding='same'))
W.add(Flatten())
W.add(Dense(256, activation='linear'))  
W.add(Dense(256, activation='linear'))	               
W.add(Dense(1, activation='tanh'))
#Compile model
W.compile(loss=keras.losses.mean_squared_error, optimizer=keras.optimizers.Adam(),metrics=['accuracy'])
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
state2 = np.reshape(state2,(-1,64,1))

print W.predict(state)
W.save('Models\\walt.h5')


B = Sequential()
B.add(Conv1D(64, kernel_size=8,activation='linear',input_shape=(64,1),padding='same'))
B.add(MaxPooling1D(pool_size=4,padding='same'))
B.add(Conv1D(128, kernel_size=8,activation='linear',input_shape=(64,1),padding='same'))
B.add(MaxPooling1D(pool_size=4,padding='same'))
B.add(Flatten())
B.add(Dense(256, activation='linear'))  
B.add(Dense(256, activation='linear'))	               
B.add(Dense(1, activation='tanh'))
#Compile model
B.compile(loss=keras.losses.mean_squared_error, optimizer=keras.optimizers.Adam(),metrics=['accuracy'])
B.summary()

print W.predict(state2)

B.save('Models\\bob.h5')
