"""
Denoising Autoencoders example with MNIST

Ken Chen
"""

import tensorflow as tf
import numpy as np
import math

class SDAutoencoder:
    """A stacked denoising autocoder implementation"""

    def __init__(dimensions):
        """
        dimensions (list): The number of neurons for each layer of the autoencoder. Ex: [784, 512, 256, 64]. The first item in the list
        should be the number of features in the input. The last item in
        the list should be the number of features in the output.
        """
        self.dimensions = dimensions
        self.x, \
        self.z, \
        self.y, \
        self.corrupt_prob, \
        self.cost = _build()

    def _build():
        x = tf.placeholder(tf.float32, [None, self.dimensions[0]], name="x")

        # Probability of corrupting the input:
            # 1 for training
            # 0 for testing/production
        corrupt_prob = tf.placeholder(tf.float32, [1])
        current_input = corrupt(x) * corrupt_prob + x * (1 - corrupt_prob)

        # Build the encoder and the latent representation
        encoder, z = _build_encoder(current_input)

        # Reconstructed input
        current_input = z
        y = _decode(current_input, encoder)

        # Cost function measures pixel-wise difference
        cost = tf.sqrt(tf.reduce_mean(tf.square(y - x)))
        return x, z, y, corrupt_prob, cost

    def _build_encoder(input_tensor):
        """Builds the encoder based on a given input and `dimensions`

        input (Tensor): the input Tensor

        returns: ([Tensor], Tensor): a tuple containing:
            - A list of weight tensors used in each layer
            - The transformed input (z) after several layers
        """
        encoder = []
        for layer_i, n_output in enumerate(self.dimensions[1:]):
            n_input = int(input_tensor.get_shape()[1])
            W = tf.Variable(tf.random_uniform(
                shape=[n_input, n_output],
                minval=-1.0 / math.sqrt(n_input),
                maxval=1.0 / math.sqrt(n_input)
            ))
            b = tf.Variable(tf.zeros([n_output]))
            encoder.append(W)
            output = tf.nn.tanh(tf.matmul(input_tensor, W) + b)
            input_tensor = output
        return encoder, output

    def _decode(encoded_tensor, encoder):
        """Decodes the encoded_tensor by reversing operations using
        a reversed incoder

        encoded_tensor (Tensor): An encoded Tensor
        encoder ([Tensor]): The list of weight Tensors used to transform the original input

        returns: (Tensor) The decoded Tensor y
        """
        # Setup for building decoder
        encoder = encoder[::-1]

        # Build the decoder using the same weights
        for layer_i, n_output in enumerate(self.dimensions[:-1][::-1]):
            W = tf.transpose(encoder[layer_i])
            b = tf.Variable(tf.zeros([n_output]))
            output = tf.nn.tanh(tf.matmul(encoded_tensor, W) + b)
            encoded_tensor = output
        return output

    """
    ########################
    ### HELPER FUNCTIONS ###
    ########################
    """
    def corrupt(x):
        """Takes an input tensor and corrupts half of the values uniformly by zeroing them.

        x (Tensor): input to corrupt
        returns: (Tensor) input with 50 percent of values corrupted
        """
        corruption = tf.cast(tf.random_uniform(
            shape=tf.shape(x),
            minval=0,
            maxval=2,
            dtype=tf.int32
        ), tf.float32)

        return tf.mul(x, corruption)

def main():
    s = SDAutoencoder([784, 256, 128, 64])
    print(vars(s))
    print(dir(s))

if __name__ == "__main__":
    main()