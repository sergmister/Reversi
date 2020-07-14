import numpy as np
from keras.models import Sequential, load_model, Model
from keras.layers import Input, Dense, Conv2D, Flatten, BatchNormalization, Activation, LeakyReLU, add
from keras.optimizers import SGD
from keras import regularizers


class Residual_CNN:

    def __init__(self, input_dim, output_dim, reg_const=0.0001, learning_rate=0.1, momentum=0.9):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.reg_const = reg_const
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.model = self._build_model()

    def predict(self, x):
        return self.model.predict(x)

    def fit(self, states, targets, epochs, verbose, validation_split, batch_size):
        return self.model.fit(states, targets, epochs=epochs, verbose=verbose, validation_split=validation_split, batch_size=batch_size)

    def write(self, game, version):
        self.model.save("/models/version" + "{0:0>4}".format(version) + ".h5")

    def read(self, game, version):
        return load_model("/models/version" + "{0:0>4}".format(version) + ".h5")

    def residual_layer(self, input_block, filters, kernel_size):

        x = self.conv_layer(input_block, filters, kernel_size)

        x = Conv2D(
            filters=filters,
            kernel_size=kernel_size,
            data_format="channels_first",
            padding="same",
            use_bias=False,
            activation="linear",
            kernel_regularizer=regularizers.l2(self.reg_const)
        )(x)

        x = BatchNormalization(axis=1)(x)

        x = add([input_block, x])

        x = LeakyReLU()(x)

        return x

    def conv_layer(self, x, filters, kernel_size):

        x = Conv2D(
            filters=filters,
            kernel_size=kernel_size,
            data_format="channels_first",
            padding="same",
            use_bias=False,
            activation="linear",
            kernel_regularizer=regularizers.l2(self.reg_const)
        )(x)

        x = BatchNormalization(axis=1)(x)
        x = LeakyReLU()(x)

        return x

    def value_head(self, x):

        x = Conv2D(
            filters=1,
            kernel_size=(1, 1),
            data_format="channels_first",
            padding="same",
            use_bias=False,
            activation="linear",
            kernel_regularizer=regularizers.l2(self.reg_const)
        )(x)

        x = BatchNormalization(axis=1)(x)
        x = LeakyReLU()(x)

        x = Flatten()(x)

        x = Dense(
            20,
            use_bias=False,
            activation="linear",
            kernel_regularizer=regularizers.l2(self.reg_const)
        )(x)

        x = LeakyReLU()(x)

        x = Dense(
            1,
            use_bias=False,
            activation="tanh",
            kernel_regularizer=regularizers.l2(self.reg_const),
            name="value_head"
        )(x)

        return x

    def policy_head(self, x):

        x = Conv2D(
            filters=2,
            kernel_size=(1, 1),
            data_format="channels_first",
            padding="same",
            use_bias=False,
            activation="linear",
            kernel_regularizer=regularizers.l2(self.reg_const)
        )(x)

        x = BatchNormalization(axis=1)(x)
        x = LeakyReLU()(x)

        x = Flatten()(x)

        x = Dense(
            self.output_dim,
            use_bias=False,
            activation="softmax",
            kernel_regularizer=regularizers.l2(self.reg_const),
            name="policy_head"
        )(x)

        return x

    def _build_model(self):

        main_input = Input(shape=self.input_dim, name="main_input")

        x = self.conv_layer(main_input, 64, (4, 4))

        for i in range(8):
            x = self.residual_layer(x, 64, (4, 4))

        vh = self.value_head(x)
        ph = self.policy_head(x)

        model = Model(inputs=[main_input], outputs=[vh, ph])
        model.compile(loss={"value_head": "mean_squared_error", "policy_head": "categorical_crossentropy"},
                      optimizer=SGD(lr=self.learning_rate, momentum=self.momentum),
                      loss_weights={"value_head": 0.5, "policy_head": 0.5})

        return model
