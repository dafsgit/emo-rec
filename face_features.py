# Author: Dafne Vania Peña Cortés
# This program produces a dictionary with every significant part of a PBL
# containing the 68 landmarks of every face per frame per student.
# [Not used for the final program]

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
    neutral = []
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
            if len(result) == 11:
                neutral = frame
                # while True:
                #     cv2.imshow('Face feature detection', fr)
                #     if cv2.waitKey(delay=1) == 27:
                #         return
        else:
            break
    cap.release()
    return [neutral, result]


def clean(students):
    for s in students:
        rem = []
        for j, frame in enumerate(s):
            if len(frame) < 1:
                rem.append(j)
        if len(rem) > 0:
            for k in reversed(rem):
                del s[k]


def getDiff(students, neuFacesPart):
    diffPart = []
    for i, student in enumerate(students):
        dRes = []
        for j, frame in enumerate(student):
            dFr = []
            if len(frame) > 0:
                for k, face in enumerate(neuFacesPart[i]):
                    dFa = []
                    for l, (xn, yn) in enumerate(face):
                        frCoord = frame[k][l]
                        xD = frCoord[0] - xn
                        yD = frCoord[1] - yn
                        dFa.append((xD, yD))
                    dFr.append(dFa)
            dRes.append(dFr)
        diffPart.append(dRes)
    return diffPart


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

# files = Path(vidPath).glob('Re_Face_*.mp4')
# for file in files:
#     vidName = os.path.basename(file)[:-4]
#     # landmarks per frame for every video in the part dir
#     print('.', end='')
#     getLandmarksPerFrame(str(file))

# dirs = ["F1"]
dirs = it.keys()
samples = {key:[] for key in dirs}
neuFaces = {key:[] for key in dirs}
differences = {key:[] for key in dirs}

for part in dirs:
    files = Path(vidPath + part + "/").glob('Re_Face_*.mp4')
    print("Part " + part)
    for file in files:
        # vidName = os.path.basename(file)[:-4]
        # landmarks per frame per video in the part dir
        print('.', end='')
        neu, res = getLandmarksPerFrame(str(file))
        neuFaces[part].append(neu)
        samples[part].append(res)
    print("")
    # for i, result in enumerate(samples[part]):
    #     # result dimentions = n-frames x n-faces x 68 tuples
    #     print("    Subject " + str(i) + " has ", end='')
    #     print(str(len(result)) + " frames each with ", end='')
    #     print(str(len(result[10])) + " faces each with ", end='') 
    #     print(str(len(result[10][0])) + " points.")

for part in dirs:
    differences[part] = getDiff(samples[part], neuFaces[part])



cv2.destroyAllWindows()