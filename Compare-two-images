#!/usr/bin/env python3
import numpy as np
import cv2 as cv
import os
import time
import pathlib
import matplotlib.pyplot as plt
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askopenfilenames



"""
Loop over picture files in the current directory using 
different thresholding techniques provided by the user 
to find bounding boxes in images.
Output each image, showing the technique used.
"""
TECHNIQUE = ""
WORKINGDIR = os.getcwd()
RAISECONTRAST = 'false'
BLUR = 'false'

"""""
We'll take one file the the user provides first which will be the mystery chop mark
Then well ask the user to select a range of possible matches to compare it against for a match
"""""
USERFILE = ""
POSSIBLEMATCHES = []

def imageResizer(userImage, galleryImage):
    
    # get each pictures dimensions
    uh, uw, uc = userImage.shape
    gh, gw, gc = galleryImage.shape
    
    resizedUserImage = userImage
    resizedgalleryImage = galleryImage
    
    if ((uh*uw) < (gh*gw)): #user image is the larger
        dim = (gw, gh)
        resizedUserImage = cv.resize(userImage, dim, interpolation = cv.INTER_AREA)
        #plt.imshow(resizedUserImage),plt.show()
        #plt.imshow(galleryImage),plt.show()
        return resizedUserImage, galleryImage
    elif ((gh*gw) < (uh*uw)): #gallery image is the larger
        dim = (uw, uh)
        resizedGalleryImage = cv.resize(galleryImage, dim, interpolation = cv.INTER_AREA)
        #plt.imshow(userImage),plt.show()
        #plt.imshow(resizedGalleryImage),plt.show()
        return userImage, resizedGalleryImage
    #return None
    
        
def matchAndCompare(userImage, userText, galleryImage, galleryText):
    
    userPath, userFile = os.path.split(userText)
    galleryPath, galleryFile = os.path.split(galleryText)
                 
    """""
    # font 
    font = cv.FONT_HERSHEY_SIMPLEX
  
    # org 
    org = (10, 40) 
  
    # fontScale 
    fontScale = 1
   
    # Blue color in BGR 
    color = (0, 0, 0) 
  
    # Line thickness of 2 px 
    thickness = 2
    """""
    
    # Initiate SIFT detector
    sift=cv.SIFT_create()
    
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(userImage,None)
    kp2, des2 = sift.detectAndCompute(galleryImage,None)
    
    # BFMatcher with default params
    bf = cv.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)


    # Apply ratio test
    good = []
    percent = 0
    for m,n in matches:
        #if m.distance < 0.75*n.distance:
        if m.distance < 0.90*n.distance:
            good.append([m])
            a=len(good)
            percent=(a*100)/len(kp2)
            #print("{} % similarity".format(percent))
        #if percent >= 75.00:
            #print('Match Found')
            
    # Using cv2.putText() method 
    #userImage = cv.putText(userImage, userFile, org, font, fontScale, color, thickness, cv.LINE_AA)
    #galleryImage = cv.putText(galleryImage, galleryFile, org, font, fontScale, color, thickness, cv.LINE_AA)
    
    print("Your image:")
    
    img1 = cv.imread(userText)
    img2 = cv.imread(galleryText)
    
    plt.imshow(img1),plt.show()
    print("Offered match:")
    plt.imshow(img2),plt.show()
    
    roundedPercent = format(percent,".2f")
    
    if (float(roundedPercent)<=100):
        print("Results: " + userFile + " and " + galleryFile + " are {}% similar".format(roundedPercent))
        img3 = cv.drawMatchesKnn(userImage,kp1,galleryImage,kp2,good,None,flags=2)
        plt.imshow(img3),plt.show()
    elif (float(roundedPercent)>=100):
        print("A result has been hidden where the match was greater than 100%, which shouldn't happen. That was " + userFile + " and " + galleryFile + " which got a score of {}% similarity".format(roundedPercent))

input("Press enter to choose your unmatched file")
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
USERFILE = askopenfilename() # show an "Open" dialog box and return the path to the selected file    
print("Chosen file for matching is " + USERFILE)

input("Press enter agaion to choose your gallery list of possible template matches and I'll score them")
POSSIBLEMATCHES = askopenfilenames(initialdir=os.getcwd(), title="Select candidate matches")
for i in range(0, len(POSSIBLEMATCHES)):    
    print("Candidate match (" + str(i+1) + ") is " + POSSIBLEMATCHES[i])
        
for i in range(0, len(POSSIBLEMATCHES)):

    galleryImage = cv.imread(POSSIBLEMATCHES[i])
    userImage = cv.imread(USERFILE)
    
    userImage, galleryImage = imageResizer(userImage, galleryImage)
        
    greyScaledUserImage = cv.cvtColor(userImage, cv.COLOR_BGR2GRAY)
    greyScaledGalleryImage = cv.cvtColor(galleryImage, cv.COLOR_BGR2GRAY)
    
    # create a CLAHE object (Arguments are optional).
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    claheAppliedUserImage = clahe.apply(greyScaledUserImage)
    claheAppliedGalleryImage = clahe.apply(greyScaledGalleryImage)
    
    #plt.imshow(claheAppliedUserImage,cmap="gray"),plt.show()
    #plt.imshow(claheAppliedGalleryImage,cmap="gray"),plt.show()
    
    #matchAndCompare(greyScaledUserImage, USERFILE, greyScaledGalleryImage, str(POSSIBLEMATCHES[i]))
    matchAndCompare(claheAppliedUserImage, USERFILE, claheAppliedGalleryImage, str(POSSIBLEMATCHES[i]))
    
    
cv.waitKey(0)
cv.destroyAllWindows()
