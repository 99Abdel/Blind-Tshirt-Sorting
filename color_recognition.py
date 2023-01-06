import cv2
import numpy as np
from skimage.io import imread, imshow
from skimage.color import rgb2hsv
from skimage.color import hsv2rgb
from matplotlib import pyplot as plt


def gray_image(image):
    fig, ax = plt.subplots(1, 3, figsize=(12, 4))
    ax[0].imshow(image[:, :, 0], cmap='gray')
    ax[0].set_title('Hue')
    ax[1].imshow(image[:, :, 1], cmap='gray')
    ax[1].set_title('Saturation')
    ax[2].imshow(image[:, :, 2], cmap='gray')
    ax[2].set_title('Value');
    plt.show()

def hsv_plot(image):
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    ax[0].imshow(image[:, :, 0], cmap='hsv')
    ax[0].set_title('hue')
    ax[1].imshow(image[:, :, 1], cmap='hsv')
    ax[1].set_title('transparency')
    ax[2].imshow(image[:, :, 2], cmap='hsv')
    ax[2].set_title('value')
    fig.colorbar(imshow(image[:, :, 0], cmap='hsv'))
    fig.tight_layout()
    plt.show()

def create_masks(image,image_hsv,low_lim,high_lim):
    # refer to hue channel (in the colorbar)
    lower_mask = image_hsv[:, :, 0] > low_lim[0]
    # refer to hue channel (in the colorbar)
    upper_mask = image_hsv[:, :, 0] < high_lim[0]
    # refer to transparency channel (in the colorbar)
    #saturation_mask = image_hsv[:, :, 1] >

    mask = upper_mask * lower_mask #* saturation_mask
    red = image[:, :, 0] * mask
    green = image[:, :, 1] * mask
    blue = image[:, :, 2] * mask
    bags_masked = np.dstack((red, green, blue))
    imshow(bags_masked)
    plt.show()

# Blue color
low_blue = np.array([90, 80, 2])
high_blue = np.array([126, 255, 255])

image = cv2.imread("images_test/blue.png")
plt.imshow(image)
plt.show()
image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
plt.imshow(image)
plt.show()
image_hsv = rgb2hsv(image)*255
gray_image(image_hsv)
hsv_plot(image_hsv)
create_masks(image,image_hsv,low_blue,high_blue)

a = 0