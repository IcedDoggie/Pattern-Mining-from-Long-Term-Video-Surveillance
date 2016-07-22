import cv2
import numpy as np
from munkres import Munkres as mks
from matplotlib import pyplot as plt


def TrackExtraction(filename,dataDir):
    video = dataDir + "\\" + filename
    videoReader = cv2.VideoCapture(video)
    tracks = np.array([], dtype=[('id','i8'),('frameNo','i8'),('bbox','f4'),('kalmanFilter','f4'),('age','i8'),
                                 ('totalVisibleCount','i8'),('consecutiveInvisibleCount','i8')])

    # Some parameters by Mehdi #
    nextId = 1
    trackInfo = []
    count = 1
    frameNo = 0

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
        coordinates = []
        diameter = 0
        # Detect Foreground #

        fgmask2 = backgroundSubMOG.apply(frame)
        #fgmask2 = backgroundSubKNN.apply(frame)

        # Morphological Operations #
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        fgmask2 = cv2.morphologyEx(fgmask2, cv2.MORPH_OPEN, kernel)
        fgmask2 = cv2.morphologyEx(fgmask2, cv2.MORPH_CLOSE, (15, 15))

        # Blob Analysis #
        detector = cv2.SimpleBlobDetector_create()
        keypoints = detector.detect(fgmask2)
        print(len(keypoints))
        if keypoints != []:
            coordinates = keypoints[0].pt
            diameter = keypoints[0].size
            objectID = keypoints[0].class_id



        # Return Values #
        return fgmask2,coordinates,diameter

    def predictNewLocationsOfTracks():
        for i in range(len(tracks)):

            bbox = tracks['bbox'[i]]  #accessing bbox in tracks array

            predictedCentroid = kalman.predict(tracks[i])
            predictedCentroid = predictedCentroid - bbox[:1, 3:4] / 2

            tracks[i].bbox = [ predictedCentroid, bbox[:1, 3:4] ]
            tracks[i].frameNo = frameNo

    def detectionToTrackAssignment():
        nTracks = len(tracks)

    # def updateAssignedTracks():
    #
    # def updateUnassignedTracks():
    #
    # def deleteLostTracks():
    #
    # def createNewTracks():
    #
    # def trimTrackingResults():

    def drawBoundingBox(frame,coordinates, diameter):
        #test only
        
        #test ends
        radius = int(diameter/2)
        coordinates = list(coordinates)
        coordinates[0] = int(coordinates[0])
        coordinates[1] = int(coordinates[1])
        coordinates = tuple(coordinates)

        return coordinates, radius




    while (videoReader.isOpened()):
        ret, frame = videoReader.read()        # equivalent to obj.reader.step()

        frameNo = frameNo + 1

        fgmask2,coordinates,diameter = detectObjects(frame)

        if coordinates != []:
            coordinates, diameter = drawBoundingBox(fgmask2,coordinates,diameter)
            abc = cv2.circle(fgmask2, coordinates, diameter, (255, 0, 0))
        print('Frame #', frameNo, ' ', coordinates)

        #if not tracks:
        predictNewLocationsOfTracks()

        detectionToTrackAssignment()

        cv2.imshow('backgroundSub', fgmask2)


        # waitKey is to control the speed of video, ord is to enable quit() using character
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break



TrackExtraction('czech.avi','E:\Documents\MMU Studies\Python Scripts')
