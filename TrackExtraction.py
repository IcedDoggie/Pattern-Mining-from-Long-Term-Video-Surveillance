import cv2
import numpy as np
from matplotlib import pyplot as plt

class tracksList:
    def __init__(self):
        self.id = []
        self.frameNo = []
        self.bbox = []
        self.kalmanFilter = []
        age = []
        totalVisibleCount = []
        consecutiveInvisibleCount = []


def TrackExtraction(filename,dataDir):
    video = dataDir + "\\" + filename
    videoReader = cv2.VideoCapture(video)
    tracks = tracksList()

    # Kalman Filter #
    kalman = cv2.KalmanFilter(4, 2)
    kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
    kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
    kalman.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)

    # initiation #
    backgroundSubMOG = cv2.createBackgroundSubtractorMOG2()
    backgroundSubKNN = cv2.createBackgroundSubtractorKNN()

    #******************************************************************************#
    #                                  Sub-Functions                               #
    #******************************************************************************#
    def detectObjects(frame):


        # Detect Foreground #
        #fgmask = backgroundSubMOG.apply(frame)
        fgmask2 = backgroundSubMOG.apply(frame)

        # Morphological Operations #
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        fgmask2 = cv2.morphologyEx(fgmask2, cv2.MORPH_OPEN, kernel)
        fgmask2 = cv2.morphologyEx(fgmask2, cv2.MORPH_CLOSE, kernel)

        # Blob Analysis #
        detector = cv2.SimpleBlobDetector_create()
        keypoints = detector.detect(fgmask2)

        # Return Values #
        return fgmask2;

    while (videoReader.isOpened()):
        ret, frame = videoReader.read()

        fgmask2 = detectObjects(frame)
        cv2.imshow('backgroundSubKNN', fgmask2)
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
