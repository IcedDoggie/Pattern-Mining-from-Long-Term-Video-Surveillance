import cv2
import numpy as np
from munkres import Munkres as mks
from matplotlib import pyplot as plt
import pandas as pd


def TrackExtraction(filename,dataDir):
    video = dataDir + "\\" + filename
    videoReader = cv2.VideoCapture(video)

    tracks = pd.DataFrame(columns=('objectID', 'frameNo', 'coordinates'))

    # Some parameters by Mehdi #
    objectId = 1
    countObject = 1
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
    def detectObjects(frame,objectId):
        coordinates = []
        tp = []
        diameter = 0
        # Detect Foreground #

        # fgmask2 = backgroundSubMOG.apply(frame)
        fgmask2 = backgroundSubKNN.apply(frame)

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
            #Conversion from float to int on coordinates
            coordinates = list(coordinates)
            coordinates[0] = int(coordinates[0])
            coordinates[1] = int(coordinates[1])
            coordinates = tuple(coordinates)

            diameter = keypoints[0].size

        # Return Values #
        return fgmask2,coordinates,diameter,tp

    def predictNewLocationsOfTracks(coordinates):
        for i in range(len(tracks)):
            coordinates = tracks['coordinates']  # accessing bbox in tracks array
            tempCoordinates = list(coordinates)
            tempCoordinatesX = float(tempCoordinates[i][0])
            tempCoordinatesY = float(tempCoordinates[i][1])
            tempCoordinates = np.array((2, 1), np.float32)
            tempCoordinates[0] = tempCoordinatesX
            tempCoordinates[1] = tempCoordinatesY

            kalman.correct(tempCoordinates)
            predictedCentroid = kalman.predict()

            return predictedCentroid


    # def detectionToTrackAssignment():
    #     nTracks = len(tracks)
    #
    # # def updateAssignedTracks():
    # #
    # # def updateUnassignedTracks():
    # #
    # # def deleteLostTracks():
    # #
    # # def createNewTracks():
    # #
    # # def trimTrackingResults():

    def drawBoundingBox(frame,coordinates, diameter):
        radius = int(diameter/2) *10

        return coordinates, radius


    while (videoReader.isOpened()):
        ret, frame = videoReader.read()        # equivalent to obj.reader.step()

        frameNo = frameNo + 1

        fgmask2,coordinates,diameter,tp = detectObjects(frame,objectId)

        if coordinates != []:
            coordinates, diameter = drawBoundingBox(fgmask2,coordinates,diameter)
            tracks.loc[countObject] = (objectId, frameNo, (coordinates[0], coordinates[1]))
            countObject = countObject + 1
            predictedCentroids = predictNewLocationsOfTracks(coordinates)
            #tracks.loc[countObject] = (objectId, frameNo, )
            cv2.circle( fgmask2, coordinates, diameter, (255, 0, 0) )
            cv2.circle( fgmask2, predictedCentroids, diameter, (0,255,0) )
        print('Frame #', frameNo, ' ', coordinates,' ','TP :',tp)
        cv2.imshow('backgroundSub', fgmask2)

        #if not tracks:
        # predictNewLocationsOfTracks()

        # detectionToTrackAssignment()





        # waitKey is to control the speed of video, ord is to enable quit() using character
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break



TrackExtraction('czech.avi','E:\Documents\MMU Studies\Python Scripts')
