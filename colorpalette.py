


import numpy as np
import matplotlib.pyplot as plt
from skimage import io, feature
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
from sklearn.datasets import load_sample_image
from sklearn.utils import shuffle
from time import time

class ColorPalette():
    
    def __init__(self):
        self.colorbook = None
        self.kmeans = None
        self.labels = None
        pass



    def quantize(self, image_path, n_colors=64, testing_image_path=""):

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


        sample_image = io.imread(image_path) 

        # Convert to floats instead of the default 8 bits integer coding. Dividing by
        # 255 is important so that plt.imshow behaves works well on float data (need to
        # be in the range [0-1])
        sample_image = np.array(sample_image, dtype=np.float64)/255

        w, h, d = original_shape = tuple(sample_image.shape)
        assert d == 3
        image_array = np.reshape(sample_image, (w*h, d))

        # xxx:  use percentage of total pixs instead?
        image_array_sample = shuffle(image_array, random_state=0)[:2000] 
        self.kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)
        self.colorbook = self.kmeans.cluster_centers_

        # Get labels for all points in the image
        labels = self.kmeans.predict(image_array)



        """
        testing
        """
        n_colors = 64
        # Load the Summer Palace photo
        china = load_sample_image("china.jpg")

        # Convert to floats instead of the default 8 bits integer coding. Dividing by
        # 255 is important so that plt.imshow behaves works well on float data (need to
        # be in the range [0-1])
        china = np.array(china, dtype=np.float64) / 255

        # Load Image and transform to a 2D numpy array.
        w, h, d = original_shape = tuple(china.shape)
        assert d == 3
        image_array = np.reshape(china, (w * h, d))

        
        moi_image = io.imread(testing_image_path) 
        moi_image = moi_image / float(255)
        w2, h2, d2 = original_shape = tuple(moi_image.shape)
        assert d2 == 3
        moi_array = np.reshape(moi_image, (w2 * h2, d2))

        print("Fitting model on a small sub-sample of the data")
        t0 = time()
        moi_array_sample = shuffle(moi_array, random_state=0)[:1000]
        kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(moi_array_sample)
        print("done in %0.3fs." % (time() - t0))

        # Get labels for all points
        print("Predicting color indices on the full image (k-means)")
        t0 = time()
        labels = kmeans.predict(image_array)
        print("done in %0.3fs." % (time() - t0))

        # myself: shuffle our image, then sample 64 of the random colors.  Calculate closest distance
        # distance between each r,g,b value with original image_array.  
        # codebook_random = shuffle(image_array, random_state=0)[:n_colors + 1]
        # #image_array[:n_colors+1] 
        # print("Predicting color indices on the full image (random)")
        # t0 = time()
        # labels_random = pairwise_distances_argmin(codebook_random,
        #   image_array,
        #   axis=0)
        # print("done in %0.3fs." % (time() - t0))



        # import pdb; pdb.set_trace()
        
        # Display all results, alongside original image
        plt.figure(1)
        plt.clf()
        ax = plt.axes([0, 0, 1, 1])
        plt.axis('off')
        plt.title('Original image (96,615 colors)')
        plt.imshow(china)

        plt.figure(2)
        plt.clf()
        ax = plt.axes([0, 0, 1, 1])
        plt.axis('off')
        plt.title('Quantized image (64 colors, K-Means)')
        plt.imshow(recreate_image(kmeans.cluster_centers_, labels, w, h))

        # plt.figure(3)
        # plt.clf()
        # ax = plt.axes([0, 0, 1, 1])
        # plt.axis('off')
        # plt.title('Quantized image (64 colors, Random)')
        # plt.imshow(recreate_image(codebook_random, labels_random, w, h))
        plt.show()


    # Takes in tuple color, converts to array.
    def translate_color(self, color):
        color = np.asarray(color)/float(255)
        color = color.reshape(1,-1)

        label = self.kmeans.predict(np.asarray(color))
        print label
        # import pdb; pdb.set_trace()
        self.colorbook[label]

        pass


