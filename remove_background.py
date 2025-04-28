from rembg import remove
from PIL import Image
import cv2
import numpy as np

def remove_background(myimage):
        # Open the image using PIL
        input_image = myimage

        # Remove background
        output_image = remove(input_image)

        # Convert to OpenCV format and ouptut
        return np.array(output_image)