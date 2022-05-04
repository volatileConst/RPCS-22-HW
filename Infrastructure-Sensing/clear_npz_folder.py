# this script clears all images in the image folder
import os

if __name__ == '__main__':

    # remove the list of all files in the directory
    dir = './dummy_npz'

    for image in os.listdir(dir):
        # remove
        os.remove(os.path.join(dir, image))