from pyimagesearch.gesture_recognition.motiondetector import MotionDetector
from pyimagesearch.gesture_recognition.gesturedetector import GestureDetector 
import numpy as np
import cv2
import imutils
import argparse

#argomenti da riga di comando
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--box", required=True,
        help="top, right, botton, left cordinate")
ap.add_argument("-v", "--video", required=False,
        help="se vuoi il video metti il path")
args = vars(ap.parse_args())

#faccio il check del video se non c'è uso la camera
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

camera.set(3, 1280)
camera.set(4, 720)

#prendo i valori per la costruzione della ROI
(top, right, bot, left) = np.int32(args["box"].split(","))
print("roi(%d, %d, %d, %d) " %(top, right, bot, left))

#inizializzo la l'instanza della classe motion
md = MotionDetector()
gd = GestureDetection()
#metto il counter dei frame a zero
numFrames = 0
gesture = None
bprint = True

# !! mainLoop:) !!
while True:
	#prendo il frame corrente
(grabbed, frame) = camera.read()
	#se sto utilizzando il video faccio il check su EOS
	if args.get("video") and not grabbed:
		break

	#prendo il frame lo flippo e lo croppo
	frame = imutils.resize(frame, width=600)
	frame = cv2.flip(frame, 1)
	clone = frame.copy()
	#shape ritorna il numero di righe colonne e canali
        (frameW, frameH) = frame.shape[:2]

	#setto la roi, passando in right:left 
	roi = frame[top:bot, right:left]
	#faccio il blur
	gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (7, 7), 0)

	#applico il motion detection quando ho raggiunto 32 frames
	if numFrames < 32:
		md.update(gray)
        
        else:
            #motion detection
            skin = md.detect(gray, 25, 15)

            #faccio il check se e' stato preso il contonro
            if skin is not None:
                (thresh, c) = skin
                cv2.drawContours(clone, [c + (right, top)], -1, (0, 255, 0), 2)
                fingers = gd.detect(thresh, c)

                #inizializzo l'oggetto dita
                if gesture is None:
                    gesture = [1, fingers]

                #conto delle dita
                else:
                    if gesture[1] == fingers:
                        gesture[0] += 1

                        #ferma la conta se seiamo arrivate a 25 frame
                        if gesture[0] >= 25:
                            if len(values) == 2:
                                values = []

                            values.append(fingers)
                            gesture = None

                    else:
                        gesture = None
    
    #disegno il risultato verificando se ce ne e uno
    if len(values) > 0:
        GestureDetector.drawBox(clone, 0)
        GestureDetector.drawText(clone, 0, values[0])
        GestureDetector.drawText(clone, 1, "+")

    if len(value ) > 2:
        GestureDetector.drawBox(clone, 2)
        GestureDetector.drawText(clone, 2, values[1])
        GestureDetector.drawText(clone, 3, "+")
        GestureDetector.drawText(clone, 4, color=(0, 255, 0))
        GestureDetector.drawText(clone, 4, values[0] + values[1], color=(0, 255, 0))

    #roi per la visualizzazione
    cv2.rectangle(clone, (left, top), (right, bot), (0, 0, 255), 2)
    numFrames += 1

    cv2.imshow("Frame", clone)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q")

camera.release()
cv2.destroyAllWindows()





