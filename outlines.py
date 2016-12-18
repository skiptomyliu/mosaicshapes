import numpy as np
import matplotlib.pyplot as plt

from skimage import measure
import os
from skimage import io

from skimage.color import rgb2grey



moi = io.imread("./examples/test.JPEG")


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

# test = np.array([[1,2,3,4],[5,6,7,8], [9,10,11,12],[13,14,15,16],[17,18,19,20]])
# (Pdb) test
# array([[ 1,  2,  3,  4],
#        [ 5,  6,  7,  8],
#        [ 9, 10, 11, 12],
#        [13, 14, 15, 16],
#        [17, 18, 19, 20]])
# test[1:3,0:3]
# array([[ 5,  6,  7],
#        [ 9, 10, 11]])
# np.where(edges1==True)

# (Pdb) test2 = np.array([[False, False, False, False], [False, False, False, False], [True, True, False, True], [False, True, False, True]])
# (Pdb) test2
# array([[False, False, False, False],
#        [False, False, False, False],
#        [ True,  True, False,  True],
#        [False,  True, False,  True]], dtype=bool)
# (Pdb) np.where(test2==True)
# (array([2, 2, 2, 3, 3]), array([0, 1, 3, 1, 3]))

from scipy import ndimage as ndi

from skimage import feature


# Generate noisy image of a square
# im = np.zeros((128, 128))
# im[32:-32, 32:-32] = 1

# im = ndi.rotate(im, 15, mode='constant')
# im = ndi.gaussian_filter(im, 4)
# im += 0.2 * np.random.random(im.shape)

# Compute the Canny filter for two values of sigma

edges1 = feature.canny(img, sigma=3)
edges2 = feature.canny(img, sigma=4)
# slope \ 
# edges2[595:610,104:110]
 # x,y = np.where(edges2[595:610,104:110]==True)
 # np.polyfit(x,y,1)
# edges2[y_start:y_end,x_start:x_end]
# edges2[row_start:row_end,col_start:col_end]

# slope /
# edges2[270:280,188:197]
# x,y=np.where(edges2[270:280,188:197]==True)
# np.polyfit(x,y,1)

# < edge
# edges2[730:765,120:128]

# display results
fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3), sharex=True, sharey=True)
# fig, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(8, 3), sharex=True, sharey=True)

ax1.imshow(img, cmap=plt.cm.jet)
ax1.axis('off')
ax1.set_title('noisy image', fontsize=20)

ax2.imshow(edges1, cmap=plt.cm.gray)
ax2.axis('off')
ax2.set_title('Canny filter, $\sigma=1$', fontsize=20)

ax3.imshow(edges2, cmap=plt.cm.gray)
ax3.axis('on')
ax3.set_title('Canny filter, $\sigma=3$', fontsize=20)
ax3.yaxis.label.set_color('red')
ax3.xaxis.label.set_color('red')

# fig.subplots_adjust(wspace=0.02, hspace=0.02, top=0.9,
#                     bottom=0.02, left=0.02, right=0.98)

plt.show()