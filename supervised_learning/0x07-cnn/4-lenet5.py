#!/usr/bin/env python3
""" task 4 CNN """

import tensorflow as tf

def lenet5(x, y):
    init = tf.contrib.layers.variance_scaling_initializer()
    layer_conv1 = tf.layers.Conv2D(filters=6,
                                   kernel_size=5,
                                   padding="same",
                                   kernel_initializer=init,
                                   activation=tf.nn.relu)(x)

    layer_pool1 = tf.layers.MaxPooling2D(pool_size=[2, 2],
                                         strides=2)(layer_conv1)

    layer_conv2 = tf.layers.Conv2D(filters=16,
                                   kernel_size=5,
                                   padding="valid",
                                   kernel_initializer=init,
                                   activation=tf.nn.relu)(layer_pool1)

    layer_pool2 = tf.layers.MaxPooling2D(pool_size=[2, 2],
                                         strides=2)(layer_conv2)

    
    layer_flat1 = tf.layers.Flatten()(layer_pool2)

    layer_fully1 = tf.layers.Dense(units=120,
                                   activation=tf.nn.relu,
                                   kernel_initializer=init)(layer_flat1)

    layer_fully2 = tf.layers.Dense(units=84,
                                   activation=tf.nn.relu,
                                   kernel_initializer=init)(layer_fully1)

    out = tf.layers.Dense(units=10,
                          activation=tf.nn.softmax,
                          kernel_initializer=init)(layer_fully2)

    loss = tf.losses.softmax_cross_entropy(y, out)
    optimizer = tf.train.AdamOptimizer().minimize(loss)

    labels = tf.argmax(y, 1)
    predictions = tf.argmax(out, 1)
    equality = tf.equal(labels, predictions)
    accuracy = tf.reduce_mean(tf.cast(equality, tf.float32))

    return out, optimizer, loss, accuracy                                     