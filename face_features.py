# Author: Dafne Vania Peña Cortés
# This program produces a dictionary with every significant part of a PBL
# containing the 68 landmarks of every face per frame per student.

import os
from pathlib import Path
import cv2
import dlib
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


it = {"I1": [146, 164], "F1": [181, 187],
      "R0": [200, 228], "F2": [238, 243],
      "I2": [280, 290]}
vidFinSec = 362
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


# dimensions: n-frames x n-faces x 68 tuples
def getLandmarksPerFrame(vid):
    cap = cv2.VideoCapture(vid)
    if (cap.isOpened()== False):
        print("Error opening video file")
    result = []
    while(cap.isOpened()):
        ret, fr = cap.read()
        if ret == True:
            gray = cv2.cvtColor(src=fr, code=cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            frame = []
            for face in faces:
                x1 = face.left()
                y1 = face.top()
                # x2 = face.right()
                # y2 = face.bottom()
                # cv2.rectangle(img=fr, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=4)
                landmarks = predictor(image=gray, box=face)
                face = []
                for n in range(0, 68):
                    x = landmarks.part(n).x # with respect to the whole window, not the face
                    y = landmarks.part(n).y
                    # cv2.circle(img=fr, center=(x, y), radius=2, color=(0, 255, 0), thickness=-1)
                    xFaceFrame = x-x1 # with top left corner of face as origin
                    yFaceFrame = y-y1
                    face.append((xFaceFrame, yFaceFrame))
                frame.append(face)
            result.append(frame)
            # cv2.imshow('Face feature detection', fr)
        else:
            break
    cap.release()
    return result


vidPath = "C:/Users/dafne/Downloads/face_recordings/"
# vidName = "Re_Face_Massimiliano_2022-10-25-10_01_14"
vidExt = ".mp4"

stIDs = []
students = Path(vidPath).glob('Re_Face_*.mp4')
for i, st in enumerate(students):
    stName = os.path.basename(st)[:-4]
    stIDs.append({
        'ID': i,
        'Student': stName.split("_")[2]
    })
# print(stIDs)

# dirs = ["F2"]
dirs = it.keys()
samples = {key:[] for key in dirs}
for part in dirs:
    files = Path(vidPath + part + "/").glob('Re_Face_*.mp4')
    print("Part " + part)
    for file in files:
        vidName = os.path.basename(file)[:-4]
        # landmarks per frame for every video in the part dir
        print('.', end='')
        samples[part].append(getLandmarksPerFrame(str(file)))
    print("")
    for i, result in enumerate(samples[part]):
        # result dim = n-frames x n-faces x 68 tuples
        print("    Subject " + str(i) + " has ", end='')
        print(str(len(result)) + " frames each with ", end='')
        # 10th frame must have points already (at 1 sec)
        print(str(len(result[10])) + " faces each with ", end='') 
        print(str(len(result[10][0])) + " points.")

cv2.destroyAllWindows()