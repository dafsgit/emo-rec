# Author: Dafne Vania Peña Cortés
# This program converts a video in images and saves the frames
# inside the indicated folder.
# [Step 3]

import os
import cv2
import dlib
from pathlib import Path

it = {"I1": [146, 164], "F1": [181, 187],
      "R0": [200, 228], "F2": [238, 243],
      "I2": [280, 290]}
vidFinSec = 362
detector = dlib.get_frontal_face_detector()


# dimensions: n-frames
def saveFrames(imgPath, imgExt, vidPath, vidName, vidExt):
    cap = cv2.VideoCapture(vidPath + vidName + vidExt)
    if (cap.isOpened()== False):
        print("Error opening video file")
    count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            if(len(faces) > 0):
                startCol = faces[0].left()
                startRow = faces[0].top()
                endCol = faces[0].right()
                endRow = faces[0].bottom()
                cv2.imwrite(imgPath + vidName + "_" + str(count).zfill(3) + imgExt, gray[startRow:endRow, startCol:endCol])
                count += 1
            # if count == 15:
            #     break
        else:
            break
    cap.release()


vp = "C:/Users/dafne/Downloads/face_recordings/"
# vn = "Re_Face_Massimiliano_2022-10-25-10_01_14"
ve = ".mp4"
ip = "C:/Users/dafne/Downloads/img_face_recordings/"
ie = ".jpeg"

stIDs = []
students = Path(vp).glob('Re_Face_*.mp4')
for i, st in enumerate(students):
    stName = os.path.basename(st)[:-4]
    stIDs.append({
        'ID': i,
        'Student': stName.split("_")[2]
    })
# print(stIDs)

# dirs = ["F1"]
dirs = it.keys()

for part in dirs:
    vidPathPart = vp + part + "/"
    imgPathPart = ip + part + "/"
    files = Path(vidPathPart).glob('Re_Face_*.mp4')
    print("Part " + part)
    for file in files:
        vn = os.path.basename(file)[:-4]
        # frames per video in the part dir
        print('.', end='')
        saveFrames(imgPathPart, ie, vidPathPart, vn, ve)
    print("")