import cv2
import numpy
import tkinter

def TrackExtraction(filename,dataDir):
    video = dataDir + "\\" + filename
    videoReader = cv2.VideoCapture(video)
    





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
