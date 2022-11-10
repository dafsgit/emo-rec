# Author: Dafne Vania Peña Cortés
# This program converts a 20 fps video to 10 fps, removing every other frame
# so the resulting video has the same lenght as the original.

import os
import cv2
from pathlib import Path


def reduceFrames(vidPath, vidwExt, everyNthFrame):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    cap = cv2.VideoCapture(vidPath + vidwExt)
    fps = int(cap.get(cv2.CAP_PROP_FPS)) # same lenght of video with different fps
    width = int(cap.get(3))
    height = int(cap.get(4))
    out = cv2.VideoWriter(vidPath + "Re_" + vidwExt, fourcc, int(fps/everyNthFrame), (width, height))
    count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            out.write(frame)
            count += everyNthFrame
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)
        else:
            break
    cap.release()
    out.release()

vidPath = "C:/Users/dafne/Downloads/face_recordings/"
# vidName = "Face_Massimiliano_2022-10-25-10_01_14"
vidExt = ".mp4"

files = Path(vidPath).glob('Face_*.mp4')
for file in files:
    vidName = os.path.basename(file)[:-4]
    reduceFrames(vidPath, vidName + vidExt, 2)
    print(vidName)