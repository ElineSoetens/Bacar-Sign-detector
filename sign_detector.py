"""This is a Simplistic Sign Detector modules.

   A Sign Detector module is a python file that contains a `detect` function
   that is capable of analyzing a color image which, according to the image
   server, likely contains a road sign. The analysis should identify the kind
   of road sign contained in the image.

   See the description of the `detect` function below for more details.
"""

import logging
import numpy as np
import cv2


# Log which sign detector is being used. This appears in the output. Useful
# for ensuring that the correct sign detector is being used.
logging.info('Simplistic SignDetector has been initialized')


def detect(bb, sign):
    """This method receives:
    - sign: a color image (numpy array of shape (h,w,3))
    - bb which is the bounding box of the sign in the original camera view
      bb = (x0,y0, w, h) where w and h are the widht and height of the sign
      (can be used to determine e.g., whether the sign is to the left or
       right)
    The goal of this function is to recognize  which of the following signs
    it really is:
    - a stop sign
    - a turn left sign
    - a turn right sign
    - None, if the sign is determined to be none of the above

    Returns: a dictionary dict that contains information about the recognized
    sign. This dict is transmitted to the state machine it should contain
    all the information that the state machine to act upon the sign (e.g.,
    the type of sign, estimated distance).

    This simplistic detector always returns "STOP", copies the bounding box
    to the dictionary.
    """

    sign_r = sign[:,:,2]
    sign_b = sign[:,:,0]
    somme_r = 0
    somme_b = 0
    for i in range(sign.shape[1]):
        somme_r += sign_r[(sign.shape[0]//2),i]
    for i in range(sign.shape[1]):
        somme_b += sign_b[(sign.shape[0]//2),i]
    if somme_r > somme_b:
        res = 'STOP'
    else:
        res = 'OBLIGATION'
    #largeur de l'image
    width = sign.shape[1]
    #on separe l'image en deux et on prend un x de repere a droite et a gauche
    x0 = width//2
    xl = x0*2//3
    xr = x0 +x0//3
    #verifie l'intensite a gauche
    somme_b_g = 0
    for i in range(sign.shape[0]):
        somme_b_g += sign_b[i,xl]
    #verifie l'intensite a droite
    somme_b_d = 0
    for i in range(sign.shape[0]):
        somme_b_d += sign_b[i,xr]
    if res == 'OBLIGATION' and somme_b_g > somme_b_d:
        res = 'GAUCHE'
    if res == 'OBLIGATION' and somme_b_g < somme_b_d:
        res = 'DROITE' 

    (x0, y0, w, h) = bb
    return {'sign': res, 'x0': x0, 'y0': y0, 'w': w, 'h': h}
		
