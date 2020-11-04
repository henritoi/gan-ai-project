import scipy
import tensorflow as tf
import tensorflow_addons as tfa
from keras.layers import *
from keras.layers.advanced_activations import ReLU
from keras.models import Sequential, Model
from keras.optimizers import Adam
from keras.models import model_from_json
from keras.models import load_model
from keras.models import save_model

from keras.initializers import RandomNormal
import datetime
import matplotlib
import matplotlib.pyplot as plt
import sys
from image_loader import ImageLoader

import numpy as np
import os
import time
from PIL import Image

from glob import glob

'''Lähin kirjottamaan tätä nyt käyttäen esimerkkinä tuota copypaste koodia'''
class CycleGan():
    def __init__(self, data):
        #shape of the input image is 128x128
        self.rows = 128
        self.cols = 128
        self.channels = 3  #should be rgb, check from image loader.py
        self.image_shape = (self.rows, self.cols, self.channels)

        #initialize image_loader
        self.data_name = data
        self.image_loader = ImageLoader(name=self.data_name,resolution=(self.rows, self.cols))

        #Calculate output shape

        patch = int(self.rows / np.power(2,4))

        self.discriminator_patch = (patch, patch,1)
        #number of filters in the first layers
        self.g_filter = 32
        self.d_filter = 64

        self.lambda_cycle = 10 #cycle consistency loss
        self.lambda_id = 0.1 * self.lambda_cycle #identity loss



        #build the discriminators

        self.d_A = self.get_discriminator()
        self.d_B = self.get_discriminator()

        self.d_A.compile(loss='mse', optimizer = Adam(2e-4, 0.5), metrics = ['Accuracy'])
        self.d_B.compile(loss='mse', optimizer = Adam(2e-4, 0.5), metrics = ['Accuracy'])

        #build the generators

        self.g_AB = self.get_generator() # A is the style images
        self.g_BA = self.get_generator() # B is the realworld photos

        image_A = Input(shape=self.image_shape)
        image_B = Input(shape=self.image_shape)

        #translate to other domain (fake images)
        f_B = self.g_AB(image_A)
        f_A = self.g_BA(image_B)

        #reconstruct back to original domain

        recon_A = self.g_BA(f_B)
        recon_B = self.g_AB(f_A)

        #identity mapping

        image_A_id = self.g_BA(image_A)
        image_B_id = self.g_AB(image_B)

        # the combined model will only train the generators

        self.d_A.trainable = False
        self.d_B.trainable = False

        #the validity of images based on discriminator

        val_A = self.d_A(f_A)
        val_B = self.d_B(f_B)

        #combined model

        self.comb = Model(input=[image_A, image_B], output=[val_A, val_B, recon_A, recon_B, image_A_id, image_B_id])

        self.comb.compile(loss=['mse','mse', 'mse','mse', 'mse','mse'], loss_weights=[1, 1, self.lambda_cycle, self.lambda_cycle, self.lambda_id, self.lambda_id], optimizer = Adam(2e-4, 0.5))

    def get_generator(self):

        def conv2d(layer_input, filter, f_size=4): #downsampling
            d = Conv2D(filter, kernel_size = f_size, strides=2, padding='same')(layer_input)
            d = LeakyReLU(alpha=0.2)(d)
            d = tfa.layers.InstanceNormalization()(d)
            return d

        def deconv2d(layer_input, skip_input, filter, f_size = 4): #upSampling
            u = UpSampling2D(size=2)(layer_input)
            u = Conv2D(filter, kernel_size = f_size, strides= 1, padding= 'same', activation='relu')(u)
            u = tfa.layers.InstanceNormalization()(u)
            u = Concatenate()(u, skip_input)
            return u
        #input image
        image = Input(shape=self.image_shape)

        #downSampling
        d1 = conv2d(image, self.g_filter)
        d2 = conv2d(d1, self.g_filter*2)
        d3 = conv2d(d2, self.g_filter*4)
        d4 = conv2d(d3, self.g_filter*8)

        #upSampling

        u1 = deconv2d(d4, d3, self.g_filter*4)
        u2 = deconv2d(u1, d2, self.g_filter*2)
        u3 = deconv2d(u2, d1, self.g_filter)

        u4 = UpSampling2D(size=2)(u3)

        output_gen = Conv2D(self.channels, kernel_size=4, strides=1, padding='same', activation='tanh')(u4)

        return Model(image, output_gen)

    def get_discriminator(self):

        def discrimination(layer_input, filter, f_size=4):
            d = Conv2D(filter, kernel_size=f_size, strides=2, padding='same')(layer_input)
            d = LeakyReLU(alpha=0.2)(d)
            return d
        image = Input(shape=self.image_shape)

        d1 = discrimination(image, self.d_filter)
        d2 = discrimination(d1, self.d_filter*2)
        d3 = discrimination(d2, self.d_filter*4)
        d4 = discrimination(d3, self.d_filter*8)

        val = Conv2D(1, kernel_size=4, strides=1, padding='same')(d4)
        return Model(image, val)
