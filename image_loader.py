import scipy
import imageio
from glob import glob
import numpy as np
from progress import Progress


class ImageLoader():
    def __init__(self, name, resolution=(128, 128)):
        self.name = name
        self.resolution = resolution

    def load_images(self, domain, batch_size=1, test=False):
        data_type = "train%s" % domain if not test else "test%s" % domain
        path = glob('./datasets/train/%s/%s/*' % (self.name, data_type))

        batch_images = np.random.choice(path, size=batch_size)

        images = []

        progress = Progress(len(batch_size))

        for index, image_path in enumerate(batch_images, start=1):
            image = self.read_image(image_path)
            if not test:
                image = scipy.misc.imresize(image, self.resolution)

                if np.random.random() > 0.5:
                    image = np.fliplr(image)

            else:
                image = scipy.misc.imresize(image, self.resolution)

            images.append(image)
            progress.update(index, 'Loading images')

        progress.stop()

        images = np.array(images) / 127.5 - 1.

        return images

    def load_batch(self, batch_size=1, test=False):
        data_type = "train" if not test else "val"

        path_A = glob('./datasets/train/%s/%sA/*' % (self.dataset_name, data_type))
        path_B = glob('./datasets/train/%s/%sB/*' % (self.dataset_name, data_type))

        self.number_of_batches = int(min(len(path_A), len(path_B)) / batch_size)
        total_samples = self.number_of_batches * batch_size

        path_A = np.random.choice(path_A, total_samples, replace=False)
        path_B = np.random.choice(path_B, total_samples, replace=False)

        progress = Progress(self.number_of_batches - 1)

        for index in range(self.number_of_batches - 1):
            batch_A = path_A[index * batch_size: (index + 1) * batch_size]
            batch_B = path_B[index * batch_size: (index + 1) * batch_size]
            images_A, images_B = [], []
            for image_A, image_B in zip(batch_A, batch_B):
                imageA = self.imread(image_A)
                imageB = self.imread(image_B)

                image_A = scipy.misc.imresize(image_A, self.resolution)
                image_B = scipy.misc.imresize(image_B, self.resolution)

                if not test and np.random.random() > 0.5:
                    image_A = np.fliplr(image_A)
                    image_B = np.fliplr(image_B)

                images_A.append(image_A)
                images_B.append(image_B)

            imgs_A = np.array(imgs_A) / 127.5 - 1.
            imgs_B = np.array(imgs_B) / 127.5 - 1.

            progress.update(index, 'Loading images')

            yield images_A, images_B
        progress.stop()

    def read_image(self, path):
        return imageio.imread(path, pilmode='RGB').astype(np.float)

    def load_image(self, path):
        image = self.read_image(path)
        iamge = scipy.misc.imresize(image, self.resolution)
        image = image / 256.5 - 1.

        return image[np.newaxis, :, :, :]
