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
        fgmask2 = backgroundSubKNN.apply(frame)     #mask
        #kernel = numpy.ones((5, 5))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
        #------------------------- Remove Holes-------------------------#
        fgmask2 = cv2.morphologyEx(fgmask2,cv2.MORPH_OPEN,kernel)
        fgmask2 = cv2.morphologyEx(fgmask2,cv2.MORPH_CLOSE,kernel)
        #---------------------------------------------------------------#

        #-------------------------Blob Analysis-------------------------#
        detector = cv2.SimpleBlobDetector_create()
        keypoints = detector.detect(fgmask2)
        #---------------------------------------------------------------#
        cv2.imshow('backgroundSubKNN',fgmask2)
        # waitKey is to control the speed of video, ord is to enable quit() using character
        if cv2.waitKey(1) & 0xFF == ord('q'):
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
