####################################
#
#  PDSB Project 2021
#
#  Module: Classification with Convolutional Neural Networks (CNN)
#  File: create_model
#
#  Created on May 30, 2021
#  Last modified on June 28, 2021
#
#  Code rights reserved to João Saraiva
#
####################################

import tensorflow as tf


def create_model(name, input_shape):
    """
    Receives a network name and the input size of the tensor entering the first layer.
    Returns the 2D CNN proposed by Borra, D., Fantozzi, S., and Magosso, E. (2020)
    URL: https://link.springer.com/chapter/10.1007%2F978-3-030-31635-8_223

    Input shape should be 'channels last', i.e., (height, width, channel) -- because tensorflow cpu version forces that
    Each input should be one epoch of the experiments.
    Note: channels here have a meaning in the context of ML, not in the context of EEG channels.
    Example: input_shape =  (8, 140, 1) means a 2D image of 8 EEG channels with 140 data points recorded by each.

    The datasets given should be in the shape (samples, height, width, channel),
    meaning each training/test set has #examples=samples. (An example is an input.)
    """

    model = tf.keras.Sequential(name=name)

    # Subnet A

    # A1
    model.add(tf.keras.layers.InputLayer(input_shape, name='Input'))

    # A2
    model.add(tf.keras.layers.ZeroPadding2D((0, 32)))
    model.add(tf.keras.layers.Conv2D(filters=8, kernel_size=(1, 64), use_bias=False))

    # A3
    model.add(tf.keras.layers.BatchNormalization(axis=-1, momentum=0.01, epsilon=1e-3, trainable=True))
    #model.add(tf.keras.layers.BatchNormalization())
    # Here "features" means "space features", since want it to normalize along the 8 channels. So, axis=-1.

    # A4
    #model.add(tf.keras.layers.DepthwiseConv2D(kernel_size=(8, 1), depth_multiplier=2, strides=1, use_bias=False, groups=8))
    #model.add(tf.keras.layers.DepthwiseConv2D(kernel_size=(8, 1), depth_multiplier=2, use_bias=False, groups=8, kernel_constraint=tf.keras.constraints.max_norm(1)))
    model.add(tf.keras.layers.DepthwiseConv2D(kernel_size=(8, 1), depth_multiplier=2, use_bias=False, groups=8, depthwise_constraint=tf.keras.constraints.max_norm(1.)))

    # A5
    model.add(tf.keras.layers.BatchNormalization(axis=-1, momentum=0.01, epsilon=1e-3, trainable=True))
    #model.add(tf.keras.layers.BatchNormalization())

    # A6
    model.add(tf.keras.layers.Activation(activation='elu'))

    # A7
    model.add(tf.keras.layers.AveragePooling2D(pool_size=(1, 4), strides=(1, 4)))

    # A8
    model.add(tf.keras.layers.Dropout(0.25))

    # Subnet B

    # B1 and B2
    model.add(tf.keras.layers.ZeroPadding2D((0, 8)))
    #model.add(tf.keras.layers.SeparableConv2D(filters=16, kernel_size=(1, 16), depth_multiplier=1, strides=1, use_bias=False, groups=16))
    model.add(tf.keras.layers.SeparableConv2D(filters=16, kernel_size=(1, 16), use_bias=False, groups=16))

    # B3
    model.add(tf.keras.layers.BatchNormalization(axis=-1, momentum=0.01, epsilon=1e-3, trainable=True))
    #model.add(tf.keras.layers.BatchNormalization())

    # B4
    model.add(tf.keras.layers.Activation(activation='elu'))

    # B5
    model.add(tf.keras.layers.AveragePooling2D(pool_size=(1, 8), strides=(1, 8)))

    # B6
    model.add(tf.keras.layers.Dropout(0.25))

    # Subnet C
    model.add(tf.keras.layers.Flatten())

    # C1
    model.add(tf.keras.layers.Dense(units=2, use_bias=True, kernel_constraint=tf.keras.constraints.max_norm(0.25)))

    # C2
    model.add(tf.keras.layers.Activation(activation='softmax', name='Output'))

    return model

