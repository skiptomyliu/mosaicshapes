


import numpy as np
import matplotlib.pyplot as plt
from skimage import io, feature
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
from sklearn.datasets import load_sample_image
from sklearn.utils import shuffle
from time import time

class ColorPalette():
    
    def __init__(self, image_path="", n_colors=64):
        self.colorbook = None
        self.kmeans = None
        self.labels = None

        if image_path:
            self.quantize(image_path, n_colors=n_colors)


    def apply_palette_to_image(self, image):

        def recreate_image(codebook, labels, w, h):
            """Recreate the (compressed) image from the code book & labels"""
            d = codebook.shape[1]
            image = np.zeros((w, h, d))
            label_idx = 0
            for i in range(w):
                for j in range(h):
                    image[i][j] = codebook[labels[label_idx]]
                    label_idx += 1
            return image


        moi_image = image
        moi_image = moi_image / float(255)
        w2, h2, d2 = original_shape = tuple(moi_image.shape)
        assert d2 == 3
        moi_array = np.reshape(moi_image, (w2 * h2, d2))
        labels = self.kmeans.predict(moi_array)

         # import pdb; pdb.set_trace()
        
        # Display all results, alongside original image
        plt.figure(1)
        plt.clf()
        ax = plt.axes([0, 0, 1, 1])
        plt.axis('off')
        plt.title('Original image (96,615 colors)')
        plt.imshow(moi_image)

        plt.figure(2)
        plt.clf()
        ax = plt.axes([0, 0, 1, 1])
        plt.axis('off')
        plt.title('Quantized image (64 colors, K-Means)')
        plt.imshow(recreate_image(self.kmeans.cluster_centers_, labels, w2, h2))

        plt.show()

    def quantize(self, image_path, n_colors=64):
        sample_image = io.imread(image_path) 

        # Convert to floats instead of the default 8 bits integer coding. Dividing by
        # 255 is important so that plt.imshow behaves works well on float data (need to
        # be in the range [0-1])
        sample_image = np.array(sample_image, dtype=np.float64)/255

        w, h, d = original_shape = tuple(sample_image.shape)
        assert d == 3
        image_array = np.reshape(sample_image, (w*h, d))

        # xxx:  use percentage of total pixs instead?
        image_array_sample = shuffle(image_array, random_state=0)[:3000] 
        self.kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)
        self.colorbook = self.kmeans.cluster_centers_

        # Get labels for all points in the image
        labels = self.kmeans.predict(image_array)




    # Takes in tuple color, converts to array.
    def translate_color(self, color):
        color = np.asarray(color)/float(255)
        color = color.reshape(1,-1)

        label = self.kmeans.predict(np.asarray(color))
        rgbs = self.colorbook[label]*255
        return tuple(rgbs[0])


