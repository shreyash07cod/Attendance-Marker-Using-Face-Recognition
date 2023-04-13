import os
import pickle

import bbox as bbox
import cv2
import cvzone as cvzone
import face_recognition
import numpy as np

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Graphics
imageBackground = cv2.imread('Resources/background.png')

# Importing the mode images into the list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
    # print(imgModeList)

# print(len(imgModeList))
# print(modePathList)


# Load the encoding file
print("Loading Encoded File.....")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encoded File Loaded")

while True:
    success, img = cap.read()

    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgSmall)
    encodeCurFrame = face_recognition.face_encodings(imgSmall, faceCurFrame)

    # height and width points
    imageBackground[162:162 + 480, 55:55 + 640] = img
    imageBackground[44:44 + 633, 808:808 + 414] = imgModeList[3]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print("matches", matches)
        print("faceDis", faceDis)

        matchIndex = np.argmin(faceDis)
        print("Match Index", matchIndex)

        if matches[matchIndex]:
            print("KNown Face Detected")
            print(studentIds[matchIndex])
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            bbox = 55+x1, 162+y1, x2-x1, y2-y1
            imageBackground = cvzone.cornerRect(imageBackground, bbox, rt=0)


    # ncv2.imshow("Webcam", img)
    cv2.imshow("Face Detection", imageBackground)
    cv2.waitKey(1)
