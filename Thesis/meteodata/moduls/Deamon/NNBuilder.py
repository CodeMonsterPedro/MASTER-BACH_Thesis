import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model


class NNBuilder:

    def buildRnnNet():
        #'mean_absolute_error' +- --
        # mean_absolute_percentage_error -- --
        # mean_squared_logarithmic_error  --
        # mean_squared_error +- --
        loss = 'mean_squared_error'
        method = keras.Sequential()
        method.add(keras.layers.Embedding(input_dim=10, output_dim=5))
        method.add(keras.layers.LSTM(units=25, return_sequences=False))
        method.add(keras.layers.Dense(5, activation='softmax'))
        method.compile(optimizer='adam', loss=loss, metrics='accuracy')
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

    def buildRnnNet_ForSummary(output_dim):
        method = keras.Sequential()
        method.add(keras.layers.Embedding(input_dim=10, output_dim=10))
        method.add(keras.layers.LSTM(units=100, return_sequences=False))
        method.add(keras.layers.Dense(output_dim, activation='softmax'))
        method.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics='accuracy')
        method.summary()
        return method

    def buildPerceptronNet_ForForecast():
        method = keras.Sequential()
        method.add(keras.layers.Dense(10, activation='relu', input_shape=(10,)))
        method.add(keras.layers.Dense(500, activation='relu'))
        method.add(keras.layers.Dense(50, activation='relu'))
        method.add(keras.layers.Dense(5, activation='softmax'))
        method.compile(optimizer='adam', loss='mean_squared_error', metrics='accuracy')
        method.summary()
        return method

    def buildAutoencoder_ForSummary(output_dim):
        obj = AutoencoderModel(10, 100, output_dim)
        obj.compile(optimizer='adam', loss='mean_squared_error', metrics='accuracy')
        return obj

    def buildAutoencoder_ForForecast():
        return AutoencoderModel(10, 100, 5)


class AutoencoderModel(Model):

    def __init__(self, values_size, latent_dim, output_dim):
        super(AutoencoderModel, self).__init__()
        self.latent_dim = latent_dim
        self.encoder = tf.keras.Sequential()
        self.encoder.add(keras.layers.InputLayer(input_shape=(values_size, )))
        self.encoder.add(keras.layers.Dense(latent_dim, activation="relu"))
        self.encoder.add(keras.layers.Dense(int(latent_dim / 2), activation="relu"))
        self.decoder = tf.keras.Sequential()
        self.decoder.add(keras.layers.InputLayer(input_shape=(int(latent_dim / 2), )))
        self.decoder.add(keras.layers.Dense(int(latent_dim / 2), activation="relu"))
        self.decoder.add(keras.layers.Dense(output_dim, activation="relu"))

    def call(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
