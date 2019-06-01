import random
from collections import deque

import keras
import numpy as np
from keras.layers import Dense, Input, Dropout
from keras.optimizers import Adam

from yaaf.models.Model import Model


class QNetwork(Model):
    """
    A class representing a QNetwork with replay memory
    """

    def __init__(self, features, actions, name="q_network",
                 layers=((64, "relu"),), learning_rate=0.001, loss="mse", dropout_rate=0.0,
                 discount_factor=0.99, replay_memory_size=1000000, replay_memory_batch=32):

        super().__init__(name)

        self._features = features
        self._actions = actions

        self._layers = layers

        self._discount_factor = discount_factor

        input_layer = Input((self._features,), name=f"{self.name}_input_layer")
        last_layer = Dropout(rate=dropout_rate)(input_layer) if dropout_rate != 0.0 else input_layer

        for i, (units, activation) in enumerate(layers):
            last_layer = Dense(units, activation=activation, name=f"{self.name}_hidden_layer_{i}")(last_layer)
            last_layer = Dropout(rate=dropout_rate)(last_layer) if dropout_rate != 0.0 else last_layer

        q_values_layer = Dense(actions, activation='linear', name=f"{self.name}_output_layer")(last_layer)

        self._model = keras.Model(input_layer, q_values_layer, name=self.name)
        self._model.compile(optimizer=Adam(learning_rate), loss=loss)

        self._replay_memory = deque(maxlen=replay_memory_size)
        self._replay_memory_batch = replay_memory_batch

    def predict(self, state):
        q_values = self._model.predict(state.reshape(1, -1))[0]
        return q_values

    def train(self, timestep):
        self._replay_memory.append(timestep)
        self._replay()

    def _replay(self):

        not_enough_data = len(self._replay_memory) < self._replay_memory_batch

        if not_enough_data:
            return
        else:
            replay_batch = random.sample(self._replay_memory, self._replay_memory_batch)
            X, Y = self._preprocess_batch(replay_batch)
            self._train(X, Y)

    def _preprocess_batch(self, batch):

        m = len(batch)

        F = self._features
        A = self._actions

        X = np.zeros((m, F))
        Y = np.zeros((m, A))

        for i, timestep in enumerate(batch):

            q_update = timestep.reward

            if not timestep.is_terminal:
                q_values_next_state = self._model.predict(timestep.next_state.reshape(1, -1))[0]
                q_update = (timestep.reward + self._discount_factor * np.amax(q_values_next_state))

            q_values = self._model.predict(timestep.state.reshape(1, -1))[0]
            q_values[timestep.action] = q_update

            X[i] = timestep.state
            Y[i] = q_values

        return X, Y

    def _train(self, X, Y):
        self._model.fit(X, Y, verbose=0)

    def _save(self, directory):
        self._model.save_weights(f"{directory}/{self.name}.h5")

    def load(self, directory):
        self._model.load_weights(f"{directory}/{self.name}.h5")
