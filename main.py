import cv2
import time
import numpy as np
import handTrackingModule as htm
import math
############################## for mac ##############################

import osascript

############################## for mac ##############################



############################ for windows ############################

#from ctypes import cast, POINTER
#from comtypes import CLSCTX_ALL
#from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

############################ for windows ############################


wCam, hCam = 640, 480

cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handTracker(detectionCon = 0.7)

############################ for windows ############################

#devices = AudioUtilities.GetSpeakers()
#interface = devices.Activate(
#    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
#volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
#volRange = volume.GetVolumeRange()
#minVol = volRange[0]
#maxVol = volRange[1]

############################ for windows ############################

while True:
    success, img = cap.read()
    img = detector.handsFinder(img)
    lmList = detector.positionFinder(img, draw=False)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        c1, c2 = (x1 + x2)//2, (y1 + y2)//2


        cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cv2.circle(img, (c1, c2), 15, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        #print(length)

############################ for windows ############################

        # vol = np.interp(length, [50, 300], [minVol, maxVol])
        # print(int(length), vol)
        # volume.SetMasterVolumeLevel(vol, None)

############################ for windows ############################


############################## for mac ##############################

        #target_volume = 50
        vol = "set volume output volume " + str(int(length - 26))
        osascript.osascript(vol)

        (0, 'output volume:'+str(int(length - 26))+', input volume:58, alert volume:100, output muted:false', '')

        result = osascript.osascript('get volume settings')
        print(result)
        print(type(result))
        volInfo = result[1].split(',')
        outputVol = volInfo[0].replace('output volume:', '')
        print(outputVol)

############################## for mac ##############################

        if length < 50:
            cv2.circle(img, (c1, c2), 15, (255, 100, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 2)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
