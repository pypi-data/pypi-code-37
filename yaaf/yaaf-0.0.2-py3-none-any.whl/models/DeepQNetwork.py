import random
from collections import deque
from queue import Queue

import keras
import numpy as np
import scipy.misc as misc
from keras import Input
from keras.layers import Dropout, Dense, Flatten, Conv2D
from keras.optimizers import Adam

from yaaf.models.Model import Model
from yaaf.runners.Runner import Timestep


class DeepQNetwork(Model):

    def __init__(self, width, height, stacked_frames, actions,
                 name="deep_q_network",
                 convolutional_layers=(
                         (16, 8, 4, "relu"),
                         (32, 4, 2, "relu")
                 ),
                 fully_connected_layers=(
                         (256, "relu"),
                 ),
                 learning_rate=0.001, loss="mse", dropout_rate=0.0,
                 discount_factor=0.99, replay_memory_size=1000000, replay_memory_batch=32):

        super(DeepQNetwork, self).__init__(name)

        self._width = width
        self._height = height
        self._stacked_frames = stacked_frames

        self._actions = actions
        self._layers = convolutional_layers + fully_connected_layers
        self._discount_factor = discount_factor

        input_shape = (height, width, stacked_frames)
        input_layer = Input(input_shape, name=f"{self.name}_input_layer")
        last_layer = Dropout(rate=dropout_rate)(input_layer) if dropout_rate != 0.0 else input_layer

        for i, (kernel_size, filters, stride, activation) in enumerate(convolutional_layers):
            last_layer = Conv2D(filters=filters, kernel_size=kernel_size, strides=stride, activation=activation,
                                name=f"{self.name}_convolutional_layer_{i}")(last_layer)
            last_layer = Dropout(rate=dropout_rate)(last_layer) if dropout_rate != 0.0 else last_layer

        flatten_layer = Flatten(name=f"{self.name}_flatten_layer")(last_layer)
        last_layer = flatten_layer

        for i, (units, activation) in enumerate(fully_connected_layers):
            last_layer = Dense(units, activation=activation, name=f"{self.name}_hidden_layer_{i}")(last_layer)
            last_layer = Dropout(rate=dropout_rate)(last_layer) if dropout_rate != 0.0 else last_layer

        q_values_layer = Dense(actions, activation='linear', name=f"{self.name}_output_layer")(last_layer)

        self._model = keras.Model(input_layer, q_values_layer, name=self.name)
        self._model.compile(optimizer=Adam(learning_rate), loss=loss)

        self._replay_memory = deque(maxlen=replay_memory_size)
        self._replay_memory_batch = replay_memory_batch

        self._lookback_memory = Queue(maxsize=stacked_frames)

    def train(self, timestep):

        frate_t_next = self._preprocess_state(timestep.next_state)

        lookback_state_t = self._lookback_state()
        lookback_state_t_next = self._push_frame_to_memory(frate_t_next)

        is_terminal = timestep.is_terminal

        if is_terminal:
            self._lookback_memory.queue.clear()

        timestep = Timestep(lookback_state_t, timestep.action, timestep.reward, lookback_state_t_next, is_terminal,
                            timestep.info)
        self._replay_memory.append(timestep)
        self._replay()

    def predict(self, state):
        frame_t = self._preprocess_state(state)
        lookback_state_t = self._push_frame_to_memory(frame_t)
        q_values = self._predict(lookback_state_t)
        return q_values

    def _save(self, directory):
        self._model.save_weights(f"{directory}/model.h5")

    def load(self, directory):
        self._model.load_weights(f"{directory}/model.h5")

    #############
    # Auxiliary #
    #############

    def _predict(self, lookback_state):
        q_values = self._model.predict(lookback_state)[0]
        return q_values

    def _lookback_state(self):
        lookback_state_t = np.array(self._lookback_memory.queue)
        return lookback_state_t.reshape((1, self._height, self._width, self._stacked_frames))

    def _push_frame_to_memory(self, frame_t):

        # Already had full depth, remove the oldest
        if self._lookback_memory.full():
            self._lookback_memory.get()
            self._lookback_memory.put(frame_t)

        if len(self._lookback_memory.queue) == 0:
            while not self._lookback_memory.full():
                self._lookback_memory.put(frame_t)

        lookback_state_t = self._lookback_state()

        return lookback_state_t

    def _preprocess_batch(self, batch):

        m = len(batch)

        W = self._width
        H = self._height
        S = self._stacked_frames

        A = self._actions

        X = np.zeros((m, H, W, S))
        Y = np.zeros((m, A))

        for i, timestep in enumerate(batch):

            q_update = timestep.reward

            if not timestep.is_terminal:
                q_values_next_state = self._predict(timestep.next_state)
                q_update = (timestep.reward + self._discount_factor * np.amax(q_values_next_state))

            q_values = self._predict(timestep.state)
            q_values[timestep.action] = q_update

            X[i] = timestep.state
            Y[i] = q_values

        return X, Y

    def _train(self, X, Y):
        self._model.fit(X, Y, verbose=0)

    def _replay(self):

        not_enough_data = len(self._replay_memory) < self._replay_memory_batch

        if not_enough_data:
            return
        else:
            replay_batch = random.sample(self._replay_memory, self._replay_memory_batch)
            X, Y = self._preprocess_batch(replay_batch)
            self._train(X, Y)

    def _preprocess_state(self, state):
        grayscale_image = np.dot(state[..., :3], [0.299, 0.587, 0.114])
        resized_image = misc.imresize(grayscale_image, [self._height, self._width], 'bilinear')
        pre_processed_image = resized_image.astype(np.float32) / 128.0 - 1.0
        return pre_processed_image
