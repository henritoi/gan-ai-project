import scipy
import tensorflow as tf
import tensorflow_addons as tfa
from keras.layers import *
from keras.layers.advanced_activations import LeakyReLU
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

# Lähin kirjottamaan tätä nyt käyttäen esimerkkinä tuota copypaste koodia


class CycleGan():
    # data is the name of the dataset
    def __init__(self, data):
        # shape of the input image is 128x128
        self.rows = 128
        self.cols = 128
        self.channels = 3  # should be rgb, check from image loader.py
        self.image_shape = (self.rows, self.cols, self.channels)

        # initialize image_loader
        self.data_name = data
        self.image_loader = ImageLoader(name=self.data_name, resolution=(self.rows, self.cols))

        # Calculate output shape

        patch = int(self.rows / np.power(2, 4))

        self.discriminator_patch = (patch, patch, 1)
        # number of filters in the first layers
        self.generator_filter = 32
        self.disc_filter = 64

        self.lambda_cycle = 10  # cycle consistency loss
        self.lambda_id = 0.1 * self.lambda_cycle  # identity loss

        # build the discriminators

        self.disc_A = self.get_discriminator()
        self.disc_B = self.get_discriminator()

        self.disc_A.compile(loss='mse', optimizer=Adam(2e-4, 0.5), metrics=['Accuracy'])
        self.disc_B.compile(loss='mse', optimizer=Adam(2e-4, 0.5), metrics=['Accuracy'])

        # build the generators

        self.generate_AB = self.get_generator()  # A is the style images
        self.generate_BA = self.get_generator()  # B is the realworld photos

        image_A = Input(shape=self.image_shape)
        image_B = Input(shape=self.image_shape)

        # translate to other domain (fake images)
        f_B = self.generate_AB(image_A)
        f_A = self.generate_BA(image_B)

        # reconstruct back to original domain

        recon_A = self.generate_BA(f_B)
        recon_B = self.generate_AB(f_A)

        # identity mapping

        image_A_id = self.generate_BA(image_A)
        image_B_id = self.generate_AB(image_B)

        # the combined model will only train the generators

        self.disc_A.trainable = False
        self.disc_B.trainable = False

        # the validity of images based on discriminator

        val_A = self.disc_A(f_A)
        val_B = self.disc_B(f_B)

        # combined model

        self.comb = Model(input=[image_A, image_B], output=[val_A, val_B, recon_A, recon_B, image_A_id, image_B_id])

        self.comb.compile(loss=['mse', 'mse', 'mse', 'mse', 'mse', 'mse'],
                          loss_weights=[1, 1, self.lambda_cycle, self.lambda_cycle, self.lambda_id, self.lambda_id],
                          optimizer=Adam(2e-4, 0.5))

    def get_generator(self):

        def conv2d(layer_input, filter, f_size=4):  # downsampling
            d = Conv2D(filter, kernel_size=f_size, strides=2, padding='same')(layer_input)
            d = LeakyReLU(alpha=0.2)(d)
            d = tfa.layers.InstanceNormalization()(d)
            return d

        def deconv2d(layer_input, skip_input, filter, f_size=4):  # upSampling
            u = UpSampling2D(size=2)(layer_input)
            u = Conv2D(filter, kernel_size=f_size, strides=1, padding='same', activation='relu')(u)
            u = tfa.layers.InstanceNormalization()(u)
            u = Concatenate()(u, skip_input)
            return u

        # input image
        image = Input(shape=self.image_shape)

        # downSampling
        d1 = conv2d(image, self.generator_filter)
        d2 = conv2d(d1, self.generator_filter * 2)
        d3 = conv2d(d2, self.generator_filter * 4)
        d4 = conv2d(d3, self.generator_filter * 8)

        # upSampling

        u1 = deconv2d(d4, d3, self.generator_filter * 4)
        u2 = deconv2d(u1, d2, self.generator_filter * 2)
        u3 = deconv2d(u2, d1, self.generator_filter)

        u4 = UpSampling2D(size=2)(u3)

        output_gen = Conv2D(self.channels, kernel_size=4, strides=1, padding='same', activation='tanh')(u4)

        return Model(image, output_gen)

    def get_discriminator(self):

        def discrimination(layer_input, filter, f_size=4):
            d = Conv2D(filter, kernel_size=f_size, strides=2, padding='same')(layer_input)
            d = LeakyReLU(alpha=0.2)(d)
            return d

        image = Input(shape=self.image_shape)

        d1 = discrimination(image, self.disc_filter)
        d2 = discrimination(d1, self.disc_filter * 2)
        d3 = discrimination(d2, self.disc_filter * 4)
        d4 = discrimination(d3, self.disc_filter * 8)

        val = Conv2D(1, kernel_size=4, strides=1, padding='same')(d4)
        return Model(image, val)

    # batch_size: number of images in one batch
    # sample_interval: interval in epcohs between sample predictions
    # saving_interval: interval in epochs between checkpoints
    # print_interval: interval in batches between printing checkpoints
    def train(self, epochs, batch_size=1, sample_interval=1, saving_interval=50, print_interval=50):

        # ground truths
        valid = np.ones((batch_size,) + self.discriminator_patch)
        fake = np.zeros((batch_size,) + self.discriminator_patch)

        for epoch in range(epochs):
            for batch_index, (imageA, imageB) in enumerate(self.image_loader(batch_size)):

                # translate images into domains, fake images
                f_B = self.generate_AB.predict(imageA)
                f_A = self.generate_BA.predict(imageB)

                # train discriminators
                real_dA_loss = self.disc_A.train_on_batch(imageA, valid)
                fake_dA_loss = self.disc_A.train_on_batch(f_A, fake)
                loss_dA = 0.5 * np.add(real_dA_loss, fake_dA_loss)

                real_dB_loss = self.disc_B.train_on_batch(imageB, valid)
                fake_dB_loss = self.disc_B.train_on_batch(f_B, fake)
                loss_dB = 0.5* np.add(real_dB_loss, fake_dB_loss)

                # training the generator with the sample pictures
                generator_loss = self.comb.train_on_batch([imageA, imageB],
                                                          [valid, valid, imageA, imageB, imageA, imageB])

                if batch_index % print_interval == 0:
                    print("Epoch: %d / %d total loss on images A: %f Total loss on images B: %f" % (
                    epoch, epochs, loss_dA, loss_dB))

                if epoch % saving_interval == 0:
                    self.epoch = epoch
                    path = "saved_model/" + self.data_name + "/epoch_" + str(self.epoch)
                    if not os.path.exists(path):
                        os.makedirs(path)
                    self.disc_A.save_weights(path + "/discriminatorA_weights.h5")
                    self.disc_B.save_weights(path + "/discriminatorA_weights.h5")
                    self.disc_A.save_model(path + "/discriminatorA_model.h5")
                    self.disc_B.save_model(path + "/discriminatorB_model.h5")

                    self.generate_AB.save_model(path + "/generatorAB_model.h5")
                    self.generate_BA.save_model(path + "/generatorBA_model.h5")
                    self.generate_AB.save_weights(path + "/generatorAB_weights.h5")
                    self.generate_BA.save_weights(path + "/generatorBA_weights.h5")
                if epoch % sample_interval == 0:
                    self.create_samples(epoch)

        self.epoch = "finished"
        path = "saved_model/" + self.data_name + "/epoch_" + str(self.epoch)
        if not os.path.exists(path):
            os.makedirs(path)
        self.disc_A.save_weights(path + "/discriminatorA_weights.h5")
        self.disc_B.save_weights(path + "/discriminatorA_weights.h5")
        self.disc_A.save_model(path + "/discriminatorA_model.h5")
        self.disc_B.save_model(path + "/discriminatorB_model.h5")

        self.generate_AB.save_model(path + "/generatorAB_model.h5")
        self.generate_BA.save_model(path + "/generatorBA_model.h5")
        self.generate_AB.save_weights(path + "/generatorAB_weights.h5")
        self.generate_BA.save_weights(path + "/generatorBA_weights.h5")

    def test(self):
        path = "saved_model/" + self.data_name + "/epoch_" + str(self.epoch)
        if not os.path.exists(path):
            return ("No such path: %s exists" % path)
        self.disc_A = load_model(path + "/discriminatorA_model.h5")
        self.disc_B = load_model(path + "/discriminatorB_model.h5")
        self.disc_A.load_weights(path + "/discriminatorA_weights.h5")
        self.disc_B.load_weights(path + "/discriminatorB_weights.h5")

        self.generate_AB = load_model(path + "/discriminatorA_model.h5")
        self.generate_BA = load_model(path + "/discriminatorB_model.h5")
        self.generate_AB.load_weights(path + "/discriminatorA_weights.h5")
        self.generate_BA.load_weights(path + "/discriminatorB_weights.h5")

        image_paths = glob('./testing/original/*')

        for image_path in image_paths:
            filename = os.path.basename(image_path)
            imageB = self.image_loader(path=image_path)
            fakeA = self.generate_BA.predict(imageB)

            scipy.misc.imsave('/testing/fakes/%s/%s' % (self.data_name, filename), arr=fakeA)

    def create_samples(self, epoch):
        os.makedirs('samples/%s' % self.data_name)

        # load all the images related to the domains
        images_A = self.image_loader.load_images(domain="A", test=True)
        images_B = self.image_loader.load_images(domain="B", test=True)

        # generate fake images
        f_B = self.generate_AB.predict(images_A)
        f_A = self.generate_BA.predict(images_B)

        # reconstruct images from fakes
        recon_A = self.generate_BA.predict(f_B)
        recon_B = self.generate_AB.predict(f_A)

        gen_images = np.concatenate([images_A, f_B, recon_A, images_B, f_A, recon_B])

        # rescale

        gen_images = 0.5 * gen_images + 0.5

        # display and save images
        titles = ['Original', 'Generated', 'Reconstructed']
        fig, ax = plt.subplots(2, 3)
        index = 0
        for i in range(2):
            for j in range(3):
                ax[i, j].imshow(gen_images[index])
                ax[i, j].set_title(titles[j])
                ax[i, j].axis('off')
                index += 1
        fig.savefig("sample_images/%s/%d" % (self.data_name, epoch))
        print("Sample images have been saved")
        plt.close()
