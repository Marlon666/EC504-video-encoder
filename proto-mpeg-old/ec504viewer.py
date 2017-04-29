import matplotlib.pyplot as plt
import matplotlib as mpl
import time
import numpy as np

mpl.rcParams['toolbar'] = 'None'

def view_sequence(images, delay):
    """
    :param images: list (or other iterable) containing sequence of images to show
    :param delay: time (seconds) to show each image
    :return: none
    """

    if len(images) == 0:
        raise Exception("Must display at least one image")
    fig, ax = plt.subplots(1)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.canvas.set_window_title("EC504 Viewer")
    im = ax.imshow(np.zeros((256, 256, 3)), extent=(0, 1, 1, 0))
    ax.axis('tight')
    ax.axis('off')
    fig.show()

    for image in images:
        im.set_data(image)
        im.axes.figure.canvas.draw()
        time.sleep(delay)

def view_single(image):
    plt.imshow(image, extent=(0, 1, 1, 0))
    ax = plt.gca()
    ax.axis('tight')
    ax.axis('off')
    fig = plt.gcf()
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    fig.canvas.set_window_title("EC504 Viewer")
    plt.show()
