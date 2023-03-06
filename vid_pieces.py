# Author: Dafne Vania Peña Cortés
# This program divides a group of videos into smaller
# pieces limited by the seconds in "it" array.
# [Step 2]

import os
from pathlib import Path
import cv2
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


it = {"I1": [146, 164], "F1": [181, 187],
      "R0": [200, 228], "F2": [238, 243],
      "I2": [280, 290]}
vidFinSec = 362

def breakIntoPieces(vidPath, vidwExt):
    cap = cv2.VideoCapture(vidPath + vidwExt)
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    seconds = round(frames / fps)
    cap.release()
    if seconds > vidFinSec:
        for part in it:
            startTime = it[part][0]
            endTime = it[part][1]
            ffmpeg_extract_subclip(vidPath + vidwExt, startTime, endTime, targetname = vidPath + str(part) + "/" + vidwExt)
    else:
        print("The recording is shorter than the PBL:")


vidPath = "C:/Users/dafne/Downloads/face_recordings/"
# vidName = "Re_Face_Massimiliano_2022-10-25-10_01_14"
vidExt = ".mp4"

files = Path(vidPath).glob('Re_Face_*.mp4')
for file in files:
    vidName = os.path.basename(file)[:-4]
    breakIntoPieces(vidPath, vidName + vidExt)
    print(vidName)