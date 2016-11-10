import cv2
import numpy as np
from munkres import Munkres as mks
from matplotlib import pyplot as plt
import pandas as pd


def TrackExtraction(filename,dataDir):
    video = dataDir + "\\" + filename
    videoReader = cv2.VideoCapture(video)

    tracks = pd.DataFrame(columns=('objectID', 'frameNo', 'coordinates'))


    # Some parameters #
    objectId = 1
    countObject = 1
    frameNo = 0
    prev = (0,0)       # store previous coordinates


    # Kalman Filter #
    kalman = cv2.KalmanFilter(4, 2)
    kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
    kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
    kalman.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)

    # initiation #

    backgroundSubMOG2 = cv2.createBackgroundSubtractorMOG2(0,0,False)

    backgroundSubKNN = cv2.createBackgroundSubtractorKNN()



    #******************************************************************************#
    #                                  Sub-Functions                               #
    #******************************************************************************#
    def detectObjects(frame,objectId):
        coordinates = []
        tp = []
        diameter = 0
        # Detect Foreground #


        fgmask2 = backgroundSubMOG2.apply(frame)
        #fgmask2 = backgroundSubKNN.apply(frame)


        # Morphological Operations #
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
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
        predictedCentroids = np.zeros((2, 1), np.float32)
        for i in range(len(tracks)):
            if coordinates == []:
                coordinates = tracks['coordinates']  # accessing bbox in tracks array
            print(coordinates)


            #Conversion from float64 to float32
            tempCoordinates = list(coordinates)
            tempCoordinatesX = float(tempCoordinates[0])
            tempCoordinatesY = float(tempCoordinates[1])
            tempCoordinates = np.array((2, 1), np.float32) # put float here because kalman.correct only accepts float32
            tempCoordinates[0] = tempCoordinatesX
            tempCoordinates[1] = tempCoordinatesY

            #Kalman's showtime

            kalman.correct(tempCoordinates)
            predictedCentroids = kalman.predict()
            predictedCentroids = list(predictedCentroids)


            #Conversion from float to int
            predictedCentroids[2] = int( predictedCentroids[2] )  # width/height
            predictedCentroids[3] = int( predictedCentroids[3] )  # width/height
            predictedCentroids[0] = int( predictedCentroids[0] )  # x
            predictedCentroids[1] = int( predictedCentroids[1] )  # y

            #tracks.loc[i] = ( predictedCentroids[0], predictedCentroids[1] )

            return predictedCentroids


    def detectionToTrackAssignment():
        nTracks = len(tracks)


    def opticFlow():
        print("Nothing is here")



    while (videoReader.isOpened()):
        ret, frame = videoReader.read()        # equivalent to obj.reader.step()
        testbox = []
        frameNo = frameNo + 1


        fgmask2,coordinates,diameter,tp = detectObjects(frame,objectId)


        if coordinates == []:
            coordinates = tuple([0,0])




        tracks.loc[countObject] = ( objectId, frameNo, ( coordinates[0], coordinates[1] ) )
        countObject = countObject + 1
        predictedCentroids = predictNewLocationsOfTracks(prev)


        # Operations below are all for kalman output
        box1 = (predictedCentroids[0], predictedCentroids[2])
        box2 = (predictedCentroids[1], predictedCentroids[3])
        box1 = tuple(predictedCentroids[0:2])
        box2 = tuple(predictedCentroids[2:4])
        testbox1 = box1[0] - box2[0]
        testbox2 = box1[1] - box2[1]
        testbox = (testbox1, testbox2)

        diameter = 50  # temp
        #testbox = (10,10)
        cv2.circle( frame, testbox, diameter, (0, 255, 0) )
        cv2.circle( frame, coordinates, diameter, (255, 0, 0) )

        #update prev to previous coordinates
        if coordinates != (0,0):
            prev = coordinates
        else:
            prev = testbox
        print('Frame #', frameNo, ' ', coordinates,' ','Kalman Prediction :',testbox)

        # Create display window
        cv2.namedWindow('TrackExtraction', cv2.WINDOW_NORMAL)
        cv2.imshow('TrackExtraction',fgmask2)

        # waitKey is to control the speed of video, ord is to enable quit() using character
        if cv2.waitKey(15) & 0xFF == ord('q'):

            break


TrackExtraction('czech.avi','E:\Documents\MMU Studies\Python Scripts')
