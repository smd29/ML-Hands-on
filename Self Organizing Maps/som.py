# -*- coding: utf-8 -*-
"""SOM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ikGAD-FFCOsp2ek12Cxk74em6ee6-6DK

#Self Organizing Map

##Install MiniSom Package

### Importing the libraries
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""## Importing the dataset"""

dataset = pd.read_csv('Credit_Card_Applications.csv')
x = dataset.iloc[:,:-1].values
y = dataset.iloc[:,-1].values

"""## Feature Scaling

"""

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range=(0,1))
x = sc.fit_transform(x)

"""##Training the SOM

"""

from minisom import MiniSom
som = MiniSom(x=10, y=10, input_len=15)
#initialize weights
som.random_weights_init(x)
som.train_random(x, num_iteration=100)

"""##Visualizing the results

"""

from pylab import bone, pcolor, colorbar, plot, show
bone()
pcolor(som.distance_map().T)
colorbar()
markers = ['o', 's']
colors = ['r', 'g']
for row, vector in enumerate(x):
  w = som.winner(vector)
  plot(w[0]+0.5, w[1]+0.5, markers[y[row]], markeredgecolor = colors[y[row]], markerfacecolor = 'None', markersize = 10, markeredgewidth = 2)
show()

"""## Finding the frauds

"""

mappings = som.win_map(x)

frauds = np.concatenate((mappings[(8,1)], mappings[(6,9)]), axis = 0)
frauds = sc.inverse_transform(frauds)

"""##Printing the Fraunch Clients"""

print("Probable Fraud Customer IDs are: ")
for id in frauds:
  print(id)

"""##Printing the Fraunch Clients

"""

print('Fraud Customer IDs')
for i in frauds[:, 0]:
  print(int(i))

"""#Part 2 - Going from Unsupervised to Supervised Deep Learning

##Create Matrix of Features
"""

customers = dataset.iloc[:, 1:].values

"""## Create Dependent Variable"""

is_fraud = np.zeros(len(dataset))
for idx in range(len(dataset)):
  cust_id = dataset.iloc[idx, 0]
  if cust_id in frauds:
    is_fraud[idx] = 1

"""## Part 3 ANN

### Feature Scaling
"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
sc.fit_transform(customers)

"""## Building the ANN"""

import tensorflow as tf

"""## Initializing the ANN"""

ann = tf.keras.models.Sequential()

"""### Add input Layer and first hidden layer"""

ann.add(tf.keras.layers.Dense(units=2, activation = 'relu'))

"""## Add output Layers"""

ann.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

"""## Compiling the ANN"""

ann.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

"""##Training the ANN on training set"""

ann.fit(customers, is_fraud, batch_size = 1, epochs = 10)

"""## Prediction"""

y_pred = ann.predict(customers)
y_pred = np.concatenate((dataset.iloc[:, 0:1].values, y_pred), axis = 1)
y_pred = y_pred[y_pred[:, 1].argsort()]

print(y_pred)

