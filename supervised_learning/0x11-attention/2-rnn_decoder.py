#!/usr/bin/env python3

"""
Defines a class that inherits from tensorflow.keras.layers.Layer
to decode for machine translation
"""


import tensorflow as tf
SelfAttention = __import__('1-self_attention').SelfAttention


class RNNDecoder(tf.keras.layers.Layer):

    def __init__(self, vocab, embedding, units, batch):
        super(RNNDecoder, self).__init__()
        self.embedding = tf.keras.layers.Embedding(input_dim=vocab,output_dim=embedding)
        self.gru = tf.keras.layers.GRU(units,return_state=True,
                                       return_sequences=True, recurrent_initializer="glorot_uniform")
        self.F = tf.keras.layers.Dense(vocab)
        self.attention = SelfAttention(units)
    def call(self, x, s_prev, hidden_states):
        """
        Returns the output word as a one hot vector and
            the new decoder hidden state
        parameters:
            x [tensor of shape (batch, 1)]:
                contains the previous word in the target sequence as
                    an index of the target vocabulary
            s_prev [tensor of shape (batch, units)]:
                contains the previous decoder hidden state
            hidden_states [tensor of shape (batch, input_seq_len, units)]:
                contains the outputs of the encoder
        returns:
            y, s:
                y [tensor of shape (batch, vocab)]:
                    contains the output word as a one hot vector in
                        the target vocabulary
                s [tensor of shape (batch, units)]:
                    contains the new decoder hidden state
        """
       
        x = self.embedding(x)
        context, _ = self.attention(s_prev, hidden_states)
        context = tf.expand_dims(context, 1)
        x = tf.concat([context, x], axis=-1)
        y, s = self.gru(x)
        y = tf.reshape(y, (-1, y.shape[2]))
        y = self.F(y)
        return y, s