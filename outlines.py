import numpy as np
import matplotlib.pyplot as plt

from skimage import measure
import os
from skimage import io

from skimage.color import rgb2grey



moi = io.imread("./examples/moi.JPEG")


# Construct some test data
x, y = np.ogrid[-np.pi:np.pi:100j, -np.pi:np.pi:100j]
r_sample = np.sin(np.exp((np.sin(x)**3 + np.cos(y)**2)))

# Find contours at a constant value of 0.8

img = rgb2grey(moi)
contours = measure.find_contours(img, .48)
# import pdb; pdb.set_trace()
# contours = measure.find_contours(r, 0.8)

# Display the image and plot all contours found
fig, ax = plt.subplots()
ax.imshow(img, interpolation='nearest')
ax.imshow(img, interpolation='nearest', cmap=plt.cm.gray)

for n, contour in enumerate(contours):
    ax.plot(contour[:, 1], contour[:, 0], linewidth=5)

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()




from scipy import ndimage as ndi

from skimage import feature


# Generate noisy image of a square
# im = np.zeros((128, 128))
# im[32:-32, 32:-32] = 1

# im = ndi.rotate(im, 15, mode='constant')
# im = ndi.gaussian_filter(im, 4)
# im += 0.2 * np.random.random(im.shape)

# Compute the Canny filter for two values of sigma
edges1 = feature.canny(img, sigma=2)
edges2 = feature.canny(img, sigma=3)

import pdb; pdb.set_trace()
# display results
fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3), sharex=True, sharey=True)

ax1.imshow(img, cmap=plt.cm.jet)
ax1.axis('off')
ax1.set_title('noisy image', fontsize=20)

ax2.imshow(edges1, cmap=plt.cm.gray)
ax2.axis('off')
ax2.set_title('Canny filter, $\sigma=1$', fontsize=20)

ax3.imshow(edges2, cmap=plt.cm.gray)
ax3.axis('off')
ax3.set_title('Canny filter, $\sigma=3$', fontsize=20)

fig.subplots_adjust(wspace=0.02, hspace=0.02, top=0.9,
                    bottom=0.02, left=0.02, right=0.98)

plt.show()