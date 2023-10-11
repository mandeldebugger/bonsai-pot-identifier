#!/usr/bin/env python3

import cv2
import numpy as np
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilenames
import matplotlib.pyplot as plt

USERFILES = []


def rotate_image(image, angle):
    # Grab the dimensions of the image and then determine the center
    (h, w) = image.shape[:2]
    (cX, cY) = (w / 2, h / 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # Compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # Adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # Perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

def perspective_transform(image, corners):
    def order_corner_points(corners):
        # Separate corners into individual points
        # Index 0 - top-right
        #       1 - top-left
        #       2 - bottom-left
        #       3 - bottom-right
        corners = [(corner[0][0], corner[0][1]) for corner in corners]
        top_r, top_l, bottom_l, bottom_r = corners[0], corners[1], corners[2], corners[3]
        return (top_l, top_r, bottom_r, bottom_l)

    # Order points in clockwise order
    ordered_corners = order_corner_points(corners)
    top_l, top_r, bottom_r, bottom_l = ordered_corners

    # Determine width of new image which is the max distance between 
    # (bottom right and bottom left) or (top right and top left) x-coordinates
    width_A = np.sqrt(((bottom_r[0] - bottom_l[0]) ** 2) + ((bottom_r[1] - bottom_l[1]) ** 2))
    width_B = np.sqrt(((top_r[0] - top_l[0]) ** 2) + ((top_r[1] - top_l[1]) ** 2))
    width = max(int(width_A), int(width_B))

    # Determine height of new image which is the max distance between 
    # (top right and bottom right) or (top left and bottom left) y-coordinates
    height_A = np.sqrt(((top_r[0] - bottom_r[0]) ** 2) + ((top_r[1] - bottom_r[1]) ** 2))
    height_B = np.sqrt(((top_l[0] - bottom_l[0]) ** 2) + ((top_l[1] - bottom_l[1]) ** 2))
    height = max(int(height_A), int(height_B))

    # Construct new points to obtain top-down view of image in 
    # top_r, top_l, bottom_l, bottom_r order
    dimensions = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], 
                    [0, height - 1]], dtype = "float32")

    # Convert to Numpy format
    ordered_corners = np.array(ordered_corners, dtype="float32")

    # Find perspective transform matrix
    matrix = cv2.getPerspectiveTransform(ordered_corners, dimensions)

    # Return the transformed image
    return cv2.warpPerspective(image, matrix, (width, height))

input("Press enter to choose the files to find the bounding box")
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
USERFILES = askopenfilenames() # show an "Open" dialog box and return the path to the selected file    

for i in range(0, len(USERFILES)):    
    print("Box found as follows (" + str(i+1) + ") is " + USERFILES[i])
        
for i in range(0, len(USERFILES)):
    userImage = cv2.imread(USERFILES[i])
    original = userImage.copy()
    greyImage = cv2.cvtColor(userImage, cv2.COLOR_BGR2GRAY)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    claheAppliedUserImage = clahe.apply(greyImage)
    
    # defalt we're using
    thresh = cv2.threshold(greyImage, 0, 255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:1]

    ROI_number = 0
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(userImage, (x, y), (x + w, y + h), (36,255,12), 1)
        ROI = original[y:y+h, x:x+w]
        #cv.imwrite('ROI_{}.png'.format(ROI_number), ROI)
        #peri = cv2.arcLength(c, True)
        #approx = cv2.approxPolyDP(c, 0.015 * peri, True)

        if len(approx) == 4:
            cv2.drawContours(userImage,[c], 0, (36,255,12), 3)
            #transformed = perspective_transform(original, approx)
            #rotated = rotate_image(transformed, -90)
            #cv2.imwrite('ROI_{}.png'.format(ROI_number), rotated)
            #cv2.imshow('ROI_{}'.format(ROI_number), rotated)
            ROI_number += 1
        print("File is " + str(USERFILES[i]))
        plt.imshow(userImage),plt.show()
        print("ROI is:")
        plt.imshow(ROI),plt.show()
    
    cv2.waitKey()
    cv2.destroyAllWindows()
