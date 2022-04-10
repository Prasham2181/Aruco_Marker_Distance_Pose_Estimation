import cv2
import imutils
import time
from imutils.video import VideoStream


vs = VideoStream(src=0).start()

#
# ARUCO_DICT = {
#     "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
#     "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
#     "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
#     "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
#     "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
#     "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
#     "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
#     "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
#     "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
#     "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
#     "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
#     "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
#     "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
#     "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
#     "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
#     "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
#     "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
#     "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
#     "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
#     "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
#     "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
# }
# arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args['type']])
# arucoParams = cv2.aruco.DetectorParameters_create()
arucoParams = cv2.aruco.DetectorParameters_create()
arucoParams_2 = cv2.aruco.DetectorParameters_create()

arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_250)
arucoDict_2 = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250)


CACHED_PTS = None
CACHED_IDS = None
Line_Pts = None
measure = None

CACHED_PTS_2 = None
CACHED_IDS_2 = None
Line_Pts_2 = None
measure_2 = None
while True:
    Dist = []
    image = vs.read()
    image = imutils.resize(image, width=800)
    corners, ids, rejected= cv2.aruco.detectMarkers( image, arucoDict, parameters=arucoParams)

    if len(corners) <= 0:
        if CACHED_PTS is not None:
            corners = CACHED_PTS
    if len(corners) > 0:
        CACHED_PTS = corners
        if ids is not None:
           ids = ids.flatten()
           CACHED_IDS = ids
        else:
           if CACHED_IDS is not None:
              ids = CACHED_IDS
        if len(corners) < 2:
           if len(CACHED_PTS) >= 2:
              corners = CACHED_PTS
        for (markerCorner, markerId) in zip(corners, ids):
            #print("[INFO] Marker detected")
            corners_abcd = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners_abcd
            topRightPoint = (int(topRight[0]), int(topRight[1]))
            topLeftPoint = (int(topLeft[0]), int(topLeft[1]))
            bottomRightPoint = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeftPoint = (int(bottomLeft[0]), int(bottomLeft[1]))
            cv2.line(image, topLeftPoint, topRightPoint, (0, 255, 0), 2)
            cv2.line(image, topRightPoint, bottomRightPoint, (0, 255, 0), 2)
            cv2.line(image, bottomRightPoint, bottomLeftPoint, (0, 255, 0), 2)
            cv2.line(image, bottomLeftPoint, topLeftPoint, (0, 255, 0), 2)
            cX = int((topLeft[0] + bottomRight[0])//2)
            cY = int((topLeft[1] + bottomRight[1])//2)

            measure = abs(3.5 / (topLeft[0] - cX))
            cv2.circle(image, (cX, cY), 4, (255, 0, 0), -1)
            cv2.putText(image, str(
                int(markerId)), (int(topLeft[0] - 10), int(topLeft[1] - 10)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
            Dist.append((cX, cY))
            # print(arucoDict)
            if len(Dist) == 0:
                if Line_Pts is not None:
                    Dist = Line_Pts
            if len(Dist) == 2:
                Line_Pts = Dist
            if len(Dist) == 2:
                cv2.line(image, Dist[0], Dist[1], (255, 0, 255), 2)
                ed = ((Dist[0][0] - Dist[1][0]) ** 2 +
                      ((Dist[0][1] - Dist[1][1]) ** 2)) ** (0.5)
                cv2.putText(image, str(int(measure * (ed))) + "inch", (int(300), int(300)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
                print("ed", ed * measure)

    Dist_2 = []
    # image = vs.read()
    # image = imutils.resize(image, width=800)
    corners_2, ids_2, rejected_2 = cv2.aruco.detectMarkers(image, arucoDict_2, parameters=arucoParams_2)
    if len(corners_2) <= 0:
        if CACHED_PTS_2 is not None:
            corners_2 = CACHED_PTS_2
    if len(corners_2) > 0:
        CACHED_PTS_2 = corners_2
        if ids_2 is not None:
            ids_2 = ids_2.flatten()
            CACHED_IDS_2 = ids_2
        else:
            if CACHED_IDS_2 is not None:
                ids_2 = CACHED_IDS_2
        if len(corners_2) < 2:
            if len(CACHED_PTS_2) >= 2:
                corners = CACHED_PTS
        for (markerCorner_2, markerId_2) in zip(corners_2, ids_2):
            # print("[INFO] Marker detected")
            corners_abcd_2 = markerCorner_2.reshape((4, 2))
            (topLeft_2, topRight_2, bottomRight_2, bottomLeft_2) = corners_abcd_2
            topRightPoint_2 = (int(topRight_2[0]), int(topRight_2[1]))
            topLeftPoint_2 = (int(topLeft_2[0]), int(topLeft_2[1]))
            bottomRightPoint_2 = (int(bottomRight_2[0]), int(bottomRight_2[1]))
            bottomLeftPoint_2 = (int(bottomLeft_2[0]), int(bottomLeft_2[1]))
            cv2.line(image, topLeftPoint_2, topRightPoint_2, (0, 255, 0), 2)
            cv2.line(image, topRightPoint_2, bottomRightPoint_2, (0, 255, 0), 2)
            cv2.line(image, bottomRightPoint_2, bottomLeftPoint_2, (0, 255, 0), 2)
            cv2.line(image, bottomLeftPoint_2, topLeftPoint_2, (0, 255, 0), 2)
            cX_2 = int((topLeft_2[0] + bottomRight_2[0]) // 2)
            cY_2 = int((topLeft_2[1] + bottomRight_2[1]) // 2)

            measure_2 = abs(3.5 / (topLeft_2[0] - cX_2))
            cv2.circle(image, (cX_2, cY_2), 4, (255, 0, 0), -1)
            cv2.putText(image, str(
                int(markerId_2)), (int(topLeft_2[0] - 10), int(topLeft_2[1] - 10)), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
            Dist_2.append((cX_2, cY_2))
            # print(arucoDict)
            if len(Dist_2) == 0:
                if Line_Pts_2 is not None:
                    Dist_2 = Line_Pts_2
            if len(Dist_2) == 2:
                Line_Pts_2 = Dist_2
            if len(Dist_2) == 2:
                cv2.line(image, Dist_2[0], Dist_2[1], (255, 0, 255), 2)
                ed_2 = ((Dist_2[0][0] - Dist_2[1][0]) ** 2 +
                      ((Dist_2[0][1] - Dist_2[1][1]) ** 2)) ** (0.5)
                cv2.putText(image, str(int(measure_2 * (ed_2))) + "inch", (int(300), int(300)), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (0, 0, 255))
                print("ed_2", ed_2 * measure_2)
        print((ed * measure)-(ed_2 * measure_2))
    cv2.imshow("[INFO] marker detected", image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
cv2.destroyAllWindows()
vs.stop()