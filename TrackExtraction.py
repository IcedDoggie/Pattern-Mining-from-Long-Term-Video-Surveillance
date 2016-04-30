import cv2
import numpy
import tkinter
from matplotlib import pyplot as plt

def TrackExtraction(filename,dataDir):
    video = dataDir + "\\" + filename
    videoReader = cv2.VideoCapture(video)
    #backgroundSubMOG = cv2.createBackgroundSubtractorMOG2()
    backgroundSubKNN = cv2.createBackgroundSubtractorKNN()

    while (videoReader.isOpened()):
        ret, frame = videoReader.read()
        #fgmask = backgroundSubMOG.apply(frame)
        fgmask2 = backgroundSubKNN.apply(frame)
        kernel = numpy.ones((5, 5))
        #------------------------- Dilation-----------------------------#
        dilation = cv2.dilate(fgmask2,kernel,iterations=1)
        #---------------------------------------------------------------#
        """
        #opening
        opening = cv2.morphologyEx(fgmask2,cv2.MORPH_OPEN,kernel)

        # Erosion
        erosion = cv2.erode(dilation,kernel,iterations=1)
        """

        #-------------------------Blob Analysis-------------------------#
        detector = cv2.SimpleBlobDetector_create()
        keypoints = detector.detect(dilation)
        #---------------------------------------------------------------#
        cv2.imshow('backgroundSubKNN',dilation)
        # waitKey is to control the speed of video, ord is to enable quit() using character
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break





def playVideo(video):
    videoReader = cv2.VideoCapture(video)

    while(videoReader.isOpened()):
        ret,frame = videoReader.read()
        cv2.imshow('Video',frame)
        #waitKey is to control the speed of video, ord is to enable quit() using character
        if cv2.waitKey(1) & 0xFF == ord('q') :
            break
    cv2.destroyAllWindows()




TrackExtraction('czech.avi','E:\Documents\MMU Studies\Python Scripts')
