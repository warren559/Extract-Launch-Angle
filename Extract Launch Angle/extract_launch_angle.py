"""" The following script allows you to open a window and move through a video frame by frame - using a start and end slider
    The user can use the start slider to move to the start frame , then left click on any point in the frame and
     x and y pixel coordinates will be displayed. These values will we stored as start coordinates
    Thereafter, the user can then use the end slider to move to a end/last frame and right click on any point in the frame and
     x and y pixel coordinates will be displayed. These values will we stored as end coordinates
"""

import cv2
import numpy as np
import math
from tkinter import Tk
from tkinter.filedialog import askopenfilename

#This variable we use to store the pixel location
refPt = []

def click_event(event, x, y, flags, param):
    """ When the user clicks on the image the x and y coordinate gets displayed and stored"""
    global strXY_first, strXY_second

    if event == cv2.EVENT_LBUTTONDOWN: # left click to get the x and y coordinates of the launch (start) position
        print("Start co-ordinates: " + str(x) + "," + str(y))
        refPt.append([x,y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY_first = str(x)+", "+str(y) # x and y co-ordinates of start point
        cv2.putText(img, strXY_first, (x,y), font, 0.5, (0,255,0), 2) # display x and y font on the screen
        cv2.imshow("mywindow", img)

    if event == cv2.EVENT_RBUTTONDOWN: # right click to get the x and y coordinates of the (end) position
        print("End co-ordinates: " + str(x) + "," + str(y))    
        refPt.append([x,y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY_second = str(x)+", "+str(y) # x and y co-ordinates of start point        
        cv2.putText(img, strXY_second, (x,y), font, 0.5, (0,255,0), 2)
        cv2.imshow("mywindow", img)

def onChange(trackbarValue):
    """ Displays each frame in the window as user uses the slider """
    global img
    print("activated")
    cap.set(cv2.CAP_PROP_POS_FRAMES,trackbarValue) # cv2.CAP_PROP_POS_FRAMES - frame to be decoded
    err,img = cap.read()
    cv2.imshow("mywindow", img)
    cv2.setMouseCallback("mywindow", click_event)
    pass

#This variable we use to store the pixel location
refPt_2 = []

Tk().withdraw() 

# open filedialog, user open the video file 
filename = askopenfilename()
cap = cv2.VideoCapture(filename) # VideoCapture object
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # amount of frames in the video
cv2.namedWindow('mywindow') # window name 
cv2.createTrackbar( 'start', 'mywindow', 0, length, onChange) # start slider
cv2.createTrackbar( 'end'  , 'mywindow', length, length, onChange) # end slider
onChange(0)
cv2.waitKey()

start = cv2.getTrackbarPos('start','mywindow')
end   = cv2.getTrackbarPos('end','mywindow')

cap.set(cv2.CAP_PROP_POS_FRAMES,start)

while cap.isOpened():
    err,img = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) >= end:
        break
    cv2.imshow("mywindow", img)
    k = cv2.waitKey(10) & 0xff
    if k==27:
        break

    #calling the mouse click event
    cv2.setMouseCallback("mywindow", click_event)

first_pos = strXY_first.split(", ")
second_pos = strXY_second.split(", ")
pix_length = int(second_pos[0]) - int(first_pos[0])
conversion = 2.135 / pix_length
print("Conversion coefficient")
print(conversion)
cv2.waitKey(0)
cv2.destroyAllWindows()
rad = math.atan2((int(first_pos[1]) - int(second_pos[1])), (int(second_pos[0]) - int(first_pos[0]) ))
deg = math.degrees(rad)
print("deg")
print(deg)

