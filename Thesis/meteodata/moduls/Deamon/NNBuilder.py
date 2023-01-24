import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model


class NNBuilder:

    def buildRnnNetTest(values, labels):
        method = keras.Sequential()
        method.add(keras.layers.LSTM(100, input_shape=(len(values[0]), 1), activation='relu', return_sequences=True))
        method.add(keras.layers.Dropout(0.2))
        method.add(keras.layers.LSTM(100, activation='relu'))
        method.add(keras.layers.Dropout(0.1))
        method.add(keras.layers.Dense(25, activation='relu'))
        method.add(keras.layers.Dropout(0.2))
        method.add(keras.layers.Dense(5, activation='softmax'))
        method.compile(optimizer='adam', loss='mean_squared_error', metrics='accuracy')
        method.summary()
        return method

    def buildRnnNet(values, labels):
        #'mean_absolute_error' +- --
        # mean_absolute_percentage_error -- --
        # mean_squared_logarithmic_error  --
        # mean_squared_error +- --
        loss = 'mean_squared_error'
        method = keras.Sequential()
        method.add(keras.layers.Embedding(input_dim=10, output_dim=5))
        method.add(keras.layers.LSTM(units=25, return_sequences=False))
        method.add(keras.layers.Dense(5, activation='relu'))
        method.compile(optimizer='adam', loss=loss, metrics='accuracy')
        method.summary()
        return method

    def buildRnnNet_ForSummary(output_dim):
        method = keras.Sequential()
        method.add(keras.layers.Embedding(input_dim=10, output_dim=10))
        method.add(keras.layers.LSTM(units=100, return_sequences=False))
        method.add(keras.layers.Dense(output_dim, activation='softmax'))
        method.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics='accuracy')
        method.summary()
        return method

    def buildPerceptronNet(output_dim):
        # categorical_crossentropy
        # sparse_categorical_crossentropy
        # categorical_hinge
        method = keras.Sequential()
        method.add(keras.layers.Dense(10, activation='relu', input_shape=(10,)))
        method.add(keras.layers.Dense(1000, activation='relu'))
        method.add(keras.layers.Dense(100, activation='relu'))
        method.add(keras.layers.Dense(output_dim, activation='softmax'))
        method.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics='accuracy')
        method.summary()
        return method

    def buildPerceptronNet_ForForecast():
        # mean_absolute_error 
        # mean_squared_logarithmic_error ++- +100 *100 
        # mean_absolute_percentage_error +- !!+700!!
        method = keras.Sequential()
        method.add(keras.layers.Dense(10, activation='relu', input_shape=(10,)))
        method.add(keras.layers.Dense(500, activation='relu'))
        method.add(keras.layers.Dense(50, activation='relu'))
        method.add(keras.layers.Dense(5, activation='relu'))
        method.compile(optimizer='adam', loss='mean_absolute_percentage_error', metrics='accuracy')
        method.summary()
        return method

    def buildAutoencoder_ForSummary():
        obj = keras.Sequential()
        obj.add(keras.layers.Dense(10, activation='relu', input_shape=(10,)))
        obj.add(keras.layers.Dense(1000, activation='relu'))
        obj.add(keras.layers.Dense(100, activation='relu'))
        obj.add(keras.layers.Dense(100, activation='relu'))
        obj.add(keras.layers.Dense(1000, activation='relu'))
        obj.add(keras.layers.Dense(20, activation='softmax'))
        obj.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics='accuracy')
        obj.summary()
        return obj

    def buildAutoencoder_ForForecast():
        obj = keras.Sequential()
        obj.add(keras.layers.Dense(10, activation='relu', input_shape=(10,)))
        obj.add(keras.layers.Dense(1000, activation='relu'))
        obj.add(keras.layers.Dense(100, activation='relu'))
        obj.add(keras.layers.Dense(100, activation='relu'))
        obj.add(keras.layers.Dense(1000, activation='relu'))
        obj.add(keras.layers.Dense(5, activation='relu'))
        obj.compile(optimizer='adam', loss='mean_absolute_percentage_error', metrics='accuracy')
        obj.summary()
        return obj
